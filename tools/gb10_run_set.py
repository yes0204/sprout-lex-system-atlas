"""GB10 실행 폴더(private-export/…) → runs-review.json 의 run_sets 한 건으로 추가/교체한다.

  python tools/gb10_run_set.py --folder E:/…/gb10-p2-service-261107 --id G-1107-gb10-p2 \
      --label "GB10 P2 — 선택/설명 2×2 × 3회" --what "…" --verdicts verdicts.json [--latest]

- 원자료(actual_N.json · plan.json)에서 일시 · 칸별 모델 · 실행 위치 · 단계별 멈춘 곳을 계산한다.
- 질문 원문은 plan 의 고정 질문(지어낸 개발 질문)만 쓴다. 근거 원문 · 사규 · 키는 넣지 않는다.
- verdicts.json(선택): {"<질문id>|<arm>": {"verdict": "…", "ok": true, "source": "…"}} — 독립 판정(Robert)을 붙인다.
"""
import argparse
import collections
import datetime
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KST = datetime.timezone(datetime.timedelta(hours=9))
LOC = {'small': '이 PC 로컬 Ollama(RTX 4060 Ti 8GB)', 'large': 'GB10 원격(사내 VPN · llama.cpp llama-server)'}
SERVICE = '서비스 로직: 이 PC 격리 프로세스(127.0.0.1:8359 · 운영 아님)'


def kst(ts):
    return datetime.datetime.fromtimestamp(ts, KST).strftime('%Y-%m-%d %H:%M')


def roles(plan, arm):
    s, l = plan['model_small'], plan['model_large']
    pick = {'S': ('small', s), 'L': ('large', l)}
    if arm in ('SS', 'SL', 'LS', 'LL'):
        return pick[arm[0]], pick[arm[1]]
    if 'LL' in str(plan.get('model_roles', '')):
        return pick['L'], pick['L']
    return pick['S'], pick['S']


def outcome(a):
    r = a.get('response') or {}
    se = r.get('source_explanation') or {}
    ex = se.get('experimental_explanation') or {}
    scores = [s['score'] for s in a.get('search', []) if isinstance(s.get('score'), (int, float))]
    score = max(scores) if scores else None
    posts = sum(1 for p in a.get('posts', []) if (p.get('observed') or {}).get('actual_posts'))
    st = {'질문': '통과', '검색': '통과', '원문·자격': '통과', '모델': '통과',
          'HTTP': '통과' if a.get('status') == 200 else '오류'}
    if r.get('answer_method') == 'boundary':
        st.update({'검색': '멈춤', '원문·자격': '도달 안 함', '모델': '도달 안 함'})
        where = '검색(최고점 %.3f < 0.45)' % score if score is not None else '검색'
    elif se.get('reason') == 'publication_integrity_not_verified':
        st.update({'원문·자격': '멈춤', '모델': '도달 안 함'})
        where = '원문·자격(공급 무결성 미확인)'
    elif se.get('reason') == 'model_proposed_needs_context':
        st['모델'] = '멈춤'
        where = '선택 모델이 확인 질문(needs_context)'
    elif ex.get('outcome') == 'explained':
        where = '끝까지 감(설명 검사 통과)'
    elif ex.get('outcome') == 'rejected':
        st['모델'] = '오류: 설명 검사 거부'
        where = '설명 검사 거부(%s)' % (ex.get('reason') or ex.get('rejection_reason'))
    elif ex.get('outcome') == 'abstained':
        st['모델'] = '멈춤'
        where = '설명 모델 보류(근거 부족)'
    else:
        st['모델'] = '멈춤'
        where = '모델 단계(세부 미기록)'
    sec = (a.get('finished') or 0) - (a.get('started') or 0)
    return st, where, posts, sec


def main():
    ap = argparse.ArgumentParser()
    for k in ('folder', 'id', 'label', 'what'):
        ap.add_argument('--' + k, required=True)
    ap.add_argument('--verdicts')
    ap.add_argument('--evaluation', default='')
    ap.add_argument('--status', default='완료')
    ap.add_argument('--latest', action='store_true')
    a = ap.parse_args()
    folder = Path(a.folder)
    plan = json.loads((folder / 'plan.json').read_text(encoding='utf-8'))
    qtext = {r['id']: r['request']['question'] for r in plan['runs']}
    verdicts = json.loads(Path(a.verdicts).read_text(encoding='utf-8')) if a.verdicts else {}
    acts = sorted(folder.glob('actual_*.json'), key=lambda p: int(re.findall(r'\d+', p.stem)[0]))
    groups = collections.OrderedDict()
    starts, ends, http200, posts_total = [], [], 0, 0
    for p in acts:
        x = json.loads(p.read_text(encoding='utf-8'))
        st, where, posts, sec = outcome(x)
        groups.setdefault((x['case_id'], x['arm']), []).append((st, where, posts, sec, x.get('status')))
        starts.append(x.get('started') or 0)
        ends.append(x.get('finished') or 0)
        http200 += x.get('status') == 200
        posts_total += posts
    cells = []
    for arm in dict.fromkeys(k[1] for k in groups):
        (sk, sm), (ek, em) = roles(plan, arm)
        cells.append({'arm': arm, 'selection_model': sm, 'selection_location': LOC[sk],
                      'explanation_model': em, 'explanation_location': LOC[ek]})
    rows = []
    for (qid, arm), items in groups.items():
        c = collections.Counter(w for _, w, _, _, _ in items)
        v = verdicts.get('%s|%s' % (qid, arm), {})
        (_, sm), (_, em) = roles(plan, arm)
        rows.append({'id': qid, 'group': '%s · 선택 %s / 설명 %s' % (arm, sm, em), 'question': qtext.get(qid, ''),
                     'stopped_at': ' · '.join(('%s %d회' % (w, n)) if len(items) > 1 else w for w, n in c.items()),
                     'stages': items[0][0], 'http': items[0][4], 'model_posts': sum(i[2] for i in items),
                     'seconds': round(sum(i[3] for i in items) / len(items), 1),
                     'why_stopped': ' · '.join('%s: %d/%d' % (w, n, len(items)) for w, n in c.items()),
                     'why_source': '원자료 actual_N.json(이 PC private-export)에서 계산',
                     'independent_verdict': v.get('verdict', '판정 대기'), 'goal_met': bool(v.get('ok')),
                     'note': v.get('source', '')})
    valid = [s for s in starts if s]
    at = ('%s ~ %s KST' % (kst(min(valid)), kst(max(ends))[11:])) if valid else '진행 중'
    run = {'id': a.id, 'label': a.label, 'period': 'latest' if a.latest else 'past', 'status': a.status,
           'evidence_class': '실제 검색 · 실제 자격 검사 · 실제 모델(칸별) · 실제 HTTP', 'at': at,
           'run_conditions': {'service': SERVICE, 'cells': cells,
                              'settings': '온도 %s · ctx %s · 출력 %s · 재시도 %s · 직렬' % (
                                  plan.get('temperature'), plan.get('context_tokens'), plan.get('output_tokens'),
                                  plan.get('retry_limit'))},
           'code_pin': str(plan.get('code_pin', ''))[:9], 'result_pin': '', 'denominator': len(acts),
           'http_200': http200, 'model_posts': posts_total, 'embedding_calls': None,
           'what_changed': a.what, 'environment': SERVICE + ' · 모델 위치는 「실행 조건」 표',
           'independent_evaluation': ({'by': 'Robert', 'positive_answered': '—', 'boundary_minimum_hold': '—',
                                       'missing_condition_resolved': '—', 'status': a.evaluation}
                                      if a.evaluation else None),
           'rows': rows, 'source': 'plan %s · 폴더 %s' % (plan.get('phase'), folder.name)}
    path = ROOT / 'runs-review.json'
    d = json.loads(path.read_text(encoding='utf-8'))
    d['run_sets'] = [r for r in d['run_sets'] if r['id'] != a.id]
    if a.latest:
        for r in d['run_sets']:
            r['period'] = 'past'
    d['run_sets'].append(run)
    d['updated_at'] = datetime.datetime.now(KST).strftime('%Y-%m-%dT%H:%M+09:00')
    path.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    (ROOT / 'runs-review-data.js').write_text('/* 기계 생성 — runs-review.json 에서 만든다. 직접 고치지 않는다. */\n'
                                              'window.RUNS_REVIEW = ' + json.dumps(d, ensure_ascii=False) + ';\n',
                                              encoding='utf-8')
    print(a.id, at, len(rows), 'rows', http200, 'http200', posts_total, 'posts')


if __name__ == '__main__':
    main()
