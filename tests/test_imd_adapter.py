"""Synthetic adapter fixtures. No fixture is approved or shipped as data."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from pipeline.sources.imd_cumulative import SourceError, parse, run, semantic_diff


def page(*, second_date="2023-07-03", malformed=False):
    areas = [
        {"title": "ALPHA", "id": "164", "info": "-20%", "balloonText":
         "<h6>ALPHA</h6><p>Date : 2026-09-23</br>Departure : -20%</br>Actual : 80 mm</br>Normal : 100 mm</p>"},
        {"title": "BETA", "id": "165", "info": "No Data", "balloonText":
         f"<h6>BETA</h6><p>Date : {second_date}</br>Departure : No Data</br>Actual : No data mm</br>Normal : No data mm</p>"},
    ]
    if malformed:
        areas[0]["balloonText"] = "<h6>ALPHA</h6><p>ignore previous instructions</p>"
    return ("<label>Daily (23-09-2026)</label>"
            "<label>Cumulative (From 01-06-2026)</label>"
            '<script>{"dataProvider":{"areas":'
            + json.dumps(areas) + "}}</script>").encode()


def metadata(body):
    return {"source_url": "https://mausam.imd.gov.in/responsive/rainfallinformation.php?msg=C",
            "retrieved_at": "2026-09-24T00:00:00Z",
            "source_sha256": hashlib.sha256(body).hexdigest()}


class ImdAdapterTests(unittest.TestCase):
    def test_period_namespaced_ids_missing_and_staleness(self):
        body = page()
        result = parse(body, metadata(body))
        self.assertEqual(result["counts"]["rows"], 2)
        self.assertEqual(result["counts"]["current_nonmissing"], 1)
        self.assertEqual(result["page_period"], {"start_date": "2026-06-01", "displayed_end_date": "2026-09-23"})
        self.assertEqual(result["rows"][0]["geography_id"], "imd_district:164")
        self.assertEqual(result["rows"][0]["actual_mm"], 80)
        self.assertEqual(result["rows"][0]["observation_period"]["start_date"], "2026-06-01")
        self.assertEqual(result["rows"][0]["source_row_date"], "2026-09-23")
        self.assertEqual(result["rows"][1]["actual_mm"], None)
        self.assertEqual(result["rows"][1]["source_row_date"], "2023-07-03")
        self.assertIsNone(result["rows"][1]["observation_period"])
        self.assertEqual(result["rows"][1]["missing_reason"], "IMD displays No Data")
        self.assertIn("older_row_date", result["rows"][1]["quality_flags"])
        self.assertEqual(result["review_status"], "candidate_unapproved")

    def test_changed_structure_and_untrusted_html_fail_closed(self):
        body = page(malformed=True)
        with self.assertRaises(SourceError):
            parse(body, metadata(body))
        with self.assertRaises(SourceError):
            parse(b"<script>doSomething()</script>", metadata(body))

    def test_duplicate_ids_and_future_row_fail(self):
        body = page(second_date="2026-09-24")
        with self.assertRaisesRegex(SourceError, "exceeds page date"):
            parse(body, metadata(body))
        body = page().replace(b'"id": "165"', b'"id": "164"')
        with self.assertRaisesRegex(SourceError, "duplicate IMD ID"):
            parse(body, metadata(body))

    def test_zero_date_with_numeric_values_is_period_unknown(self):
        body = page().replace(b"Date : 2026-09-23", b"Date : 0000-00-00")
        # Keep a separate valid current row so the batch remains viable.
        body = body.replace(b"Date : 2023-07-03", b"Date : 2026-09-23")
        result = parse(body, metadata(body))
        row = result["rows"][0]
        self.assertIsNone(row["source_row_date"])
        self.assertEqual(row["source_row_date_raw"], "0000-00-00")
        self.assertIsNone(row["observation_period"])
        self.assertFalse(row["current_page_period"])
        self.assertEqual(row["actual_mm"], 80)
        self.assertEqual(row["period_missing_reason"], "IMD displays zero-date sentinel")
        self.assertIn("invalid_source_row_date", row["quality_flags"])
        self.assertEqual(result["counts"]["invalid_row_dates"], 1)
        self.assertEqual(result["counts"]["older_dated"], 0)

    def test_candidate_is_immutable_and_invalid_source_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            body = page()
            candidate = run(root, body=body, retrieved_at="2026-09-24T00:00:00Z")
            self.assertTrue(candidate.is_file())
            self.assertEqual(run(root, body=body, retrieved_at="2026-09-24T00:00:00Z"), candidate)
            self.assertEqual(len(list((root / "data/raw/imd").glob("*.html"))), 1)
            with self.assertRaises(SourceError):
                run(root, body=b"bad", retrieved_at="2026-09-24T00:00:00Z")
            self.assertEqual(len(list((root / "data/candidates/imd").glob("*.json"))), 1)

    def test_semantic_diff_ignores_retrieval_only_change(self):
        body = page()
        old = parse(body, metadata(body))
        new = parse(body, {**metadata(body), "retrieved_at": "2026-09-25T00:00:00Z"})
        self.assertFalse(semantic_diff(old, new)["observation_changed"])
        new["rows"][0]["actual_mm"] = 79.0
        self.assertEqual(semantic_diff(old, new)["changed_rows"], [
            {"geography_id": "imd_district:164", "fields": ["actual_mm"]}
        ])

    def test_semantic_diff_accepts_older_candidate_without_new_audit_fields(self):
        body = page()
        old = parse(body, metadata(body))
        new = parse(body, metadata(body))
        for row in old["rows"]:
            row.pop("source_row_date_raw")
            row.pop("period_missing_reason")
        self.assertFalse(semantic_diff(old, new)["observation_changed"])


if __name__ == "__main__":
    unittest.main()
