"""Publication tools use the real approved snapshot, then mutate isolated copies."""
from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

from tools.build_publication_data import publication, write_publication
from tools.export_journalists import safe_cell, write_exports
from tools.package_site import package_site
from tools.validate_approved import ROOT, load_collections, validate


class PublicationToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "data" / "approved").mkdir(parents=True)
        shutil.copytree(ROOT / "schemas", self.root / "schemas")
        self.rows = copy.deepcopy(load_collections())
        self.save()

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        for name, rows in self.rows.items():
            (self.root / "data" / "approved" / f"{name}.json").write_text(json.dumps(rows), encoding="utf-8")

    def test_current_snapshot_and_projection_traceability(self):
        self.assertEqual([], validate(self.root))
        result = publication(self.root)
        claims = {x["id"]: x for x in result["claims"]}
        sources = {x["id"]: x for x in result["sources"]}
        self.assertTrue(claims)
        self.assertTrue(result["observations"])
        for observation in result["observations"]:
            self.assertIn(observation["claimId"], claims)
            self.assertIn(observation["sourceId"], sources)
            self.assertIn(observation["sourceId"], claims[observation["claimId"]]["evidenceIds"])
        for source in result["sources"]:
            self.assertTrue(source["url"].startswith("https://"))
            self.assertNotIn("local_snapshot_path", source)
            self.assertNotIn("access_notes", source)
        roster_refs = {eid for geo in self.rows["geographies"] if geo["kind"] in {"state", "ut", "union_territory"} for eid in geo["evidence_ids"]}
        self.assertTrue(roster_refs.issubset(sources))
        self.assertEqual("andhra-pradesh", next(g["slug"] for g in result["geographies"] if g["name"] == "Andhra Pradesh"))
        out = self.root / "publication.json"
        write_publication(self.root, out)
        digest = hashlib.sha256(out.read_bytes()).hexdigest()
        write_publication(self.root, out)
        self.assertEqual(digest, hashlib.sha256(out.read_bytes()).hexdigest())

    def test_synthetic_public_observation_blocked(self):
        row = next(x for x in self.rows["observations"] if x["public"])
        row["synthetic"] = True
        self.save()
        self.assertIn("synthetic", "\n".join(validate(self.root)))
        with self.assertRaises(ValueError):
            publication(self.root)

    def test_unreviewed_public_claim_blocked(self):
        row = next(x for x in self.rows["claims"] if x["public"])
        row["reviewed_at"] = None
        self.save()
        self.assertIn("must be reviewed", "\n".join(validate(self.root)))

    def test_orphan_and_unsafe_evidence_blocked(self):
        row = next(x for x in self.rows["claims"] if x["public"])
        row["evidence_ids"] = ["unknown-evidence"]
        self.rows["evidence"][0]["url"] = "http://127.0.0.1/private"
        self.save()
        errors = "\n".join(validate(self.root))
        self.assertIn("missing reference", errors)
        self.assertIn("unsafe source URL", errors)

    def test_reversed_observation_period_blocked(self):
        row = next(x for x in self.rows["observations"] if x["public"])
        row["period"]["start"], row["period"]["end"] = row["period"]["end"], row["period"]["start"]
        self.save()
        self.assertIn("period ends before it starts", "\n".join(validate(self.root)))

    def test_public_observation_needs_reviewed_claim(self):
        self.rows["claims"] = []
        self.save()
        with self.assertRaisesRegex(ValueError, "no reviewed public claim"):
            publication(self.root)

    def test_csv_formula_safety_and_export_links(self):
        for value in ("=SUM(1,1)", "+cmd", "-cmd", "@cmd", "\t=SUM(1,1)"):
            self.assertTrue(safe_cell(value).startswith("'"))
        self.assertEqual("0", safe_cell(0))
        self.assertEqual("-14.9", safe_cell(-14.9))
        output = write_exports(self.root, self.root / "exports")
        with (output / "observations.csv").open(encoding="utf-8-sig", newline="") as stream:
            observations = list(csv.DictReader(stream))
        with (output / "claims.csv").open(encoding="utf-8-sig", newline="") as stream:
            claims = {x["id"] for x in csv.DictReader(stream)}
        self.assertTrue(observations)
        self.assertTrue(all(x["claimId"] in claims for x in observations))
        self.assertIn("Snapshot SHA-256", (output / "README.txt").read_text())

    def test_zip_is_deterministic_and_blocks_private_files(self):
        dist = self.root / "dist"
        dist.mkdir()
        (dist / "index.html").write_text("<h1>Example</h1>", encoding="utf-8")
        (dist / "assets").mkdir()
        (dist / "assets" / "x.css").write_text("body{}", encoding="utf-8")
        first = self.root / "a.zip"
        second = self.root / "b.zip"
        summary = package_site(dist, first)
        package_site(dist, second)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertEqual(2, summary["file_count"])
        with zipfile.ZipFile(first) as archive:
            self.assertEqual(["assets/x.css", "index.html"], archive.namelist())
        (dist / "raw").mkdir()
        (dist / "raw" / "secret.txt").write_text("secret")
        with self.assertRaisesRegex(ValueError, "Forbidden public path"):
            package_site(dist, self.root / "c.zip")
        with self.assertRaisesRegex(ValueError, "outside dist"):
            package_site(dist, dist / "site.zip")


if __name__ == "__main__":
    unittest.main()
