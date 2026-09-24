"""Starter packaging checks, not verification of reporting or a website."""
import csv
import json
from pathlib import Path
import unittest
from tools.validate_starter import validate
ROOT=Path(__file__).resolve().parents[1]

class StarterTests(unittest.TestCase):
    def test_structure(self): self.assertEqual(validate(ROOT),[])
    def test_all_tasks_unexecuted_in_starter(self):
        tasks=json.loads((ROOT/'project/tasks.json').read_text(encoding='utf-8'))
        # This is a starter-only invariant. Replace this test as implementation begins.
        if json.loads((ROOT/'state/PROJECT_STATE.json').read_text(encoding='utf-8')).get('phase')=='starter_only':
            self.assertTrue(all(t['status']=='not_started' for t in tasks))
    def test_acceptance_ids_unique(self):
        with (ROOT/'project/acceptance.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
        ids=[r['id'] for r in rows]
        self.assertEqual(len(ids),len(set(ids))); self.assertTrue(rows)
        self.assertTrue(all(r['verification'] and r['owner_role'] for r in rows))
    def test_original_html_not_in_package(self):
        self.assertFalse((ROOT/'south_india_water_stress_2002_vs_2026.html').exists())
    def test_no_enabled_workflows_in_starter(self):
        if json.loads((ROOT/'state/PROJECT_STATE.json').read_text(encoding='utf-8')).get('phase')=='starter_only':
            self.assertFalse(list((ROOT/'.github/workflows').glob('*.yml'))+list((ROOT/'.github/workflows').glob('*.yaml')))

if __name__=='__main__': unittest.main()
