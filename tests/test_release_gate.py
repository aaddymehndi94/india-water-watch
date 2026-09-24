"""Temporary synthetic STRUCTURAL tests. No mock site is exported or published."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from tools.release_gate import COLLECTIONS, COMPARISON_FIELDS, gate, safe_relative, snapshot_digest

class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        (self.root/'data').mkdir(); (self.root/'state').mkdir()
        self.data={name:[] for name in COLLECTIONS}
        self.write_data()
        self.write('state/RELEASE_REVIEW.json',{'checks':[],'blocking_findings':[]})
        self.write('state/PUBLICATION_POLICY.json',{'first_deployment_authorized':False})
    def tearDown(self): self.temp.cleanup()
    def write(self,path,value):
        p=self.root/path; p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(value),encoding='utf-8')
    def write_data(self):
        for name,value in self.data.items(): self.write(f'data/{name}.json',value)
    def errors(self): return '\n'.join(gate(self.root))
    def make_manifest(self):
        dist=self.root/'dist'; dist.mkdir(exist_ok=True)
        (dist/'index.html').write_text('<!doctype html><title>Structural fixture only</title>',encoding='utf-8')
        digest=snapshot_digest(self.data)
        manifest={'release_id':'test-only','snapshot_sha256':digest,'source_watermarks':{'fixture':'2020-01-01'},
            'files_sha256':{'index.html':hashlib.sha256((dist/'index.html').read_bytes()).hexdigest()}}
        self.write('dist/release.json',manifest)
        return manifest
    def test_empty_starter_is_not_publication(self):
        e=self.errors(); self.assertIn('No public observations',e); self.assertIn('dist/index.html is missing',e)
    def test_wrong_collection_shape_is_failure_not_crash(self):
        self.write('data/claims.json',{})
        self.assertIn('Cannot read claims',self.errors())
    def test_malformed_records_are_failure_not_crash(self):
        self.data['observations']=[None,'value',{'id':[]}]
        self.data['comparisons']=[None]
        self.write_data(); self.assertIn('Malformed or duplicate IDs',self.errors())
    def test_duplicate_ids_rejected(self):
        self.data['observations']=[{'id':'x'},{'id':'x'}]; self.write_data()
        self.assertIn('duplicate IDs',self.errors())
    def test_public_synthetic_rejected(self):
        self.data['observations']=[{'id':'x','public':True,'synthetic':True}]; self.write_data()
        self.assertIn('Synthetic record cannot publish',self.errors())
    def test_public_flag_requires_bool(self):
        self.data['observations']=[{'id':'x','public':'yes'}]; self.write_data()
        self.assertIn('Invalid public flag',self.errors())
    def test_orphan_source_rejected(self):
        self.data['claims']=[{'id':'c','public':True,'status':'verified','reviewer_id':'agent','evidence_ids':['missing']}]
        self.write_data(); self.assertIn('Uninspected/orphan evidence',self.errors())
    def test_unsafe_source_url_rejected(self):
        self.data['evidence']=[{'id':'e','source_inspected':True,'locator':'table','url':'javascript:alert(1)'}]
        self.data['observations']=[{'id':'o','public':True,'evidence_ids':['e']}]
        self.write_data(); self.assertIn('Unsafe evidence URL',self.errors())
    def test_malformed_evidence_list_rejected(self):
        self.data['claims']=[{'id':'c','public':True,'evidence_ids':[{}]}]; self.write_data()
        self.assertIn('Malformed evidence references',self.errors())
    def test_unreviewed_claim_rejected(self):
        self.data['claims']=[{'id':'c','public':True,'status':'draft'}]; self.write_data()
        self.assertIn('Unreviewed claim cannot publish',self.errors())
    def test_missing_human_review_reference_rejected(self):
        self.data['claims']=[{'id':'c','public':True,'requires_human_review':True}]; self.write_data()
        self.assertIn('Missing genuine human-review reference',self.errors())
    def test_incompatible_comparison_rejected(self):
        flags={key:'match' for key in COMPARISON_FIELDS}; flags['baseline']='mismatch'
        self.data['comparisons']=[{'id':'c','public':True,'status':'allowed','checks':flags,'reviewer_id':'agent'}]
        self.write_data(); self.assertIn('Incompatible comparison allowed',self.errors())
    def test_incomplete_comparison_rejected(self):
        self.data['comparisons']=[{'id':'c','public':True,'status':'allowed','checks':{}}]
        self.write_data(); self.assertIn('Incomplete comparison checks',self.errors())
    def test_harmonization_needs_method(self):
        flags={key:'match' for key in COMPARISON_FIELDS}; flags['baseline']='harmonized'
        self.data['comparisons']=[{'id':'c','public':True,'status':'allowed','checks':flags}]
        self.write_data(); self.assertIn('Missing harmonization method',self.errors())
    def test_nonfinite_snapshot_rejected(self):
        self.data['observations']=[{'id':'o','value':float('nan')}]; self.write_data()
        self.assertIn('invalid non-finite',self.errors())
    def test_digest_deterministic_for_object_key_order(self):
        self.assertEqual(snapshot_digest({'a':1,'b':2}),snapshot_digest({'b':2,'a':1}))
    def test_digest_changes_on_revision(self):
        self.assertNotEqual(snapshot_digest({'a':1}),snapshot_digest({'a':2}))
    def test_paths_cannot_escape_root(self):
        for path in ['../outside','/etc/passwd','C:\\Windows\\secret',None,'','\x00']:
            with self.subTest(path=path): self.assertIsNone(safe_relative(self.root,path))
        self.assertEqual(safe_relative(self.root,'reports/check.txt'),self.root/'reports/check.txt')
    def test_manifest_must_be_object(self):
        self.write('dist/release.json',[])
        self.assertIn('manifest missing/invalid',self.errors())
    def test_file_tampering_detected(self):
        self.make_manifest(); (self.root/'dist/index.html').write_text('modified',encoding='utf-8')
        self.assertIn('file inventory/hash mismatch',self.errors())
    def test_source_revision_invalidates_built_manifest(self):
        self.make_manifest(); self.data['claims']=[{'id':'new'}]; self.write_data()
        self.assertIn('does not match reviewed input snapshot',self.errors())
    def test_nested_release_manifest_is_not_exempt(self):
        self.make_manifest(); self.write('dist/extra/release.json',{'unexpected':True})
        self.assertIn('file inventory/hash mismatch',self.errors())
    def test_private_output_rejected(self):
        self.make_manifest(); self.write('dist/raw/private.json',{'secret':'fixture'})
        self.assertIn('Forbidden public output',self.errors())
    def test_placeholder_leak_rejected(self):
        self.make_manifest(); (self.root/'dist/index.html').write_text('SYNTHETIC_TEST_FIXTURE',encoding='utf-8')
        self.assertIn('Placeholder/test fixture leaked',self.errors())
    def test_checkbox_alone_is_not_review_evidence(self):
        self.make_manifest()
        self.write('state/RELEASE_REVIEW.json',{'checks':[{'id':'data','status':'passed','reviewer':'agent'}]})
        self.assertIn('Missing evidenced review checks',self.errors())
    def test_publication_requires_specific_authorization(self):
        self.make_manifest(); e='\n'.join(gate(self.root,publication=True))
        self.assertIn('No explicit destination/publication authorization',e)
        self.assertIn('Authorization is not tied to this release',e)
    def test_malformed_review_check_handled(self):
        self.write('state/RELEASE_REVIEW.json',{'checks':[None]})
        self.assertIn('Malformed review check',self.errors())
    def test_no_fixture_accidentally_passes_publication(self):
        self.make_manifest(); self.assertTrue(gate(self.root,publication=True))

if __name__=='__main__': unittest.main()
