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
    esc = html.escape
    parts=[START, '<div class="wbs-current" aria-label="11월 16일 작업 계획">',
           '<h1>11/16 작업 WBS — 근거부터 실제 답변까지</h1>',
           '<p><strong>'+esc(d['baseline'])+'</strong></p>', '<p>'+esc(d['authority'])+'</p>',
           '<p>'+esc(d['status_note'])+'</p>',
           '<p>순서: T1·T2 병행 → T3 기준선 → T4·T6 구현 → T5 연결 → T7 평가 → T8 인수. 화면 틀과 검사 설계는 병행합니다.</p>',
           '<div class="wbs-grid">']
    for r in d['tasks']:
        parts += ['<article id="wbs-'+r['id']+'"><h2>'+r['id']+' '+esc(r['title'])+'</h2>',
                  '<p class="wbs-status">'+esc(r['status'])+' · 책임 '+esc(r['owner'])+'</p>',
                  '<p>'+esc(r['current'])+'</p>', '<details><summary>담당·선행 조건·완료 기준</summary><dl>']
        for key,label in [('partners','협업'),('depends','선행'),('output','산출물'),('acceptance','완료 기준')]:
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
