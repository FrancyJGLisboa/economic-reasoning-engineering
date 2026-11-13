"""Portable-context regressions, including isolated navigation and failures with refreshed hashes."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import context_package as cp

class PortableContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.project = self.root/'analysis'
        out = self.project/'output'
        out.mkdir(parents=True)
        (self.project/'corpus').mkdir()
        (self.project/'corpus/source.txt').write_text('A weaker currency may help only when exposure remains open.\n')
        ref = {'source_id':'s1','locator':'anchor: A weaker currency may help only when exposure remains open.'}
        method = dict(id='m1',episode_id='e1',title='Inspect actual FX exposure',trigger='Currency weakens',
          method_candidate='Reconcile currency exposure before inferring a margin change.',
          required_inputs=[{'name':'Effective FX rate','unit':'BRL/USD'}],
          ordered_steps=[{'order':1,'action':'Identify receipt and cost hedges.','readiness':'DATA_DISCOVERY_REQUIRED'}],
          competing_hypotheses=['A hedge neutralizes the spot change.'],
          discrimination_test='Compare effective rates with spot.',abstention_conditions=['Hedge unknown.'],
          source_vs_inference={'source':'Exposure condition.','investigator':'Hedge reconciliation.'},
          operational_readiness='CONCEPTUALLY_REUSABLE',source_refs=[ref])
        data={'sources':[{'source_id':'s1','filename':'corpus/source.txt','coverage':'One synthetic excerpt.'}],
          'episodes':[{'id':'e1','title':'Conditional FX claim','status':'ACCEPTED','source_refs':[ref]}],
          'opinions':[{'id':'o1','episode_id':'e1','thesis':'FX effect is conditional.','source_refs':[ref]}],
          'reasoning_cards':[method],
          'data_requirements':[{'id':'d1','episode_id':'e1','reasoning_id':'m1','required_inputs':[{'name':'Hedge'}],'source_refs':[ref]}],
          'reviews':[], 'state':{'status':'PARTIAL','accepted_episode_ids':['e1'],'reusable_method_ids':['m1']},
          'graph':{'nodes':[{'id':'n1','type':'OPINION','text':'Conditional FX claim','source_refs':[ref]}], 'edges':[]}}
        for name, value in data.items():cp.dump(out/(name+'.json'),value)
        for name in ('report.md','playbooks.md','backlog.md'):
            (out/name).write_text('Francy, inspect the conditional FX claim and the missing hedge data.\n')
        self.package = self.root/'portable/output'
        self.result = cp.build(self.project,self.package,'test-run','Conditional FX fixture')
        self.gid='test-run::reasoning_cards::m1'

    def mutate(self,name,change):
        data=cp.load(self.package/name)
        change(data)
        cp.dump(self.package/name,data)
        self.refresh_hashes()

    def refresh_hashes(self):
        manifest=cp.load(self.package/'manifest.json')
        for entry in manifest['files']:
            p=self.package/entry['path']
            if p.is_file():entry.update(bytes=p.stat().st_size,sha256=cp.digest(p))
        cp.dump(self.package/'manifest.json',manifest)

    def test_valid_nonempty_package(self):
        self.assertEqual(cp.validate_package(self.package),([],[]))
        self.assertGreater(len(cp.load(self.package/'manifest.json')['records']),0)

    def test_relocation_without_original_corpus(self):
        relocated=self.root/'elsewhere/output'
        shutil.copytree(self.package,relocated)
        self.project.rename(self.root/'unavailable-original')
        self.assertEqual(cp.validate_package(relocated),([],[]))
        result=cp.query(relocated,self.gid,True)
        self.assertIn('exposure remains open',result['evidence'][0]['quote'])
        self.assertEqual(result['record']['source_vs_inference']['investigator'],'Hedge reconciliation.')
        self.assertEqual(result['record']['abstention_conditions'],['Hedge unknown.'])

    def test_bundled_cli_works_from_unrelated_directory(self):
        cmd=[sys.executable,str(self.package/'tools/context_package.py'),'query','--package',str(self.package),'--id',self.gid,'--trace']
        result=subprocess.run(cmd,cwd=self.root,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual(json.loads(result.stdout)['record']['id'],'m1')

    def test_payload_tampering_fails(self):
        (self.package/'report.md').write_text('changed')
        self.assertTrue(any('Changed payload' in e for e in cp.validate_package(self.package)[0]))

    def test_stale_receipt_fails_after_resealing(self):
        receipt=self.package/self.result['receipt']
        self.mutate('state.json',lambda x:x.update(status='STOPPED'))
        errors,_=cp.check_receipt(self.package,receipt)
        self.assertTrue(any('Stale receipt' in e for e in errors))

    def test_fabricated_anchor_fails_even_with_updated_hashes(self):
        self.mutate('reasoning_cards.json',lambda x:x[0]['source_refs'][0].update(anchor='unsupported words'))
        self.assertTrue(any('fabricated anchor' in e for e in cp.validate_package(self.package)[0]))

    def test_source_reference_filename_mismatch_fails(self):
        self.mutate('reasoning_cards.json',lambda x:x[0]['source_refs'][0].update(filename='report.md'))
        self.assertTrue(any('does not match' in e for e in cp.validate_package(self.package)[0]))

    def test_wrong_anchor_line_fails(self):
        self.mutate('reasoning_cards.json',lambda x:x[0]['source_refs'][0].update(line=999))
        self.assertTrue(any('line mismatch' in e for e in cp.validate_package(self.package)[0]))

    def test_missing_method_field_fails(self):
        self.mutate('reasoning_cards.json',lambda x:x[0].pop('abstention_conditions'))
        self.assertTrue(any('requires abstention_conditions' in e for e in cp.validate_package(self.package)[0]))

    def test_unknown_episode_fails(self):
        self.mutate('reasoning_cards.json',lambda x:x[0].update(episode_id='missing'))
        self.assertTrue(any('unresolved episode_id' in e for e in cp.validate_package(self.package)[0]))

    def test_manifest_index_drift_fails(self):
        self.mutate('manifest.json',lambda x:x['records'].pop())
        self.assertTrue(any('index does not match' in e for e in cp.validate_package(self.package)[0]))

    def test_path_escape_fails(self):
        self.mutate('sources.json',lambda x:x[0].update(filename='../outside.txt'))
        self.assertTrue(any('escapes' in e for e in cp.validate_package(self.package)[0]))

    def test_absolute_path_fails(self):
        self.mutate('sources.json',lambda x:x[0].update(filename='/tmp/outside.txt'))
        self.assertTrue(any('escapes' in e for e in cp.validate_package(self.package)[0]))

    def test_symlink_escape_fails(self):
        (self.root/'external.txt').write_text('external')
        (self.package/'outside-link.txt').symlink_to(self.root/'external.txt')
        self.mutate('sources.json',lambda x:x[0].update(filename='outside-link.txt'))
        self.assertTrue(any('symlink escapes' in e for e in cp.validate_package(self.package)[0]))

    def test_run_ids_prevent_cross_run_collision(self):
        other=self.root/'other/output'
        cp.build(self.project,other,'other-run','Other run')
        a={r['global_id'] for r in cp.load(self.package/'manifest.json')['records']}
        b={r['global_id'] for r in cp.load(other/'manifest.json')['records']}
        self.assertFalse(a & b)

    def test_local_id_only_is_refused(self):
        with self.assertRaises(ValueError):cp.query(self.package,'m1')

    def test_query_refuses_invalid_package(self):
        (self.package/'state.json').write_text('invalid JSON')
        with self.assertRaises(ValueError):cp.query(self.package,self.gid)

    def test_missing_corpus_is_not_invented(self):
        (self.project/'corpus/source.txt').unlink()
        with self.assertRaises(ValueError):cp.build(self.project,self.root/'bad/output','bad-run','Missing source')

    def test_original_files_are_not_modified(self):
        data=cp.load(self.project/'output/reasoning_cards.json')
        self.assertNotIn('global_id',data[0])
        self.assertEqual(data[0]['source_refs'][0]['locator'].split(': ')[0],'anchor')

    def test_nonempty_output_is_not_overwritten(self):
        with self.assertRaises(ValueError):cp.build(self.project,self.package,'another-run','Overwrite')

    def test_explicit_unavailable_unreferenced_source_is_preserved(self):
        sources=cp.load(self.project/'output/sources.json')
        sources.append({'source_id':'missing_chart','filename':None,'coverage':'Chart mentioned, not supplied.'})
        cp.dump(self.project/'output/sources.json',sources)
        other=self.root/'missing-chart/output'
        cp.build(self.project,other,'chart-run','Missing chart inventory')
        source=cp.load(other/'sources.json')[1]
        self.assertEqual(source['availability'],'unavailable')
        self.assertTrue(source['unavailable_reason'])
        self.assertEqual(cp.validate_package(other),([],[]))

    def test_legacy_validator_routes_portable_packages(self):
        legacy=Path(cp.__file__).with_name('validate.py')
        result=subprocess.run([sys.executable,str(legacy),'--project',str(self.package.parent)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_false_model_evaluation_claim_is_refused(self):
        self.mutate('manifest.json',lambda x:x['validation_claims'].update(model_navigation_evaluation='PASS'))
        self.assertTrue(any('Unsupported semantic' in e for e in cp.validate_package(self.package)[0]))

if __name__=='__main__':unittest.main(verbosity=2)
