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

    def declare_profile(self, name='operations'):
        state = cp.load(self.project/'output/state.json')
        state['analysis_profile'] = {'name': name, 'selection_reason': 'Inspect delivery feasibility.',
                                     'scope_limits': ['No observed shipment performance.']}
        cp.dump(self.project/'output/state.json', state)
        cards = cp.load(self.project/'output/reasoning_cards.json')
        cards[0]['expected_outputs'] = ['Conditional exposure comparison in BRL per tonne.']
        cp.dump(self.project/'output/reasoning_cards.json', cards)

    def test_declared_profiles_survive_relocation(self):
        for name in ('economics', 'operations'):
            with self.subTest(profile=name):
                self.declare_profile(name)
                package = self.root/name
                cp.build(self.project, package, name, 'Declared profile')
                relocated = self.root/(name + '-relocated')
                shutil.move(str(package), str(relocated))
                self.assertEqual(cp.validate_package(relocated), ([], []))
                profile = cp.load(relocated/'manifest.json')['analysis_profile']
                self.assertEqual(profile, cp.load(relocated/'state.json')['analysis_profile'])
                self.assertEqual(profile['name'], name)
                self.assertIn('Analysis profile: ' + name, (relocated/'CONTEXT.md').read_text())
                self.assertTrue(cp.query(relocated, name + '::reasoning_cards::m1')['record']['expected_outputs'])

    def test_legacy_profile_is_not_fabricated(self):
        self.assertNotIn('analysis_profile', cp.load(self.package/'manifest.json'))
        self.assertIn('not recorded', (self.package/'CONTEXT.md').read_text())
        self.assertEqual(cp.validate_package(self.package), ([], []))

    def test_invalid_profile_refused_before_writing(self):
        self.declare_profile('strategy')
        destination = self.root/'invalid-profile'
        with self.assertRaisesRegex(ValueError, 'unsupported value'):
            cp.build(self.project, destination, 'bad-profile', 'Invalid')
        self.assertFalse(destination.exists())

    def test_profile_requires_selection_reason_and_limits(self):
        self.declare_profile()
        state_path = self.project/'output/state.json'
        for change in ({'selection_reason': ''}, {'scope_limits': []}):
            state = cp.load(state_path)
            state['analysis_profile'].update(change)
            cp.dump(state_path, state)
            with self.assertRaises(ValueError):
                cp.build(self.project, self.root/'bad-metadata', 'bad', 'Invalid metadata')
            self.declare_profile()

    def test_profile_requires_method_outputs(self):
        self.declare_profile()
        cards_path = self.project/'output/reasoning_cards.json'
        cards = cp.load(cards_path)
        for value in (None, [], [''], 'delivery'):
            if value is None:
                cards[0].pop('expected_outputs', None)
            else:
                cards[0]['expected_outputs'] = value
            cp.dump(cards_path, cards)
            with self.assertRaises(ValueError):
                cp.build(self.project, self.root/'missing-outputs', 'bad', 'Missing outputs')

    def test_profile_mismatch_refused_with_refreshed_hashes(self):
        self.declare_profile()
        package = self.root/'profiled'
        cp.build(self.project, package, 'profiled', 'Profiled')
        self.package = package
        self.mutate('manifest.json', lambda x: x['analysis_profile'].update(name='economics'))
        self.assertTrue(any('differs' in e for e in cp.validate_package(package)[0]))

    def test_profile_cannot_be_removed_only_from_manifest(self):
        self.declare_profile()
        package = self.root/'profiled'
        cp.build(self.project, package, 'profiled', 'Profiled')
        self.package = package
        self.mutate('manifest.json', lambda x: x.pop('analysis_profile'))
        self.assertTrue(any('both state and manifest' in e for e in cp.validate_package(package)[0]))

    def test_profiled_package_rejects_removed_method_outputs(self):
        self.declare_profile()
        package = self.root/'profiled'
        cp.build(self.project, package, 'profiled', 'Profiled')
        self.package = package
        self.mutate('reasoning_cards.json', lambda x: x[0].pop('expected_outputs'))
        self.assertTrue(any('requires expected_outputs' in e for e in cp.validate_package(package)[0]))
        with self.assertRaises(ValueError):
            cp.query(package, 'profiled::reasoning_cards::m1')

    def test_profile_cannot_be_removed_only_from_state(self):
        self.declare_profile()
        package = self.root/'profiled'
        cp.build(self.project, package, 'profiled', 'Profiled')
        self.package = package
        self.mutate('state.json', lambda x: x.pop('analysis_profile'))
        self.assertTrue(any('both state and manifest' in e for e in cp.validate_package(package)[0]))

    def test_working_validator_checks_declared_profile(self):
        import validate
        self.declare_profile('unknown')
        self.assertTrue(any('unsupported value' in e for e in validate.validate(self.project)[0]))
        self.declare_profile()
        cards = cp.load(self.project/'output/reasoning_cards.json')
        cards[0].pop('expected_outputs')
        cp.dump(self.project/'output/reasoning_cards.json', cards)
        self.assertTrue(any('requires expected_outputs' in e for e in validate.validate(self.project)[0]))

    def declare_faithful(self, critique=False):
        state_path = self.project/'output/state.json'
        state = cp.load(state_path)
        state['extraction_mode'] = 'faithful_with_critique' if critique else 'faithful'
        if critique:
            state['critique_authorization'] = 'User requests a separate arithmetic and method critique.'
        cp.dump(state_path, state)
        anchor = 'Compare the invoice currency with the payment currency before judging exposure.'
        (self.project/'corpus/source.txt').write_text('Speaker A: ' + anchor + '\n')
        for name in ('episodes', 'opinions', 'reasoning_cards', 'data_requirements'):
            items = cp.load(self.project/'output'/(name + '.json'))
            for item in items:
                item['source_refs'] = [{'source_id': 's1', 'locator': 'anchor: ' + anchor}]
            cp.dump(self.project/'output'/(name + '.json'), items)
        graph = cp.load(self.project/'output/graph.json')
        graph['nodes'][0]['source_refs'] = [{'source_id': 's1', 'locator': 'anchor: ' + anchor}]
        cp.dump(self.project/'output/graph.json', graph)
        cards = cp.load(self.project/'output/reasoning_cards.json')
        cards[0].update(method_origin='DOCUMENTED', attributed_to='Speaker A',
                        documentation_gaps=['No numerical threshold or competing hypothesis is documented.'],
                        operational_readiness='DOCUMENTED_FRAGMENT',
                        competing_hypotheses=['NOT_DOCUMENTED'], discrimination_test='NOT_DOCUMENTED',
                        abstention_conditions=['NOT_DOCUMENTED'],
                        source_vs_inference={'source': anchor, 'investigator': 'Organized the stated comparison. No added procedure.'})
        cards[0]['ordered_steps'] = [{'order': 1, 'action': anchor, 'readiness': 'KNOWLEDGE_ONLY',
                                     'evidence_basis': 'STATED', 'evidence_ref_indexes': [0]}]
        cp.dump(self.project/'output/reasoning_cards.json', cards)

    def build_faithful(self):
        self.package = self.root/'faithful'
        return cp.build(self.project, self.package, 'faithful', 'Documented speaker comparison')

    def test_faithful_fragment_survives_relocation_without_completion(self):
        self.declare_faithful()
        self.build_faithful()
        relocated = self.root/'moved-faithful'
        shutil.move(str(self.package), str(relocated))
        shutil.rmtree(self.project)
        self.assertEqual(cp.validate_package(relocated), ([], []))
        result = cp.query(relocated, 'faithful::reasoning_cards::m1', True)
        self.assertEqual(result['record']['attributed_to'], 'Speaker A')
        self.assertEqual(result['record']['record_class'], 'source_statement')
        self.assertEqual(result['record']['operational_readiness'], 'DOCUMENTED_FRAGMENT')
        self.assertEqual(result['record']['discrimination_test'], 'NOT_DOCUMENTED')
        self.assertEqual(result['record']['ordered_steps'][0]['evidence_ref_indexes'], [0])
        self.assertIn('invoice currency', result['evidence'][0]['quote'])
        self.assertFalse((relocated/'critique.json').exists())
        self.assertEqual(cp.load(relocated/'manifest.json')['extraction_mode'], 'faithful')

    def test_legacy_mode_is_not_invented(self):
        self.assertNotIn('extraction_mode', cp.load(self.package/'manifest.json'))
        self.assertEqual(cp.query(self.package, self.gid)['record']['record_class'], 'investigator_proposal')

    def test_critique_is_separate_indexed_and_queryable(self):
        self.declare_faithful(critique=True)
        critique = [{'id': 'c1', 'episode_id': 'e1', 'kind': 'METHOD_PROPOSAL',
                     'assessment': 'Investigator proposes a documented exposure inventory. Not the speaker method.',
                     'source_refs': cp.load(self.project/'output/reasoning_cards.json')[0]['source_refs']}]
        cp.dump(self.project/'output/critique.json', critique)
        self.build_faithful()
        relocated = self.root/'moved-critique'
        shutil.move(str(self.package), str(relocated))
        self.assertEqual(cp.validate_package(relocated), ([], []))
        manifest = cp.load(relocated/'manifest.json')
        self.assertEqual(manifest['routes']['investigator_critique'], 'critique.json')
        result = cp.query(relocated, 'faithful::critique::c1', True)
        self.assertEqual(result['record']['record_class'], 'investigator_proposal')
        self.assertTrue(result['evidence'])
        self.assertEqual(cp.query(relocated, 'faithful::reasoning_cards::m1')['record']['ordered_steps'][0]['evidence_basis'], 'STATED')

    def test_critique_refused_without_explicit_mode(self):
        cp.dump(self.project/'output/critique.json', [])
        with self.assertRaisesRegex(ValueError, 'Critique requires'):
            self.build_faithful()
        self.assertFalse(self.package.exists())

    def test_critique_refused_in_faithful_mode_even_when_empty(self):
        self.declare_faithful()
        cp.dump(self.project/'output/critique.json', [])
        with self.assertRaisesRegex(ValueError, 'Critique requires'):
            self.build_faithful()

    def test_critique_requires_nonblank_authorization(self):
        self.declare_faithful(critique=True)
        state = cp.load(self.project/'output/state.json')
        state['critique_authorization'] = ' '
        cp.dump(self.project/'output/state.json', state)
        with self.assertRaisesRegex(ValueError, 'critique_authorization'):
            self.build_faithful()

    def test_invalid_extraction_modes_are_refused(self):
        for mode in (None, '', 'improve', 1):
            state = cp.load(self.project/'output/state.json')
            state['extraction_mode'] = mode
            cp.dump(self.project/'output/state.json', state)
            with self.assertRaisesRegex(ValueError, 'extraction_mode'):
                self.build_faithful()

    def test_mode_drift_refused_with_updated_hashes(self):
        self.declare_faithful()
        self.build_faithful()
        self.mutate('manifest.json', lambda x: x.pop('extraction_mode'))
        self.assertTrue(any('Fidelity metadata differs' in e for e in cp.validate_package(self.package)[0]))

    def test_unauthorized_critique_refused_after_resealing(self):
        self.declare_faithful(critique=True)
        cp.dump(self.project/'output/critique.json', [])
        self.build_faithful()
        self.mutate('state.json', lambda x: x.pop('critique_authorization'))
        self.mutate('manifest.json', lambda x: x.pop('critique_authorization'))
        self.assertTrue(any('critique_authorization' in e for e in cp.validate_package(self.package)[0]))

    def test_proposed_steps_cannot_be_labeled_documented(self):
        self.declare_faithful()
        path = self.project/'output/reasoning_cards.json'
        cards = cp.load(path)
        cards[0]['ordered_steps'][0]['evidence_basis'] = 'INVESTIGATOR_PROPOSAL'
        cp.dump(path, cards)
        with self.assertRaisesRegex(ValueError, 'evidence_basis'):
            self.build_faithful()

    def test_step_reference_must_resolve(self):
        self.declare_faithful()
        path = self.project/'output/reasoning_cards.json'
        for indexes in ([], [-1], [1], [True], ['0']):
            cards = cp.load(path)
            cards[0]['ordered_steps'][0]['evidence_ref_indexes'] = indexes
            cp.dump(path, cards)
            with self.assertRaisesRegex(ValueError, 'evidence_ref_indexes'):
                self.build_faithful()

    def test_faithful_methods_require_origin_attribution_and_gaps(self):
        for field in ('method_origin', 'attributed_to', 'documentation_gaps'):
            self.declare_faithful()
            path = self.project/'output/reasoning_cards.json'
            cards = cp.load(path)
            cards[0].pop(field)
            cp.dump(path, cards)
            with self.assertRaises(ValueError):
                self.build_faithful()

    def test_faithful_methods_cannot_retain_proposal_class(self):
        self.declare_faithful()
        path = self.project/'output/reasoning_cards.json'
        cards = cp.load(path)
        cards[0]['record_class'] = 'investigator_proposal'
        cp.dump(path, cards)
        with self.assertRaisesRegex(ValueError, 'source_statement'):
            self.build_faithful()

    def test_working_validator_checks_fidelity(self):
        import validate
        self.declare_faithful()
        path = self.project/'output/reasoning_cards.json'
        cards = cp.load(path)
        cards[0]['ordered_steps'][0]['evidence_ref_indexes'] = [90]
        cp.dump(path, cards)
        self.assertTrue(any('evidence_ref_indexes' in e for e in validate.validate(self.project)[0]))

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
