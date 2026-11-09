"""Render the two frozen, local Markdown reports without remote scripts."""
from pathlib import Path
import html, re

ROOT = Path(__file__).resolve().parents[1]
def inline(text):
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

def render(md):
    lines = md.splitlines(); output=[]; i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1; continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=lines[i].strip().strip('|').split('|')
                if not all(re.fullmatch(r'\s*:?-+:?\s*', c) for c in cells): rows.append(cells)
                i+=1
            output.append('<div class="table-wrap" tabindex="0" aria-label="비교표 · 좁은 화면에서는 가로로 이동"><table>')
            for j,row in enumerate(rows):
                tag='th' if j==0 else 'td'
                output.append('<tr>'+''.join(f'<{tag}>{inline(c.strip())}</{tag}>' for c in row)+'</tr>')
            output.append('</table></div>'); continue
        if line.startswith('#'):
            level=len(line)-len(line.lstrip('#')); output.append(f'<h{level}>{inline(line[level:].strip())}</h{level}>')
        elif line.startswith('- '):
            output.append('<ul>')
            while i<len(lines) and lines[i].startswith('- '): output.append('<li>'+inline(lines[i][2:])+'</li>'); i+=1
            output.append('</ul>'); continue
        elif re.match(r'^\d+\. ',line):
            output.append('<ol>')
            while i<len(lines) and re.match(r'^\d+\. ',lines[i]): output.append('<li>'+inline(re.sub(r'^\d+\. ','',lines[i]))+'</li>'); i+=1
            output.append('</ol>'); continue
        else: output.append('<p>'+inline(line)+'</p>')
        i+=1
    return '\n'.join(output)

def page(title,body):
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>'+title+'</title><link rel="stylesheet" href="reports.css"></head><body><header><a href="./">통합 보드</a><a href="reports.html">결과 보고</a><a href="runs-review.html">실행 기록</a><a href="atlas-browser.html">구조 데이터 열람</a><a href="./#tab=lexicon">개념·사전</a></header><main>'+body+'</main><footer>고정 기록 · 실시간 현황이나 운영 배포를 뜻하지 않습니다. 모델/API 호출 없는 읽기 화면입니다.</footer></body></html>'

for date in ['2026-11-07','2026-11-08']:
    md=(ROOT/f'report-{date}.md').read_text(encoding='utf-8-sig')
    note='기존 7일 보고의 본문을 변경하지 않고 읽기 화면으로 옮겼습니다. 작성 당시의 후속 상태도 그대로 보존합니다.' if date.endswith('07') else '11월 8일의 결과만 모았습니다. 작성일은 11월 9일이며, 9일 실험은 합산하지 않습니다.'
    body=f'<p class="eyebrow">DAILY REPORT / {date}</p><aside>{note} <a href="report-{date}.md" download>원문 Markdown 내려받기</a></aside>'+render(md)
    (ROOT/f'report-{date}.html').write_text(page(date+' 작업 결과 보고 · Sprout Lex',body),encoding='utf-8')

body='''<p class="eyebrow">ANNA / 작업 결과 보고</p><h1>무엇을 바꿨고,<br>답변은 얼마나 나아졌나</h1>
<p class="lead">실행 횟수나 검수 통과 수보다, 사용자의 질문에 맞는 답이 전달됐는지를 중심으로 읽는 일일 보고입니다.</p>
<section class="report-card"><p>2026.11.08 · 결과 보고</p><h2><a href="report-2026-11-08.html">회사 업무 질문으로 병목을 확인했습니다</a></h2><p>검색 힌트만으로 신규 도달은 늘지 않았습니다. 원문 공급을 일부 복구했지만 설명 보류와 확인 질문 손실이 남았습니다.</p><a href="report-2026-11-08.html">전후 비교 · 실패 원인 · 다음 개선 읽기 →</a></section>
<section class="report-card"><p>2026.11.07 · 기존 보고 보존</p><h2><a href="report-2026-11-07.html">실제 서비스 안에서 모델을 비교하기 시작했습니다</a></h2><p>선택·설명 모델 교체, 검색 보강, KG 문맥 시험을 모듈별로 정리한 기존 보고입니다. 본문과 당시 한계를 그대로 보존했습니다.</p><a href="report-2026-11-07.html">기존 7일 모듈별 보고 읽기 →</a></section>
<h2>누가 보드를 갱신하나</h2><dl><dt>Anna · 통합 책임</dt><dd>공통 화면, 작업 결과 보고, 작업 보드와 공개 반영을 맡습니다. 각 담당의 산출물을 사용자 관점의 결과로 묶습니다.</dd><dt>Sarah · 런리뷰·구조 현행화</dt><dd>실행 기록과 독립 판정, 아틀라스 구조 데이터·한 페이지 흐름도를 작성하고 갱신합니다.</dd><dt>James · 개념·사전</dt><dd>04 사전·범위 내용과 별도 관계 지도, 실험 결과 화면을 맡습니다. 공개 반영은 Anna와 결속합니다.</dd></dl>
<aside>날짜별 보고는 그날의 고정 기록입니다. 이후 수정으로 과거 실패를 덮지 않습니다. 아틀라스의 구조 스냅샷·런리뷰의 실행 기록·개념 등록 수는 서로 다른 자료이며, 어느 하나만으로 답변 품질이나 운영 반영을 증명하지 않습니다.</aside>'''
(ROOT/'reports.html').write_text(page('작업 결과 보고 · Sprout Lex',body),encoding='utf-8')
