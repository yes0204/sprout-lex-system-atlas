"""Publish sanitized answers from a completed, bounded comparison only."""
import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NAMES={'manufacturer':'제조사 유지보수 · 감독과 직원 교육',
       'retailer':'유통사 개발 · 감독과 접근권한 관리',
       'education':'교육회사 SI · 감독과 직원 교육',
       'staff_control':'자체 직원 급여 · 위탁이 아닌 경우'}

def build():
    data=json.loads((ROOT/'source-order-2026-11-20.json').read_text(encoding='utf8'))
    assert len(data['rows'])==8 and data['model_posts']==7
    esc=lambda text:html.escape(text).replace('\n','&#10;')
    out=['<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
      '<title>근거부터 고르면 답변이 나아질까? · 실제 4질문 비교</title>',
      '<style>body{max-width:1080px;margin:40px auto;padding:0 24px;color:#202620;background:#fff;font:17px/1.8 system-ui,sans-serif}h1{font-size:2rem;line-height:1.4}h2{font-size:1.35rem}a{color:#255d4a}.lead{font-size:1.12rem}.note{background:#f1f5f2;padding:20px;border-left:4px solid #426851}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}.arm{border-top:2px solid #a7b8ad;padding-top:12px;min-width:0}.answer{white-space:pre-wrap;overflow-wrap:anywhere;font:16px/1.9 Georgia,"Noto Serif KR",serif}details{margin:16px 0}summary{cursor:pointer;font-weight:600}section{margin:48px 0}table{width:100%;border-collapse:collapse}td,th{padding:12px 8px;text-align:left;border-bottom:1px solid #ddd}small{color:#58615a} @media(max-width:700px){body{padding:0 18px;margin-top:24px}.pair{grid-template-columns:1fr}h1{font-size:1.65rem}table{font-size:14px}td,th{padding:8px 4px}}</style>',
      '<a href="index.html#tab=kanban">← 진행보드</a> · <a href="#followup">마지막 운영 답변과 수정 전후 ↓</a><h1>근거부터 고르면<br>답변이 나아질까?</h1>',
      '<p class="lead">같은 검색 결과와 같은 검사 기준으로, 답변을 만드는 순서만 바꿔 실제 4질문을 비교했습니다.</p>',
      '<div class="note"><strong>'+esc(data['conclusion'])+'</strong><p>'+esc(data['decision'])+'</p></div>',
      '<p>기존: 적용 유형 → 설명 → 근거 선택<br>후보: 근거 선택 → 설명 → 적용 유형</p>',
      '<p>모델 생성 7회 중 6회는 답변까지 검증했습니다. 자체 직원 질문 1회는 재검증 때 공급이 달라져 중단했고, 남은 기존 방식 1회는 실행하지 않았습니다. 출력 변동이 섞여 있으므로 일반적인 개선율이나 정답률을 계산하지 않습니다. 새 질문 2개도 개발자가 작성했으며 독립 평가용 비공개 질문은 아닙니다.</p>',
      '<table><thead><tr><th>회사 업무 질문</th><th>기존 전달 / 보류</th><th>후보 전달 / 보류</th></tr></thead><tbody>']
    for key,title in NAMES.items():
        pair={r['arm']:r for r in data['rows'] if r['case']==key}
        cells=[str(pair[a]['accepted'])+' / '+str(len(pair[a]['held'])) if pair[a]['accepted'] is not None else pair[a]['status_label'] for a in ['baseline','evidence_first']]
        out.append('<tr><td><a href="#'+key+'">'+esc(title)+'</a></td>'+''.join('<td>'+x+'</td>' for x in cells)+'</tr>')
    out+=['</tbody></table><small>전달 = 기존 원문·역할 연결 검사를 통과한 설명 묶음 수. 법률 의미 정답 수가 아닙니다. 설명 개수가 달라도 같은 업무를 중복 설명할 수 있습니다.</small>']
    for key,title in NAMES.items():
        pair={r['arm']:r for r in data['rows'] if r['case']==key}
        out+=['<section id="'+key+'"><h2>'+esc(title)+'</h2><p>'+esc(pair['baseline']['question'])+'</p>',
              '<p><strong>읽어본 결과:</strong> '+esc(data['reading'][key])+'</p><div class="pair">']
        for arm,label in [('baseline','기존 방식'),('evidence_first','근거 우선 후보')]:
            r=pair[arm]
            state='설명 '+str(r['accepted'])+'개 전달 · '+str(len(r['held']))+'개 보류' if r['accepted'] is not None else esc(r['status_label'])
            out+=['<article class="arm"><h3>'+label+'</h3><p>'+state+'</p>',
                  '<details><summary>검사 보완 전 전달 답변 — 위 지적과 함께 읽기</summary><div class="answer">'+esc(r.get('answer') or '전달된 설명 없음')+'</div></details>']
            if r.get('repair_answer'):
                out+=['<details><summary>검사 보완 후 같은 원출력 재검증 · 새 생성 아님</summary><div class="answer">'+esc(r['repair_answer'])+'</div></details>']
            out+=['</article>']
        out+=['</div></section>']
    repair=data['repair']
    out+=['<section id="repair"><h2>이번에 실제로 고친 것: 역할을 같은 뜻으로 묶지 않기</h2><p>'+esc(repair['summary'])+'</p><div class="pair">',
          '<article class="arm"><h3>검사 보완 전</h3><div class="answer">'+esc(repair['before_excerpt'])+'</div></article>',
          '<article class="arm"><h3>같은 원응답에 검사 보완 후</h3><div class="answer">'+esc(repair['after_excerpt'])+'</div></article></div><p>'+esc(repair['scope'])+'</p></section>']
    operating=data['operating_check']
    out+=['<section id="operating"><h2>새 병원 업무 질문을 운영 서버에서 확인했습니다</h2><p>'+esc(operating['question'])+'</p>',
          '<p>'+esc(operating['assessment'])+'</p><p>운영 API 1회 · HTTP 200 · 137.451초 · 자동 재시도 없음. HTTP 성공은 답변 품질 통과가 아닙니다.</p>',
          '<details><summary>실제 운영 답변 전체 — 남은 오류 포함</summary><div class="answer">'+esc(operating['answer'])+'</div></details>']
    for statement in operating['explanation_recheck']['statements']:
        if statement['changed']:
            out+=['<div class="pair"><article class="arm"><h3>실제 운영 답변에서 발견</h3><div class="answer">'+esc(statement['before'])+'</div></article>',
                  '<article class="arm"><h3>추가 검사 후 · 새 생성 아님</h3><div class="answer">'+esc(statement['after'])+'</div></article></div>']
    out+=['<p>원칙 5개 중 3개는 그대로, 2개는 근거 없는 마지막 문장만 제외했습니다. 남겨진 원칙 문구는 다시 쓰지 않았습니다. 모든 법률 의미를 검증한 결과는 아닙니다.</p></section>']
    followup=data['followup']
    out+=['<section id="followup"><h2>운영 재확인: 원칙 두 축은 전달, 사안 단정은 추가 보완</h2><p>'+esc(followup['assessment'])+'</p>',
          '<p>운영 6e421a6f7 · HTTP 200 · 59.087초 · 자동 재시도 0. 원응답과 실패는 보존했습니다.</p>',
          '<details><summary>새 운영 답변 전체 · 추가 지적 포함</summary><div class="answer">'+esc(followup['run']['answer'])+'</div></details>']
    for statement in followup['recheck']:
        out+=['<div class="pair"><article class="arm"><h3>새 답변의 해설</h3><div class="answer">'+esc(statement['before'])+'</div></article>',
              '<article class="arm"><h3>추가 검사 후 · 원칙 문구 그대로</h3><div class="answer">'+esc(statement['after'])+'</div></article></div>']
    out+=['<p>끝난 일: 발견한 표현의 검사 보완과 같은 문장 재검사. 남은 일: 다른 표현·다른 업무에서의 의미 검증과 검색 재현 안정성. 모든 질문의 정답이나 개선율 100%를 주장하지 않습니다.</p></section>']
    out+=['<details><summary>검증 범위와 증거</summary><p>네 쌍 모두 질문·공급 원문·지시문·모델 설정이 동일하고 구조화 출력 항목 순서만 다른 것을 전송 전에 대조했습니다. 다만 자체 직원 질문은 이후 재현에서 공급이 변해 종단 비교에서 제외했습니다. 운영 DB·색인·KG 변경 없음. 실패한 준비 실행은 보존했으며 모델을 보내지 않았습니다. 모델 원출력과 배달 결과는 분리했습니다. 이 페이지는 합성 업무 질문과 공개 법령에 근거한 답변만 포함합니다.</p><a href="source-order-2026-11-20.json">실제 결과와 해시 JSON</a></details></html>']
    (ROOT/'source-order-2026-11-20.html').write_text('\n'.join(out)+'\n',encoding='utf8')

if __name__=='__main__':build()
