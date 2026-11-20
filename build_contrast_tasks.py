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
'<h1>고객사 감독 근거를 찾아, 직원 관리와 함께 설명하도록 고쳤습니다</h1><p><a href="#final-operating">최종 운영 답변으로 바로 가기 ↓</a> · <a href="#citation-owner">인용 경고 수정 전후 ↓</a></p>',
'<aside><strong>바뀐 점:</strong> 두 업무를 비교하는 질문에서 먼저 나온 업무도 한 번 더 검색합니다. 기존 검색 순위는 그대로 두고, 원문 자격을 통과한 근거만 추가합니다. 고객사 감독을 빠뜨렸던 질문에서 이제 감독 의무와 직원 접근권한 관리가 함께 나왔습니다.</aside>',
'<p>11월 20일 초기 비교 기록 · 기존 12입력의 원검색 결과 동일 · 실제 새 생성 3회 · 자동 재시도·GPT 0 · 관련 시험 998개 통과. 질문은 모두 합성한 회사 업무 사례입니다.</p>',
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
if d.get('final_operating_ui'):
 f=d['final_operating_ui']
 lines+=['<h2>앞선 9c329c04d 운영 확인 기록</h2><p>운영 '+esc(f['deployed_commit'][:9])+' · 전체 회귀 1,006개 통과 · 고정 응답 14입력 재검증. 고객사 역할 단정 수정 뒤 운영 화면에서 같은 질문을 한 번 더 실행했습니다.</p><p>감독·직원 권한 관리 원칙이 함께 나왔고, 법적 역할을 단정한 뒷문장 1개가 실제로 제외됐습니다. 아래는 화면에서 읽어 보존한 답변입니다. HTTP 원응답·토큰 기록으로 대신 표기하지 않았습니다.</p>',answer('최종 운영 화면의 실제 답변',f['answer']),'<p>당시 발견한 문제: 준용 조문 열거를 인용 검사기가 별도 인용으로 읽으면서 미확인 경고 61개를 표시했습니다. 경고를 숨기거나 검증 완료로 바꾸지 않았습니다. 후속 인용 검사 수정 결과는 아래에 따로 기록했습니다.</p>']
if d.get('operating'):
 o=d['operating'];lines+=['<h2>운영 반영 뒤 다시 확인</h2>','<p>회사 Git main → deploy '+esc(o['deployed_commit'][:9])+' 반영 후 두 질문을 새로 실행했습니다. 앞선 격리 결과를 운영 결과로 바꿔 적지 않았습니다.</p>']
 for r in o['rows']:
  lines.append('<p>'+esc(r['question'])+' · HTTP '+str(r['status'])+' · '+str(r['elapsed_seconds'])+'초</p>')
  lines.append(answer('운영 서버의 새 실제 답변',r['answer']))
if d.get('citation_owner_release'):
 c=d['citation_owner_release']
 lines+=['<section id="citation-owner"><h2>인용 경고: 답변을 바꾸지 않고, 무엇이 미확인인지 구분했습니다</h2><aside><strong>같은 원응답 비교:</strong> 한 교육 사례에서 소속 법령을 못 찾던 인용 경고가 61개 → 0개로 줄었습니다. 실제 답변과 출처는 그대로입니다. <strong>답변 근거 연결 미확인 27개는 그대로 남겼습니다.</strong></aside><p>원문에 있는 조문 번호의 소속을 확인한 것과, 그 조문이 답변을 충분히 뒷받침하는 것은 다른 검사입니다. 원문 구간·출처·해시가 모두 맞을 때만 소속 법령을 연결합니다. 상한 40개를 넘는 인용은 전수 확인했다고 표시하지 않습니다.</p><p>기존 원응답 14건의 답변·출처 동일 · 통합 회귀 1,023개 통과 · 운영 반영 '+esc(c['deployed_commit'][:9])+'</p>']
 for r in c['rows']:
  lines+=['<h3>'+esc(r['label'])+'</h3><p>'+esc(r['question'])+'</p><p>'+esc(r['interpretation'])+'</p><p>HTTP '+str(r['status'])+' · '+str(r['elapsed_seconds'])+'초 · 조문 좌표 확인 '+str((r['citation_counts'] or {}).get('ok',0))+' · 답변 근거 연결 미확인 '+str(r['grounding_unconfirmed'])+'</p>',answer('이번 운영 실행에서 실제 전달한 답변',r['answer'])]
 lines+=['<p>두 질문은 실제 운영 서버에서 새로 실행했습니다. 모델 출력 변동이 있으므로, 앞선 답변과의 문장 차이를 이번 인용 표시 수정의 효과로 해석하지 않습니다. 새 질문은 개발자가 작성한 합성 업무 사례이며 독립 정답 평가가 아닙니다.</p></section>']
if d.get('spaced_role_recheck'):
 r=d['spaced_role_recheck']
 lines+=['<h2>실제 답변에서 새로 발견한 띄어쓰기 결함도 수정했습니다</h2><p>“수탁자인 민간 SI 회사”처럼 회사명에 공백이 있으면 역할 단정 검사를 빠져나갔습니다. 회사명 한 가지를 외우는 대신 공백·탭이 있는 조직 표현을 같은 규칙으로 검사하고, 조건부 표현과 원문에 그대로 있는 문장은 보존하도록 시험했습니다. 운영 '+esc(r['deployed_commit'][:9])+' 반영 · 최종 회귀 1,029개 통과.</p>',answer('실제 운영에서 나온 문장 — 수정 전',r['before']),answer('동일 문장 재검증 — 원칙은 유지하고 단정만 제외',r['after']),'<p>위 전후는 같은 문장의 재검증이며 새 모델 실행 결과가 아닙니다. 나머지 원응답과 실패 기록은 보존했습니다.</p>']
if d.get('role_alias_recheck'):
 r=d['role_alias_recheck']
 lines+=['<h2>운영 새 답변에서 발견해 추가로 고친 역할 표현</h2><p>고객사를 위탁자로 괄호 안에 단정하는 표현이 다시 나왔습니다. 고객사·협력사 같은 회사 지칭도 검사하도록 고쳤습니다. 아래는 그 실제 답변 문장의 재검증이며 새 모델 생성이나 전체 응답 재실행은 아닙니다.</p>',answer('수정 전 실제 해설',r['original_explanation']),answer('같은 문장 재검증 — 원칙 유지·마지막 단정 제외',r['after'])]
if d.get('final_citation_ui'):
 lines+=['<h2>마지막 운영 화면 실행은 보류였습니다</h2><p>공백 회사명 수정 뒤 SI 질문을 화면에서 다시 실행했으나, 원문 인용 또는 역할 연결 검사에서 설명이 전부 보류됐습니다. 앞선 API 2건 성공과 합쳐 성공으로 표시하지 않았습니다. 이 화면에서는 모델 원출력을 확보하지 못했으므로 공백 검사 때문이라고 단정하지 않습니다. 별도 원출력 보존 진단 결과는 아래에 구분합니다.</p>']
if d.get('instrumented_diagnostic'):
 r=d['instrumented_diagnostic']
 lines+=['<h2>원출력을 보존한 별도 진단: 원칙 3개 유지·역할 단정 3개 제외</h2><p>운영과 같은 코드를 별도 프로세스에서 실행해 요청을 고정하고, 새 모델 응답 1개를 원출력까지 저장했습니다. 같은 요청 바이트를 재생한 API 경로에서 감독·접근권한·직원 관리 원칙 3개가 전달됐습니다. 모델이 덧붙인 회사 역할 단정 3개는 제외됐습니다.</p>',answer('고정 요청의 새 모델 응답을 검사한 실제 전달문',r['answer']),'<p>앞선 화면 보류와는 다른 생성 결과입니다. 그 보류가 해소됐다거나 항상 설명을 전달한다고 판단하지 않습니다. 이후 보류에는 형식·역할·근거 검사별 개수를 남기도록 진단을 보완했습니다.</p>']
if d.get('final_operating_citation'):
 r=d['final_operating_citation']
 lines+=['<section id="final-operating"><h2>최종 운영 화면: 네 가지 원칙을 전달했습니다</h2><p>운영 '+esc(r['deployed_commit'][:9])+' · 실제 HTTP 200과 화면을 함께 확인했습니다. 감독 의무·접근권한 변경·기록 보관·계정 공유 제한의 4원칙이 표시됐습니다. 근거 연결이 부족한 설명 2개는 보류하고, 법적 역할을 단정한 뒷문장 1개는 제외했습니다.</p>',answer('최종 운영 HTTP 원응답의 답변',r['answer']),'<p>검사 사유 표시 추가는 답변 수락 기준을 바꾸지 않았습니다. 앞선 보류 뒤 이번 답변이 나온 차이는 모델 출력 변동을 포함합니다. 보류가 완전히 해소됐다는 증거로 사용하지 않습니다.</p></section>']
lines+=['<details><summary>증거와 범위</summary><p>원문·질문을 새로 쓰지 않고 실제 전달 응답을 표시했습니다. 보류 원출력을 수락 답변으로 올리지 않았습니다. 원DB/색인/KG 교체 없음. 완전한 법률 의미 검수·모든 회사 질문의 정답 보장 아님.</p><p><a href="contrast-tasks-2026-11-20.json">질문별 답변과 해시 JSON</a></p></details>','</html>']
Path('contrast-tasks-2026-11-20.html').write_text('\n'.join(lines)+'\n',encoding='utf8')
