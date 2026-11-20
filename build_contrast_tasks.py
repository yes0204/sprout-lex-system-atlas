"""Human-facing actual comparison; generated response text stays unchanged."""
from pathlib import Path
import json,html

def esc(s):return html.escape(str(s)).replace('\n','&#10;')
def answer(label,text):return '<details><summary>'+esc(label)+'</summary><div class="answer">'+esc(text)+'</div></details>'
d=json.loads(Path('contrast-tasks-2026-11-20.json').read_text(encoding='utf8'))
lines=['<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
'<title>고객사 감독과 직원 관리를 나누어 답하기</title>',
'<style>body{max-width:860px;margin:32px auto;padding:0 20px;color:#222;background:white;font:18px/1.8 Georgia,serif}h1{font-size:30px}h2{font-size:23px}aside{padding:18px;background:#f4f3ee}details{border:1px solid #ddd;padding:12px;margin:12px 0}summary{cursor:pointer;font-weight:bold}.answer{white-space:pre-wrap;overflow-wrap:anywhere;font-size:16px}p,li{overflow-wrap:anywhere}@media(max-width:600px){body{font-size:16px}h1{font-size:25px}}</style>',
'<p><a href="./#tab=kanban">← 진행보드</a> · <a href="operating-business-2026-11-20.html">앞선 운영 7질문</a></p>',
'<h1>고객사 감독 근거를 찾아, 직원 관리와 함께 설명하도록 고쳤습니다</h1>',
'<aside><strong>바뀐 점:</strong> 두 업무를 비교하는 질문에서 먼저 나온 업무도 한 번 더 검색합니다. 기존 검색 순위는 그대로 두고, 원문 자격을 통과한 근거만 추가합니다. 고객사 감독을 빠뜨렸던 질문에서 이제 감독 의무와 직원 접근권한 관리가 함께 나왔습니다.</aside>',
'<p>11월 20일 · 기존 12입력의 원검색 결과 동일 · 실제 새 생성 3회 · 자동 재시도·GPT 0 · 관련 시험 998개 통과. 질문은 모두 합성한 회사 업무 사례입니다.</p>',
'<h2>확인한 개선과 남은 문제</h2><ul><li>고객사 감독 질문: 직원 관리만 설명하던 답변에 위탁자의 감독 원문과 설명이 추가됐습니다.</li><li>제조사 사례: 직원 교육·관리와 준용 원칙은 전달됐지만, 감독 설명을 모델이 잘못 분류해 보류했습니다.</li><li>유통회사 사례: 감독·내부 관리 원칙은 전달됐지만, 접근권한 설명의 준용 근거가 부족해 보류했습니다.</li></ul>',
'<p>원문 공급 개선이 모든 답변의 완성을 뜻하지는 않습니다. 새 두 질문은 개발자가 작성했으며 독립 평가용 비공개 문제는 아닙니다. 수정 전후의 생성 결과도 달라져 문장 차이를 전부 검색 효과로 단정하지 않습니다.</p>']
notes=['직원 관리만 다루던 답변에 고객사 감독 원칙이 추가됐습니다. 직접 비교할 수 있는 수정 전 답변이 있습니다.',
'다른 업종에서 새로 검증했습니다. 원문은 공급됐지만 모델이 직접 의무를 준용으로 분류해 감독 설명 2개가 보류됐습니다.',
'다른 업무에서 새로 검증했습니다. 감독과 내부 관리 원칙은 표시됐고, 접근권한에 관한 설명 1개는 연결 근거 부족으로 보류됐습니다.']
for i,(r,note) in enumerate(zip(d['rows'],notes),1):
 lines+=['<section id="case-'+str(i)+'"><h2>'+str(i)+'. '+['고객사 감독과 직원 권한 관리','제조사 점검과 유지보수 업체 직원 교육','유통회사 감독과 개발회사 접근권한 관리'][i-1]+'</h2>', '<p>'+esc(r['question'])+'</p><p>'+esc(note)+'</p>', '<p>검사를 통과한 설명 '+str(r['accepted'])+'개 · 보류 '+str(len(r['held']))+'개. 설명 수는 정답 점수가 아닙니다.</p>']
 if r['before_answer']:lines.append(answer('수정 전 운영 답변',r['before_answer']))
 lines.append(answer('수정 후 격리 실행에서 실제 전달된 답변',r['answer']))
 lines.append('</section>')
if d.get('operating'):
 o=d['operating'];lines+=['<h2>운영 반영 뒤 다시 확인</h2>','<p>회사 Git main → deploy '+esc(o['deployed_commit'][:9])+' 반영 후 두 질문을 새로 실행했습니다. 앞선 격리 결과를 운영 결과로 바꿔 적지 않았습니다.</p>']
 for r in o['rows']:
  lines.append('<p>'+esc(r['question'])+' · HTTP '+str(r['status'])+' · '+str(r['elapsed_seconds'])+'초</p>')
  lines.append(answer('운영 서버의 새 실제 답변',r['answer']))
if d.get('role_alias_recheck'):
 r=d['role_alias_recheck']
 lines+=['<h2>운영 새 답변에서 발견해 추가로 고친 역할 표현</h2><p>고객사를 위탁자로 괄호 안에 단정하는 표현이 다시 나왔습니다. 고객사·협력사 같은 회사 지칭도 검사하도록 고쳤습니다. 아래는 그 실제 답변 문장의 재검증이며 새 모델 생성이나 전체 응답 재실행은 아닙니다.</p>',answer('수정 전 실제 해설',r['original_explanation']),answer('같은 문장 재검증 — 원칙 유지·마지막 단정 제외',r['after'])]
lines+=['<details><summary>증거와 범위</summary><p>원문·질문을 새로 쓰지 않고 실제 전달 응답을 표시했습니다. 보류 원출력을 수락 답변으로 올리지 않았습니다. 원DB/색인/KG 교체 없음. 완전한 법률 의미 검수·모든 회사 질문의 정답 보장 아님.</p><p><a href="contrast-tasks-2026-11-20.json">질문별 답변과 해시 JSON</a></p></details>','</html>']
Path('contrast-tasks-2026-11-20.html').write_text('\n'.join(lines)+'\n',encoding='utf8')
