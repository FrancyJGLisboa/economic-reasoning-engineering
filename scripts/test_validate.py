"""Regression checks for source requirements and project-relative output paths."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('validate.py')
spec = importlib.util.spec_from_file_location('economic_validator', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        self.out = self.project / 'output'
        self.out.mkdir()
        self.data = {name: [] for name in validator.ARRAYS}
        ref = {'source_id': 'source_1', 'locator': 'paragraph 1'}
        self.data.update(sources=[{'source_id': 'source_1'}],
          episodes=[{'id': 'episode_1', 'status': 'ACCEPTED', 'source_refs': [ref]}],
          opinions=[{'id': 'opinion_1', 'source_refs': [ref]}],
          graph={'nodes': [], 'edges': []}, state={'status': 'COMPLETE'})
        self.save()

    def save(self):
        for name, value in self.data.items():
            (self.out / (name + '.json')).write_text(json.dumps(value))

    def test_valid_package(self):
        self.assertEqual(validator.validate(self.project)[0], [])

    def test_default_cli_uses_working_project(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], cwd=self.project, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_explicit_cli_path_from_another_directory(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--output', str(self.out)],
                                cwd=self.out, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_opinion_without_evidence_fails(self):
        self.data['opinions'][0].pop('source_refs')
        self.save()
        self.assertTrue(any('requires non-empty source_refs' in e for e in validator.validate(self.project)[0]))

    def test_unknown_source_fails(self):
        self.data['opinions'][0]['source_refs'][0]['source_id'] = 'missing'
        self.save()
        self.assertTrue(any('unknown source' in e for e in validator.validate(self.project)[0]))

    def test_empty_complete_fails_but_blocked_is_allowed(self):
        self.data['episodes'] = []
        self.save()
        self.assertTrue(any('COMPLETE requires' in e for e in validator.validate(self.project)[0]))
        self.data['state']['status'] = 'BLOCKED'
        self.save()
        self.assertEqual(validator.validate(self.project)[0], [])

    def test_malformed_graph_returns_errors(self):
        self.data['graph'] = {'nodes': None, 'edges': None}
        self.save()
        self.assertIn('graph.nodes must be list', validator.validate(self.project)[0])

    def test_missing_locator_fails(self):
        self.data['opinions'][0]['source_refs'][0]['locator'] = ''
        self.save()
        self.assertTrue(any('missing locator' in e for e in validator.validate(self.project)[0]))

    def anchor_fixture(self, text="Revenue fell, but field application stayed normal.", suffix=".txt"):
        corpus=self.project/'corpus'
        corpus.mkdir(exist_ok=True)
        filename='source'+suffix
        (corpus/filename).write_text(text)
        self.data['sources'][0]['filename']='corpus/'+filename
        self.data['opinions'][0]['source_refs']=[{'source_id':'source_1','locator':'anchor: field application stayed normal'}]
        self.save()

    def test_exact_anchor_passes(self):
        self.anchor_fixture()
        self.assertEqual(validator.validate(self.project)[0], [])

    def test_fabricated_anchor_fails(self):
        self.anchor_fixture()
        self.data['opinions'][0]['source_refs'][0]['locator']='anchor: field application collapsed'
        self.save()
        self.assertTrue(any('anchor not in corpus' in e for e in validator.validate(self.project)[0]))

    def test_missing_corpus_does_not_silently_pass_anchor(self):
        self.data['opinions'][0]['source_refs'][0]['locator']='anchor: unverified claim'
        self.save()
        self.assertTrue(any('source text unavailable' in e for e in validator.validate(self.project)[0]))

    def test_markdown_source_anchors(self):
        self.anchor_fixture(suffix='.md')
        self.assertEqual(validator.validate(self.project)[0], [])

    def test_anchor_in_wrong_source_fails(self):
        self.anchor_fixture(text='Only different evidence exists here.')
        (self.project/'corpus/other.txt').write_text('field application stayed normal')
        self.assertTrue(any('anchor not in corpus' in e for e in validator.validate(self.project)[0]))

    def test_duplicated_method_warns(self):
        ref={'source_id':'source_1','locator':'paragraph 1'}
        self.data['reasoning_cards']=[{'id':str(i),'method_candidate':'Compare actual farm applications','source_refs':[ref]} for i in range(2)]
        self.save()
        errors,warnings=validator.validate(self.project)
        self.assertFalse(errors)
        self.assertTrue(any('duplicate method' in w for w in warnings))

    def test_unknown_episode_reference_fails(self):
        self.data['opinions'][0]['episode_id']='missing'
        self.save()
        self.assertTrue(any('unknown episode_id' in e for e in validator.validate(self.project)[0]))

if __name__ == '__main__':
    unittest.main(verbosity=2)
