"""Render the dated WBS above the preserved 11/7 board; no network calls."""
import html
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
START, END = '<!-- WBS-1116-START -->', '<!-- WBS-1116-END -->'
def render():
    d = json.loads((ROOT/'wbs-2026-11-16.json').read_text(encoding='utf-8'))
    assert len(d['tasks']) == 8 and len({r['id'] for r in d['tasks']}) == 8
    c=d['completion']
    ids=c['complete']+c['partial']+c['latest_unconfirmed']
    assert len(ids)==8 and set(ids)=={r['id'] for r in d['tasks']}
    esc = html.escape
    parts=[START, '<div class="wbs-current" aria-label="회사 업무 질문 개선 현황">',
           '<h1>11/16 시작 작업 — 11/21 운영 재확인</h1>',
           '<div class="wbs-remaining"><h2>얼마나 남았나요?</h2><p><strong>8개 작업 묶음 중 '+str(len(c['complete']))+'개 완료 · '+str(len(c['partial']))+'개 부분 완료 · '+str(len(c['latest_unconfirmed']))+'개 최신 증거 확인 필요</strong></p><p>먼저 고칠 것: 고객사·질문자 혼동 → 빠진 감독 설명 → 오류 로그 답변 보류.<br>마감 전 확인: 다른 업무 재검증 · 새 정본과 KG 결속 · 전체 평가 인수.</p><small>'+esc(c['basis'])+'</small></div>',
           (ROOT/'improvement-summary.html').read_text(encoding='utf-8').strip(),
           '<p><strong>'+esc(d['baseline'])+'</strong></p>', '<p>'+esc(d['authority'])+'</p>',
           '<p>'+esc(d['status_note'])+'</p>',
           '<p>갱신: '+esc(d['updated_at'])+' · 실제 확인된 결과 기준</p>',
           '<p>진행 순서: '+esc(d['progress_order'])+'</p>',
           *['<p><strong>'+esc(x['title'])+'</strong> — '+esc(x['text'])+'</p>' for x in d['summary']],
           '<p><a href="operating-eight-2026-11-21.html">최신: 운영 8질문과 수정 뒤 새 답변 1건</a> · <a href="condition-scope-2026-11-20.html">이전: 조건 누락·행위 확장 검사 전후 6질문</a></p>',
           '<p><a href="operating-check-2026-11-20.html">운영 반영 후 실제 답변 2건 보기</a></p><p><a href="action-evidence-2026-11-20.html">회사 업무 질문 8건: 실제 답변과 남은 문제 보기</a> · <a href="compact-evidence-2026-11-20.html">원문 공급 개선 전후 6건 보기</a></p>',
           '<p>날짜별 실험과 운영 확인 결과는 각각의 실행 기록입니다. 서로 다른 분모를 합쳐 완료율이나 정답률을 계산하지 않습니다.</p>',
           '<div class="wbs-grid">']
    for r in d['tasks']:
        link=r.get('next_link')
        next_text=('<a href="'+esc(link['href'])+'">'+esc(link['label'])+'</a>'+esc(link['suffix'])) if link else esc(r['next'])
        parts += ['<article id="wbs-'+r['id']+'"><h2>'+r['id']+' '+esc(r['title'])+'</h2>',
                  '<p class="wbs-status">'+esc(r['status'])+' · 책임 '+esc(r['owner'])+'</p>',
                  '<p><strong>왜 하나요?</strong> '+esc(r['benefit'])+'</p>', '<p><strong>지금까지</strong> '+esc(r['current'])+'</p>', '<p><strong>다음 작업</strong> '+next_text+'</p>', '<p><strong>완료 기준</strong> '+esc(r['acceptance'])+'</p>', '<details><summary>협업 담당 · 기술 기록</summary><dl>']
        for key,label in [('partners','협업'),('depends','선행'),('output','산출물'),('technical_note','기술 산출물')]:
            parts += ['<dt>'+label+'</dt><dd>'+esc(r[key])+'</dd>']
        parts += ['</dl></details></article>']
    parts += ['</div><details><summary>확인 근거 · 공개 가능한 기록만</summary><ul>']
    parts += ['<li><a href="'+esc(u)+'">기록 '+str(i+1)+'</a></li>' for i,u in enumerate(d['sources'])]
    parts += ['</ul></details></div>',END]
    block='\n'.join(parts)
    p=ROOT/'index.html'; s=p.read_text(encoding='utf-8')
    if START in s:
        s=s[:s.index(START)]+block+s[s.index(END)+len(END):]
    else:
        begin=s.index('<section id="kanban-view"'); content=s.index('>',begin)+1
        depth=1; close=None
        for m in re.finditer(r'</?section\b[^>]*>',s[content:]):
            depth += -1 if m.group().startswith('</') else 1
            if depth == 0:
                close=content+m.start(); break
        assert close is not None
        old=s[content:close].replace('지금 무엇을 하고 있나','11/7 작업 기록 — 현재 상태 아님')
        s=s[:content]+'\n'+block+'\n<details class="wbs-archive"><summary>11/7 이전 보드 보관 · 갱신 중단</summary>'+old+'</details>\n'+s[close:]
        s=s.replace('</head>','<link rel="stylesheet" href="wbs.css">\n</head>')
    p.write_text(s,encoding='utf-8',newline='\n')
if __name__ == '__main__': render()
