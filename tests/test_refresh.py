"""Candidate refresh behavior with synthetic source bytes in temporary roots."""

from datetime import datetime
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from pipeline.refresh import parse_as_of, refresh
from pipeline.sources.imd_cumulative import SourceError


def fixture_page(actual="80"):
    area = [{"title": "ALPHA", "id": "164", "info": "-20%", "balloonText":
             f"<h6>ALPHA</h6><p>Date : 2026-09-23</br>Departure : -20%</br>Actual : {actual} mm</br>Normal : 100 mm</p>"}]
    return ("<label>Daily (23-09-2026)</label>"
            "<label>Cumulative (From 01-06-2026)</label>"
            '<script>{"dataProvider":{"areas":'
            + json.dumps(area) + "}}</script>").encode()


def fake_fetch(body, retrieved):
    return lambda: (body, {"source_url": "https://mausam.imd.gov.in/responsive/rainfallinformation.php?msg=C",
                            "retrieved_at": retrieved, "source_sha256": hashlib.sha256(body).hexdigest(),
                            "response_bytes": len(body), "http_status": 200,
                            "content_type": "text/html", "http_last_modified": None, "http_date": None})


class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.as_of = parse_as_of("2026-09-24T12:00:00+05:30")

    def tearDown(self):
        self.temp.cleanup()

    def test_first_candidate_then_no_change_reuses_candidate(self):
        body = fixture_page()
        first_path, first = refresh(self.root, scope="all", as_of=self.as_of,
                                    fetcher=fake_fetch(body, "2026-09-24T06:00:00Z"))
        self.assertEqual(first["status"], "candidate_created")
        self.assertTrue(first["diff"]["baseline"])
        self.assertEqual((self.root / first["raw_snapshot_path"]).read_bytes(), body)
        self.assertEqual(first["raw_snapshot_sha256"], hashlib.sha256(body).hexdigest())
        self.assertEqual(json.loads((self.root / first["candidate_path"]).read_text())["source"]["raw_snapshot_path"],
                         first["raw_snapshot_path"])
        second_path, second = refresh(self.root, scope="all", as_of=self.as_of,
                                      fetcher=fake_fetch(body, "2026-09-24T06:01:00Z"))
        self.assertEqual(second["status"], "no_change")
        self.assertFalse(second["diff"]["observation_changed"])
        self.assertEqual(second["candidate_path"], first["candidate_path"])
        self.assertEqual(second["raw_snapshot_path"], first["raw_snapshot_path"])
        self.assertNotEqual(first_path, second_path)
        self.assertEqual(len(list((self.root / "data/candidates/imd").glob("*.json"))), 1)
        self.assertEqual(len(list((self.root / "data/raw/imd").glob("*.html"))), 1)
        self.assertFalse((self.root / "data/approved").exists())
        self.assertFalse(second["deployment_performed"])

    def test_changed_observation_makes_candidate_and_diff(self):
        first_body = fixture_page()
        _, first = refresh(self.root, scope="imd", as_of=self.as_of,
                           fetcher=fake_fetch(first_body, "2026-09-24T06:00:00Z"))
        # Keep published departure unchanged: the candidate carries an
        # arithmetic review flag, but a changed source value is still diffed.
        second_body = fixture_page(actual="79")
        _, second = refresh(self.root, scope="imd", as_of=self.as_of,
                            fetcher=fake_fetch(second_body, "2026-09-24T06:01:00Z"))
        self.assertEqual(second["status"], "candidate_created")
        self.assertTrue(second["diff"]["observation_changed"])
        self.assertEqual(second["diff"]["changed_rows"][0]["fields"], ["actual_mm"])
        self.assertNotEqual(first["candidate_path"], second["candidate_path"])

    def test_failed_fetch_and_invalid_source_preserve_existing(self):
        body = fixture_page()
        refresh(self.root, scope="all", as_of=self.as_of,
                fetcher=fake_fetch(body, "2026-09-24T06:00:00Z"))
        before = sorted((p.name, p.read_bytes()) for p in (self.root / "data/candidates/imd").glob("*.json"))
        with self.assertRaises(OSError):
            refresh(self.root, scope="all", as_of=self.as_of,
                    fetcher=lambda: (_ for _ in ()).throw(OSError("network unavailable")))
        with self.assertRaises(SourceError):
            refresh(self.root, scope="all", as_of=self.as_of,
                    fetcher=fake_fetch(b"login page", "2026-09-24T06:01:00Z"))
        after = sorted((p.name, p.read_bytes()) for p in (self.root / "data/candidates/imd").glob("*.json"))
        self.assertEqual(before, after)

    def test_rejects_unknown_scope_and_naive_as_of(self):
        with self.assertRaises(SourceError):
            parse_as_of("2026-09-24T12:00:00")
        with self.assertRaises(SourceError):
            refresh(self.root, scope="karnataka", as_of=self.as_of,
                    fetcher=fake_fetch(fixture_page(), "2026-09-24T06:00:00Z"))

    def test_rejects_future_page_date(self):
        too_early = datetime.fromisoformat("2026-09-22T12:00:00+05:30")
        with self.assertRaisesRegex(SourceError, "after --as-of"):
            refresh(self.root, scope="all", as_of=too_early,
                    fetcher=fake_fetch(fixture_page(), "2026-09-24T06:00:00Z"))
        self.assertFalse((self.root / "data/candidates/imd").exists())


if __name__ == "__main__":
    unittest.main()
