/* 01 처리 지도 — 「지식·자료 층」 덧그림 (작성: Sarah · 2026-11-06 · 사용자 요청 · Anna 와 함께 검토)
   - 원래 지도(data.js 의 노드 14개 · 엣지 17개)는 바꾸지 않는다. 그 위에 별도 묶음(#layer-root)을 덧그린다.
   - 상태는 색만이 아니라 글자로도 적는다: 제품 연결 / 격리 실험 / 미연결 / 제안.
   - 「격리 실험」·「제안」은 main 코드에 없다. 원래 지도는 11/4 고정 커밋의 코드 그림이고, 이 층은 그 뒤의 기록을 덧붙인 것이다.
   - 네트워크·모델 호출 없음. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var GH = 'https://github.com/yes0204/sprout-lex/blob/';
  var STATE = {
    live: { label: '제품 연결', cls: 'live' },
    exp: { label: '격리 실험', cls: 'exp' },
    off: { label: '미연결', cls: 'off' },
    plan: { label: '제안 · 구현 전', cls: 'plan' }
  };
  var LAYERS = [
    { id: 'L-registry', x: 1380, y: 60, state: 'exp', title: 'James 신규 사전 · 등록부', sub: '등록 2,850 · 출처 726 · 정의 202',
      summary: 'James 가 새로 만든 전체 사전 등록부다. 낱말·개념 항목 2,850개, 원문 출처 726개, 정의 연결 202개를 엄격 검사로 읽어 들인다. 전체 등록 수는 승인된 개념 수가 아니다. 이전 되묻기 사전 기록은 04 탭의 접힌 이전 기록에서 확인한다.',
      now: ['엄격 적재 2,850 / 726 / 202 유지(새 세대 root e64ca83d… 포함).', '격리 실행에서 실제 API 가 읽는 것까지 확인(신규 35건 실소비 회귀 HTTP 111건 · 모델 0 · 연결 확인이지 답변 성공이 아님).', '대부분 항목의 자격은 unknown — 답변 근거로 쓰이려면 자격 통과가 필요하다.', '제품(main) 답변 경로 전체 연결은 미완.'],
      effect: ['지금 main 의 분기는 이 등록부를 읽지 않는다 — 기존 main 사전과 신규 등록부의 연결 상태는 다르다.', '연결되면 검색 뒤 근거 선별 단계에서 원문 출처·정의 연결을 쓰게 된다(격리 브랜치에서 진행 중).', '04 사전·범위 탭의 내용은 James 소유이며 별도로 갱신된다.'],
      links: [['적재 검사 코드', 'a17ee1d97/harness_team/engine/cx01/registry_set.py'], ['격리 API', 'f377ba070/harness_team/engine/cx01/live_view.py'], ['사전 탭 내용 근거', 'f7af634ff/harness_team/engine/data/cx01/c1-remaining-batch04-261105/independent-intake/board/lexicon-content-copy.js']],
      edge: { to: 'L-ledger', label: '같은 등록부의 새 세대', kind: 'side' } },
    { id: 'L-kg', x: 1380, y: 240, state: 'off', title: '지식그래프 · 개념 그래프', sub: '파생 DB · 답변 미사용',
      summary: '정본 DB 를 읽기 전용으로 읽어 조문·판·낱말 사이 연결을 이어 둔 파생 DB 다. 개념 그래프(온톨로지에 해당)도 이 안에 있다. 정본으로 옮기지 않는다(사용자 결정).',
      now: ['노드 21,911 · 간선 32,823(11/6 재빌드 · SHA c33cbb8a…).', '「위임」 159건을 법령 위계로 다시 분류: 위로 → 근거로 한다 117 · 같은 급 → 함께 본다 42.', '위계 분류는 위임의 법률 인증이 아니다.', '실제 DB 는 Robert 독립 인수 통과(3521d5c48 · 읽기 전용 증거) — 그래도 답변 경로에는 연결되지 않았다.'],
      effect: ['지금은 어떤 분기도 이 그래프를 읽지 않는다.', '연결된다면 「누구에게 적용되나」 판단의 재료가 될 수 있다 — 아직 설계 전.'],
      links: [['재빌드 결과', 'c1a6031c9/harness_team/engine/kg/RESULT_rank_rule_v1.md'], ['설계 결정', 'c1a6031c9/harness_team/engine/kg/DECISIONS.md'], ['독립 인수(Robert)', '3521d5c48/harness_team/worklog/261105_1732_robert_kg_boundary_review.md']],
      edge: { from: 'db', label: '파생', kind: 'right' } },
    { id: 'L-ledger', x: 1380, y: 420, state: 'exp', title: '원문 장부 · 새 세대', sub: 'ledger16 · 자격 unknown',
      summary: '파일로 받은 고시·행정규칙 16개의 원문 장부다. 부칙 사유 하나(279338)를 고친 새 세대를 격리된 API 가 실제로 읽는 것까지 확인했다.',
      now: ['새 root e64ca83d… · 177 파일 바이트 재생성 일치.', '279338 은 새 메타로 읽히지만 자격은 unknown 그대로.', '독립 재검수 통과(Henry · Robert) — 격리 실행만.'],
      effect: ['원문·자격 검사 단계가 쓰는 장부다. 자격이 unknown 인 원문은 답변 근거가 되지 못한다.'],
      links: [['통합 핀', 'a17ee1d97/harness_team/engine/cx04/ledger_generation.py']],
      edge: { to: 'db', label: '새 메타', kind: 'left', y: 480 } },
    { id: 'L-frame', x: 1380, y: 630, state: 'exp', title: '원문 정리표 · norm frame', sub: '8개 항 · 생성 입력 기각',
      summary: '조문 문장을 「누가·무엇을·언제·어떻게·예외」 칸으로 나눈 표다. 칸에는 원문 글자를 잘라 넣고 위치를 적어 기계로 대조한다.',
      now: ['개발용 8개 항 · 표 11개(공급 v3).', 'AI 입력에 붙인 비교 8회(이미 노출된 개발 질문 3개): 의미 통과 0/4(표 없음) · 0/4(표 있음) → 채택 기준 미달로 기각.', '이번 비교에서는 표가 있어도 공급에 없는 절차를 지어냈다.'],
      effect: ['이번 개발 비교(AB8)에서는 AI 입력 보조로 채택 기준을 넘지 못했다 — 일반적으로 효과가 없다는 결론은 아니다.', '다음 제안(주체 거르기 · 행위 확인)의 결정적 재료로 다시 쓸 수 있다.'],
      links: [['정리표 v3', '3e584a66d/harness_team/engine/cx03/evidence/261106-norm-frame/fixture-v3.json'], ['독립 판정', '669473022/harness_team/worklog/261106_robert_norm_frame_ab8_verdict.json']],
      edge: { to: 'llm', label: '실험 입력', kind: 'left', y: 660 } },
    { id: 'L-gate', x: 1380, y: 800, state: 'plan', title: '주체 거르기 · 행위 확인', sub: '모델 앞 결정적 단계',
      summary: 'AI 에게 맡겼다 실패한 두 판단을 AI 앞으로 옮기는 제안이다. ① 적용 주체가 한정된 원문(예: 「공공기관은」)을 선택 후보에서 가른다 ② 질문이 묻는 행위가 공급 원문에 없으면 모델을 부르지 않고 「근거 없음」으로 보류한다.',
      now: ['제안 · 구현 전(David 조건부 동의) · 지금 코딩 중인 담당 없음.', '먼저 AI 없이 개발 8 · 실제 10 · 미노출 6 질문에 잰다.', '「고객 자료」라는 말로 민간 사업자라고 추론하지 않는다 — 주체가 안 밝혀졌으면 unknown 으로 표시한다(Anna 조건).', '사전 낱말이 안 맞는다는 것만으로 「근거 없음」을 확정하지 않는다 — 형태 변형 · 돌려 말하기 · 복합 질문의 재현율을 먼저 잰다(Anna 조건).'],
      effect: ['선택 단계 앞에 새 분기가 생긴다: 주체 한정 → 별도 안내 또는 되물음 / 행위 없음 → 근거 없음.', '맞는 질문인데 보류하는 비용은 Robert 가 상한을 먼저 정한다.'],
      links: [['제안서', '5ac5d1bb3/harness_team/worklog/261106_0850_sarah_next_direction_proposal.md'], ['모델 계약 의견', '1b17c9524/harness_team/worklog/261106_0843_david_next_direction_model_contract_opinion.md']],
      edge: { to: 'llm', label: '모델 전', kind: 'left', y: 700 } }
  ];
  // 원래 노드 상세에 덧붙일 내용(원래 문구는 그대로 두고 뒤에 한 절을 더한다)
  var EXTRA = {
    route: { h: '분기를 정하는 자료 (지식·자료 층과의 연결)', items: ['① 범위 밖: 수록 법령 목록과 법령 약칭 사전이 정한다(사전·범위 규칙).', '① 점수 미달: 검색 점수 0.45 — 거리 척도 l2 에 묶인 값이다.', '② 용어 확인: main의 기존 되묻기 사전이 기준이다. 신규 James 등록부와 별개이며, 세부 이력은 04 탭의 이전 기록에 있다.', '제안 중: 선택 앞에 「주체 거르기 · 행위 확인」 분기가 들어갈 수 있다(구현 전).'] },
    generate: { h: '11/4 이후 바뀐 것 — 격리 브랜치 · main 미반영 (Emily)', items: ['보호 선택 경로 통합 a938ca706: 선택 앞 출구들을 지킨 채 모델 선택을 붙였다.', '설명 연결 60504bb07: 선택 뒤에만 AI 설명 · 기본 꺼짐 · 「의미 미검증」 표지.', '실제 연결 확인(11/5 21:13): 질문 → 검색 → 선택 → 설명 → 화면. 인용 정확성은 미달.', '생성 품질 시도 5가지(선택 지시문 · 설명 지시문 · 자기 판정 · 모델 교체 · 정리표) 모두 기각.'] },
    enrich: { h: '11/4 이후 바뀐 것 — 격리 브랜치 · main 미반영 (Emily)', items: ['원문 장부 새 세대 소비 a17ee1d97: 새 root 를 실제 API 가 읽음 · 자격 unknown 유지.', '정리표를 실제 검색 결과에 결합 67337053e · 2eb714b0a: 검색 9 단위 중 8 단위가 공급과 일치.'] }
  };
  var CSS = [
    '.layer-node{cursor:pointer;outline:none}',
    '.layer-node rect{fill:#fff;stroke-width:1.8;rx:9}',
    '.layer-node.live rect{stroke:#14604f}',
    '.layer-node.exp rect{stroke:#b07a10;stroke-dasharray:6 4;fill:#fffaf0}',
    '.layer-node.off rect{stroke:#8a959b;stroke-dasharray:3 4;fill:#f6f8f8}',
    '.layer-node.plan rect{stroke:#6a4c93;stroke-dasharray:2 4;fill:#faf7fd}',
    '.layer-node .lt{font-size:17px;font-weight:700;fill:#192e35}',
    '.layer-node .ls{font-size:12px;font-weight:700}',
    '.layer-node.live .ls{fill:#14604f}.layer-node.exp .ls{fill:#8a5b00}.layer-node.off .ls{fill:#5d6a70}.layer-node.plan .ls{fill:#5a3d85}',
    '.layer-node .lm{font-size:11px;fill:#5d6a70;font-family:monospace}',
    '.layer-node.active rect,.layer-node:focus rect{stroke-width:4}',
    '.layer-edge{fill:none;stroke:#b9a6d6;stroke-width:1.6;stroke-dasharray:4 4;marker-end:url(#layer-arrow)}',
    '.layer-edge.live{stroke:#7fb3a3}',
    '.layer-caption{font-size:13px;font-weight:700;fill:#5d6a70;letter-spacing:.04em}',
    '.layer-extra{margin-top:14px;padding-top:10px;border-top:1px dashed #cfd8d6}',
    '.layer-extra h4{margin:6px 0}',
    '.layer-extra li{margin:3px 0}'
  ].join('\n');

  function s(tag, attrs, text) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (text != null) e.textContent = text; return e; }
  function h(tag, text, cls) { var e = document.createElement(tag); if (text != null) e.textContent = text; if (cls) e.className = cls; return e; }
  function base() { return window.ATLAS && window.ATLAS.nodes || []; }
  function find(id) { var n = base().filter(function (x) { return x.id === id; })[0]; return n || LAYERS.filter(function (x) { return x.id === id; })[0]; }

  function edgePath(L) {
    var e = L.edge, t, a = L;
    if (e.kind === 'down') { t = find(e.to); return 'M' + (a.x + 120) + ',' + (a.y + 84) + ' V' + t.y; }
    if (e.kind === 'side') { t = find(e.to); return 'M' + (a.x + 240) + ',' + (a.y + 42) + ' H1650 V' + (t.y + 42) + ' H' + (t.x + 240); }
    if (e.kind === 'right') { t = find(e.from); return 'M' + (t.x + 240) + ',' + (t.y + 20) + ' H1325 V' + (a.y + 42) + ' H' + a.x; }
    t = find(e.to); var ty = e.y, sy = (Math.abs((a.y + 42) - ty) < 30) ? ty : a.y + 42;
    return sy === ty ? 'M' + a.x + ',' + ty + ' H' + (t.x + 240) : 'M' + a.x + ',' + sy + ' H1360 V' + ty + ' H' + (t.x + 240);
  }
  function labelPos(L) {
    var e = L.edge;
    if (e.kind === 'down') return [L.x + 128, L.y + 84 + 24, 'start'];
    if (e.kind === 'side') return [1640, L.y + 128, 'end'];
    if (e.kind === 'right') return [1352, L.y + 34, 'middle'];
    return [1345, e.y - 7, 'middle'];
  }

  function select(L) {
    document.querySelectorAll('.diagram-node,#node-list button').forEach(function (x) { x.classList.remove('active'); x.setAttribute('aria-pressed', 'false'); });
    document.querySelectorAll('.layer-node').forEach(function (x) { x.classList.toggle('active', x.dataset.id === L.id); });
    var box = document.getElementById('detail'); if (!box) return;
    box.replaceChildren(h('p', '지식·자료 층 · ' + STATE[L.state].label, 'kicker'), h('h3', L.title), h('p', L.summary, 'summary'));
    box.append(h('h4', '지금 상태'));
    var ol = h('ul'); L.now.forEach(function (x) { ol.append(h('li', x)); }); box.append(ol);
    box.append(h('h4', '분기·답변에 미치는 영향'));
    var c = h('div', null, 'conditions'); L.effect.forEach(function (x) { c.append(h('p', x)); }); box.append(c);
    box.append(h('h4', '근거'));
    var r = h('div', null, 'code-ref');
    L.links.forEach(function (l, i) { if (i) r.append(document.createElement('br')); var a = h('a', l[0] + ' ↗ · 저장소 권한 필요'); a.href = GH + l[1]; a.target = '_blank'; a.rel = 'noopener'; r.append(a); });
    box.append(r);
    box.append(h('p', '이 층은 11/4 코드 그림 위에 11/6 기록을 덧붙인 것이다. 「격리 실험」·「제안」은 main 코드에 없다.', 'summary'));
  }

  function addLayer() {
    var root = document.getElementById('diagram'); if (!root || document.getElementById('layer-root')) return;
    var g = s('g', { id: 'layer-root' });
    var defs = s('defs'); var m = s('marker', { id: 'layer-arrow', viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse' }); m.append(s('path', { d: 'M0 0 L10 5 L0 10 Z', fill: '#9c8bb8' })); defs.append(m); g.append(defs);
    g.append(s('text', { x: 1380, y: 40, class: 'layer-caption' }, '지식·자료 층 — 11/6 기록 덧그림'));
    LAYERS.forEach(function (L) {
      g.append(s('path', { d: edgePath(L), class: 'layer-edge' + (L.state === 'live' ? ' live' : '') }));
      var p = labelPos(L); g.append(s('text', { x: p[0], y: p[1], 'text-anchor': p[2], class: 'edge-label' }, L.edge.label));
    });
    LAYERS.forEach(function (L) {
      var n = s('g', { transform: 'translate(' + L.x + ' ' + L.y + ')', class: 'layer-node ' + STATE[L.state].cls, 'data-id': L.id, tabindex: 0, role: 'button', 'aria-label': L.title + ' — ' + STATE[L.state].label + ' 상세' });
      n.append(s('title', {}, L.summary));
      n.append(s('rect', { width: 240, height: 84 }));
      n.append(s('text', { x: 14, y: 28, class: 'lt' }, L.title));
      n.append(s('text', { x: 14, y: 50, class: 'ls' }, STATE[L.state].label));
      n.append(s('text', { x: 14, y: 70, class: 'lm' }, L.sub));
      n.onclick = function () { select(L); };
      n.onkeydown = function (ev) { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); select(L); } };
      g.append(n);
    });
    root.append(g);
  }

  function extend(ev) {
    var x = EXTRA[ev.detail]; var box = document.getElementById('detail'); if (!x || !box) return;
    document.querySelectorAll('.layer-node').forEach(function (n) { n.classList.remove('active'); });
    var sec = h('div', null, 'layer-extra'); sec.append(h('h4', x.h));
    var ul = h('ul'); x.items.forEach(function (t) { ul.append(h('li', t)); }); sec.append(ul);
    var share = box.querySelector('.share-node'); if (share) box.insertBefore(sec, share); else box.append(sec);
  }

  function init() {
    var root = document.getElementById('diagram'); if (!root) return;
    if (!document.getElementById('layer-style')) { var st = document.createElement('style'); st.id = 'layer-style'; st.textContent = CSS; document.head.append(st); }
    root.setAttribute('viewBox', '0 0 1680 1090');
    addLayer();
    new MutationObserver(function () { addLayer(); }).observe(root, { childList: true });
    document.addEventListener('atlas-node-select', extend);
    var cap = document.querySelector('.map-caption');
    if (cap && !cap.dataset.layer) { cap.dataset.layer = '1'; cap.textContent += ' · 오른쪽 「지식·자료 층」은 11/6 기록 덧그림(제품 연결 / 격리 실험 / 미연결 / 제안).'; }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
