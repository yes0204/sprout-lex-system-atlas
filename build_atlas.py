# -*- coding: utf-8 -*-
"""atlas.json — 아틀라스 단일 원천(엔티티·관계) 빌드 · 작성 Sarah 2026-11-08 (개정안 R2·R3)
읽는 것: data.js(처리 지도 노드·엣지), runs-review.json(단계·run_set·onepage), module-notes.json(모듈 메모 id)
쓰는 것: atlas.json(사람이 읽는 원천) · atlas-model.js(화면용 · 기계 생성)
규칙: 손으로 고치는 파일은 runs-review.json 의 onepage 와 data.js 뿐 — 이 스크립트는 둘을 합쳐 관계로 바꾼다.
truth: observed(관측) · pinned(코드 고정) · proposed(제안) · agreed(합의)
"""
import json, re, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = Path(__file__).parent

def load_js(path, prefix):
    s = path.read_text(encoding='utf8')
    i = s.index(prefix) + len(prefix)
    body = s[i:].strip().rstrip(';').strip()
    return json.loads(body)

A = load_js(HERE / 'data.js', 'window.ATLAS =')
R = json.loads((HERE / 'runs-review.json').read_text(encoding='utf8'))
try:
    M = json.loads((HERE / 'module-notes.json').read_text(encoding='utf8'))
except Exception:
    M = None
op = R['onepage']
ents, rels = [], []
def ent(kind, id_, title, **kw):
    e = dict(kind=kind, id=f'{kind}:{id_}', title=title); e.update(kw); ents.append(e); return e['id']
def rel(t, src, dst, **kw):
    r = dict(type=t, src=src, dst=dst); r.update(kw); rels.append(r)

code_pin = dict(commit=A['code_commit'], checked_at=A['checked_at'])
# 1) 처리 지도 노드 — pinned(코드 고정)
for n in A['nodes']:
    src = n.get('source') or {}
    ent('node', n['id'], n['title'], node_kind=n['kind'], summary=n.get('summary', ''),
        as_of=A['checked_at'][:10], truth='pinned',
        evidence=dict(commit=A['code_commit'], file=src.get('file'), line=src.get('line'), sha256=src.get('sha256')),
        link=f"index.html#node={n['id']}")
for a, b, label, kind in A['edges']:
    rel('flows_to' if kind == 'flow' else ('reads' if kind == 'data' else kind), f'node:{a}', f'node:{b}', label=label)
# 2) 실행 단계 — observed(관측)
for s in R['answer_flow']['stages']:
    meta = op['stage_meta'].get(s['id'], {})
    ent('stage', s['id'], s['name'], state=s.get('state'), goal=meta.get('goal'), ratio=meta.get('ratio'),
        as_of=(re.match(r'\d{4}-\d{2}-\d{2}', R['answer_flow'].get('as_of') or '') or re.match(r'.*', R['updated_at'][:10])).group(0), truth='observed',
        evidence=dict(run_sets=[r['id'] for r in R['run_sets'] if r.get('period') in ('latest',)], note=s.get('evidence', '')[:120]),
        link='runs-review.html')
    for nid in meta.get('modules', []):
        rel('observed_at', f'stage:{s["id"]}', f'node:{nid}')
    if meta.get('tobe'):
        tag = meta['tobe']['tag'].split(' ')[0]
        ent('change', f'{s["id"]}-{tag}', meta['tobe']['tag'], text=meta['tobe']['text'], as_of=op['as_of'], truth='proposed', evidence=dict(doc='261108_sarah_flow_asis_tobe.html'))
        rel('changes', f'change:{s["id"]}-{tag}', f'stage:{s["id"]}')
# 3) run_set — observed
for r in R['run_sets']:
    ent('run_set', r['id'], r['label'], at=r.get('at'), period=r.get('period'), evidence_class=r.get('evidence_class'),
        code_pin=r.get('code_pin'), as_of=(r.get('at') or '')[:10], truth='observed',
        evidence=dict(code_pin=r.get('code_pin'), http_200=r.get('http_200'), denominator=r.get('denominator')),
        link=f"runs-review.html#run={r['id']}")
    for s in R['answer_flow']['stages']:
        rel('measured_by', f'stage:{s["id"]}', f'run_set:{r["id"]}', weak=True)
# 4) 구조 모듈(한 페이지 4열) — node 가 있으면 pinned 를 상속, 없으면 agreed/proposed
for col in op['structure']:
    for m in col['modules']:
        mid = re.sub(r'[^0-9A-Za-z가-힣]+', '-', m['label']).strip('-')
        truth = 'pinned' if m.get('node') else ('proposed' if m.get('k') else 'agreed')
        ent('module', mid, m['label'], column=col['title'], desc=m['desc'], k=bool(m.get('k')), tag=m.get('tag'),
            as_of=op['as_of'], truth=truth,
            evidence=(dict(node=m['node'], commit=A['code_commit']) if m.get('node') else dict(doc='runs-review.json#onepage.structure')),
            link=m.get('link') or (f"index.html#node={m['node']}" if m.get('node') else 'index.html'))
        if m.get('node'):
            rel('implements', f'module:{mid}', f'node:{m["node"]}')
        for sid in m['stages']:
            rel('supports', f'module:{mid}', f'stage:{sid}')
# 5) 진행 track — agreed/proposed
for t in op['tracks']:
    ent('track', t['id'], t['title'], status=t['status'], desc=t['desc'], k=bool(t.get('k')), as_of=op['as_of'],
        truth='proposed' if t.get('k') else 'agreed', evidence=dict(run_set=t.get('run'), doc='261108_sarah_flow_asis_tobe.html'),
        link=f"runs-review.html#run={t['run']}" if t.get('run') else 'index.html#tab=kanban')
    for sid in t.get('stages', []):
        rel('changes', f'track:{t["id"]}', f'stage:{sid}')
    if t.get('run'):
        rel('measured_by', f'track:{t["id"]}', f'run_set:{t["run"]}')
# 6) 모듈 메모(담당 01-1~01-8) — observed(기록) · 상태 ok/weak/fail
if isinstance(M, dict):
    for m in M.get('modules', []):
        ent('note', m['id'], m.get('name', m['id']), role=m.get('role'), status=m.get('status'), latest=m.get('latest'),
            as_of=(M.get('updated_at') or op['as_of'])[:10], truth='observed', evidence=dict(doc='module-notes.json', source=m.get('source')), link='index.html')

ids = {e['id'] for e in ents}
bad = [r for r in rels if r['src'] not in ids or r['dst'] not in ids]
if bad:
    raise SystemExit('관계 끝점 미해소: ' + json.dumps(bad[:5], ensure_ascii=False))
out = dict(schema='atlas.model.v0', built_from=dict(data_js=A['code_commit'], runs_review_updated_at=R['updated_at']),
           truth_legend=dict(observed='실행 기록으로 관측', pinned='코드 커밋·파일에 고정', agreed='회의 합의 · 미착수', proposed='제안 · 그림자/Track K'),
           entities=ents, relations=rels,
           counts=dict(entities=len(ents), relations=len(rels), by_kind={k: sum(e['kind'] == k for e in ents) for k in sorted({e['kind'] for e in ents})},
                       by_truth={k: sum(e['truth'] == k for e in ents) for k in ('observed', 'pinned', 'agreed', 'proposed')}))
(HERE / 'atlas.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf8')
(HERE / 'atlas-model.js').write_text('/* 기계 생성 — build_atlas.py 가 atlas.json 에서 만든다. 직접 고치지 않는다. */\nwindow.ATLAS_MODEL = ' + json.dumps(out, ensure_ascii=False) + ';\n', encoding='utf8')
print(json.dumps(out['counts'], ensure_ascii=False))
