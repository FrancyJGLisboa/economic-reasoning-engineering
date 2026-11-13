#!/usr/bin/env python3
"""Structural and source-anchor validation, not economic fact-checking."""
import argparse, json, re, sys
from pathlib import Path

REQUIRED = ("sources","episodes","opinions","reasoning_cards","data_requirements","reviews","graph","state")
ARRAYS = set(REQUIRED) - {"graph","state"}

def validate(project=None):
    project=Path(project or Path.cwd()).resolve()
    out=project/"output"
    if (out/"manifest.json").is_file():
        from context_package import validate_package
        return validate_package(out)
    errors=[]; warnings=[]; data={}
    for name in REQUIRED:
        p=out/f"{name}.json"
        if not p.is_file():
            errors.append(f"missing {p}"); continue
        try: data[name]=json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError) as e: errors.append(f"invalid {name}: {e}")
    for name in ARRAYS:
        if name in data and not isinstance(data[name],list): errors.append(f"{name} must be list")
    graph=data.get("graph",{})
    if not isinstance(graph,dict): errors.append("graph must be object"); graph={}
    for field in ("nodes","edges"):
        if not isinstance(graph.get(field),list): errors.append(f"graph.{field} must be list")
    state=data.get("state",{})
    if not isinstance(state,dict) or state.get("status") not in ("BLOCKED","PARTIAL","COMPLETE","STOPPED"):
        errors.append("invalid state.status")
    ids={}
    for name in list(ARRAYS)+["nodes","edges"]:
        items=graph.get(name,[]) if name in ("nodes","edges") else data.get(name,[])
        if not isinstance(items,list): continue
        key="source_id" if name=="sources" else "id"
        seen=set()
        for i,item in enumerate(items):
            if not isinstance(item,dict): errors.append(f"{name}[{i}] not object"); continue
            v=item.get(key)
            if not isinstance(v,str) or not v.strip(): errors.append(f"{name}[{i}] missing {key}")
            elif v in seen: errors.append(f"duplicate {name} id {v}")
            else: seen.add(v)
        ids[name]=seen
    for i,edge in enumerate(graph.get("edges",[]) if isinstance(graph.get("edges"),list) else []):
        if not isinstance(edge,dict): continue
        for key in ("from","to"):
            if edge.get(key) not in ids.get("nodes",set()): errors.append(f"edge[{i}] bad {key}")
    source_ids=ids.get("sources",set())
    corpus_files=sorted(p for p in (project/"corpus").rglob("*") if p.is_file() and p.suffix.lower() in (".txt",".md")) if (project/"corpus").exists() else []
    corpus_text="\n".join(p.read_text(encoding="utf-8",errors="replace") for p in corpus_files)
    sources_by_id={x.get("source_id"):x for x in data.get("sources",[]) if isinstance(x,dict)} if isinstance(data.get("sources"),list) else {}
    for name in ("episodes","opinions","reasoning_cards","nodes","edges"):
        items=graph.get(name,[]) if name in ("nodes","edges") else data.get(name,[])
        if not isinstance(items,list): continue
        for i,item in enumerate(items):
            if not isinstance(item,dict): continue
            source_refs=item.get("source_refs")
            if not isinstance(source_refs,list) or not source_refs:
                if name in ("nodes","edges") and item.get("evidence_status")=="UNSUPPORTED":
                    continue
                errors.append(f"{name}[{i}] requires non-empty source_refs")
                continue
            for ref in source_refs:
                if not isinstance(ref,dict) or ref.get("source_id") not in source_ids:
                    errors.append(f"{name}[{i}] unknown source"); continue
                locator=ref.get("locator","")
                if not locator: errors.append(f"{name}[{i}] missing locator")
                if not isinstance(locator,str):
                    errors.append(f"{name}[{i}] locator must be text"); continue
                match=re.search(r"anchor:\s*(.+)$",locator)
                reference_text=corpus_text
                filename=sources_by_id.get(ref.get("source_id"),{}).get("filename")
                if isinstance(filename,str) and filename:
                    source_path=Path(filename)
                    if not source_path.is_absolute(): source_path=project/source_path
                    if source_path.is_file() and source_path.suffix.lower() in (".txt",".md"):
                        reference_text=source_path.read_text(encoding="utf-8",errors="replace")
                    else:
                        reference_text=""
                elif match:
                    warnings.append(f"{name}[{i}] anchor checked against combined corpus, not a source-specific file")
                if match and not reference_text:
                    errors.append(f"{name}[{i}] anchor cannot be checked: source text unavailable")
                elif match and match.group(1).strip() not in reference_text:
                    errors.append(f"{name}[{i}] anchor not in corpus: {match.group(1)}")
                elif not match: warnings.append(f"{name}[{i}] no machine-checkable anchor")
    cards=data.get("reasoning_cards",[])
    if isinstance(cards,list):
        methods={}
        for card in cards:
            if not isinstance(card,dict): continue
            method=card.get("method_candidate","").strip()
            if method: methods.setdefault(method,[]).append(card.get("id","?"))
        for method, card_ids in methods.items():
            if len(card_ids)>1: warnings.append(f"duplicate method text in {len(card_ids)} cards: {', '.join(card_ids)}")
    episodes=data.get("episodes")
    if isinstance(state,dict) and state.get("status")=="COMPLETE":
        if not isinstance(episodes,list) or not any(isinstance(ep,dict) and ep.get("status")=="ACCEPTED" for ep in episodes):
            errors.append("COMPLETE requires at least one ACCEPTED episode; use BLOCKED or STOPPED for empty results")
    for name in ("opinions","reasoning_cards","data_requirements"):
        items=data.get(name,[])
        if not isinstance(items,list):continue
        for i,item in enumerate(items):
            if isinstance(item,dict) and "episode_id" in item and item["episode_id"] not in ids.get("episodes",set()):
                errors.append(f"{name}[{i}] unknown episode_id")
    if isinstance(state,dict) and 'analysis_profile' in state and isinstance(cards,list):
        if all(isinstance(card,dict) for card in cards):
            from context_package import profile_checks
            errors.extend(profile_checks({'state': state, 'reasoning_cards': cards}))
    if isinstance(state,dict) and isinstance(cards,list):
        from context_package import fidelity_checks
        fidelity_data = {'state': state, 'reasoning_cards': cards}
        if (out/'critique.json').is_file():
            try:
                fidelity_data['critique'] = json.loads((out/'critique.json').read_text(encoding='utf-8'))
            except (OSError, ValueError) as exc:
                errors.append('Invalid critique: ' + str(exc))
        errors.extend(fidelity_checks(fidelity_data))
    return errors,warnings

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group()
    group.add_argument("--project",type=Path,help="Working project containing corpus/ and output/. Defaults to current directory.")
    group.add_argument("--output",type=Path,help="Compatibility alias for a project output directory named output.")
    args=parser.parse_args()
    if args.output and args.output.resolve().name!="output":
        parser.error("--output must name the project output directory named output; use --project otherwise")
    project=args.output.resolve().parent if args.output else args.project
    errors,warnings=validate(project)
    for warning in warnings: print("WARNING:",warning)
    for error in errors: print("ERROR:",error)
    print("PASS — structural/anchor checks only" if not errors else "FAIL — structural/anchor checks")
    sys.exit(bool(errors))
