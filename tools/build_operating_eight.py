"""Render actual operating results separately from same-response guard checks."""
import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def build():
    d=json.loads((ROOT/'operating-eight-2026-11-21.json').read_text(encoding='utf8'))
    assert len(d['rows'])==8 and d['api_requests']==8 and not d['causal']
    e=lambda value: html.escape(value).replace('\n','&#10;')
    out=['<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
    '<title>회사 업무 8질문 · 운영 답변 재확인</title>',
    '<style>body{max-width:1040px;margin:40px auto;padding:0 24px;background:white;color:#252b28;font:17px/1.85 system-ui,sans-serif}h1{font-size:2rem;line-height:1.4}h2{font-size:1.35rem}a{color:#215c48}.lead{font-size:1.15rem}.note{background:#f0f5f1;padding:20px;border-left:4px solid #527664}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:24px 0}.metric{border-top:2px solid #527664;padding-top:10px}.metric strong{font-size:2.2rem;display:block}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}.answer{white-space:pre-wrap;overflow-wrap:anywhere;font:16px/1.9 Georgia,"Noto Serif KR",serif}section{margin:48px 0;padding-top:12px;border-top:1px solid #ccc}summary{cursor:pointer;font-weight:600}details{margin:16px 0}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:12px 8px;border-bottom:1px solid #ddd}small{color:#55625a}code{overflow-wrap:anywhere}@media(max-width:700px){body{padding:0 16px;margin-top:20px}.pair{grid-template-columns:1fr}.metrics{gap:8px}.metric strong{font-size:1.8rem}h1{font-size:1.65rem}table{font-size:14px}th,td{padding:8px 4px}}</style>',
    '<a href="index.html#tab=kanban">← 기존 진행보드</a><h1>실제로 다시 물어보니,<br>설명은 나오지만 빈틈도 남아 있습니다.</h1>',
    '<p class="lead">11월 21일 운영 서버에서 회사 업무 질문 8개를 검색부터 답변까지 한 번씩 실행했습니다. HTTP 성공 8건을 정답 8건으로 세지 않았습니다.</p>',
    '<div class="metrics"><div class="metric"><strong>6 / 8</strong>일반 원칙 설명 전달</div><div class="metric"><strong>1 / 8</strong>개인정보 포함 여부 확인</div><div class="metric"><strong>1 / 8</strong>설명 검증에서 보류</div></div>',
    '<div class="note"><strong>확인된 진전</strong><p>새 급여 업무 질문에서 고객사의 감독과 퇴사자 접근권한 회수를 함께 설명했습니다. 연락처 활용 질문에서는 공공기관 한정 단서도 보존했습니다.</p><strong>이번에 다시 드러난 문제</strong><p>계정 공유 답변에 적용 범위를 넓힌 문장 5개, 병원 질문에 감독 설명 누락, 비개인정보 오류 로그 질문에 설명 보류가 남았습니다.</p></div>',
    '<p><a href="#repair">이번 검사 수정 전후 ↓</a> · <a href="#limits">비교 범위와 한계 ↓</a></p>',
    '<table><thead><tr><th>질문</th><th>실제 결과</th></tr></thead><tbody>']
    for i,r in enumerate(d['rows'],1):
        out.append('<tr><td><a href="#q'+str(i)+'">'+e(r['title'])+'</a></td><td>'+e(r['status'])+'</td></tr>')
    out+=['</tbody></table><section id="repair"><h2>이번 수정: 원문에 없는 행위까지 적용한다고 덧붙이지 않기</h2>',
    '<p>계정 공유 질문에 답하면서, 권한 변경·인증·기록 관리 원칙까지 모두 공유에 관한 규정이라고 연결했습니다. 해당 선택 원문에 없는 행위를 단정하는 마지막 문장만 제외하도록 보완했습니다.</p>',
    '<p><strong>'+e(d['candidate_status'])+'</strong> · 관련 시험 '+str(d['tests_passed'])+'개 통과. 아래는 실제 배달된 해설에 새 검사만 적용한 결과입니다. 모델이 새로 생성한 답변이나 전체 검증 재생은 아닙니다.</p>']
    for c in d['rows'][0]['action_only_recheck']:
        if c['changed']:
            out+=['<div class="pair"><article><h3>운영 답변의 해설</h3><div class="answer">'+e(c['before'])+'</div></article><article><h3>검사 보완 후 · 원칙 문장 그대로</h3><div class="answer">'+e(c['after'])+'</div></article></div>']
    out+=['</section>']
    for i,r in enumerate(d['rows'],1):
        out+=['<section id="q'+str(i)+'"><h2>'+str(i)+'. '+e(r['title'])+'</h2><p>'+e(r['question'])+'</p><p><strong>'+e(r['status'])+'</strong> — '+e(r['reading'])+'</p><p><small>운영 API '+str(r['seconds'])+'초 · 단회 · 자동 재시도 0</small></p>']
        if r['questions']:
            out+=['<div class="note">실제로 나온 질문: '+e(r['questions'][0]['text'])+'</div>']
        out+=['<details><summary>이번 실제 응답 전체 · 원문 인용 포함</summary><div class="answer">'+e(r['answer'] or '설명 없음 · 위 사실 확인 질문을 전달했습니다.')+'</div></details>']
        if r['before_answer']:
            out+=['<details><summary>이전에 보존한 같은 질문 답변 · 다른 실행</summary><div class="answer">'+e(r['before_answer'])+'</div></details>']
        else:out+=['<p><small>새로 작성한 질문입니다. 같은 질문의 이전 답변은 없습니다.</small></p>']
        out+=['</section>']
    out+=['<section id="limits"><h2>이 결과를 어떻게 읽어야 하나요?</h2><p>'+e(d['scope'])+'</p><p>과거 답변과는 운영 데이터·코드·모델 출력이 달라질 수 있어, 차이 전부를 이번 수정 효과로 돌리지 않습니다. 도중 화면 코드 배포로 원 실행을 멈춘 뒤, 답변 실행 코드의 전체 지문이 같은 것을 확인하고 미실행 6개만 이어갔습니다. 앞의 두 질문을 반복 호출하지 않았습니다.</p><p>답변 전달 수는 정답 수가 아닙니다. 법률 의미 전수 검수와 독립 평가가 완료된 결과도 아닙니다. 이번 수정은 선택 원문에 없는 행위의 좁은 표현 검사이며, 모든 추론을 판정하는 장치가 아닙니다.</p><p>다음 작업은 병원 질문의 누락이 공급·선택·검사 중 어디서 생겼는지 구분하고, 비개인정보 로그 질문의 보류 사유를 복원하는 것입니다. 같은 실패를 확인하려고 모델을 반복 호출하지 않습니다.</p><details><summary>결과 파일 · 확인 근거</summary><p>8요청 HTTP 200 · GPT 0 · 자동 재시도 0 · 각 실행 DB 전후 해시 동일. 운영 데이터 '+e(d['data_commit'][:9])+' · 수정 후보 '+e(d['candidate_commit'])+'.</p><a href="operating-eight-2026-11-21.json">질문·답변·응답 SHA·문장 재검사 JSON</a></details></section></html>']
    (ROOT/'operating-eight-2026-11-21.html').write_text('\n'.join(out)+'\n',encoding='utf8')

if __name__=='__main__':build()
