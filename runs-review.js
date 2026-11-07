/* 02 실행 기록 따라가기 — 내용 렌더러 (작성: Sarah · 02 전용 · 공통 파일과 독립)
   입력: window.RUNS_REVIEW (runs-review-data.js — runs-review.json 에서 기계 생성)
   사용: RunsReview.mount(element)  — 네트워크·모델 호출 없음. 기록을 화면에 그릴 뿐이다. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  // 끝난 곳 4종 — 색은 항목에 고정(순서·필터가 바뀌어도 같은 색). 글자는 항상 본문 색.
  var ENDED = [
    { key: 'quoted', label: '인용 답변까지 감', color: '#2a78d6' },
    { key: 'model_stopped', label: '모델에서 멈춤(근거 부족 응답)', color: '#eda100', ink: '#192e35' },
    { key: 'error', label: '오류 응답', color: '#d03b3b', mark: '!' },
    { key: 'before_model', label: '모델 전에 보류', color: '#b4bfc2', ink: '#192e35' }
  ];
  var CSS = [
    '.rr{color:#192e35;font-size:13px;line-height:1.6}',
    '.rr h3{font-size:15px;margin:26px 0 8px}',
    '.rr h4{font-size:13px;margin:16px 0 6px}',
    '.rr p{margin:6px 0}',
    '.rr .rr-note{color:#65757b;font-size:12px}',
    '.rr .rr-rules{margin:0;padding-left:18px;color:#3d5158;font-size:12px}',
    '.rr .rr-card{border:1px solid #dce3e4;border-radius:7px;background:#fff;padding:16px 18px;margin:10px 0}',
    '.rr .rr-legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12px;margin:4px 0 10px}',
    '.rr .rr-legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}',
    '.rr svg{display:block;width:100%;height:auto;max-width:760px;min-width:560px}',
    '.rr svg text{font-family:inherit}',
    '.rr .rr-tip{position:fixed;pointer-events:none;background:#192e35;color:#fff;font-size:12px;padding:6px 9px;border-radius:5px;max-width:260px;z-index:20}',
    '.rr .rr-scroll{overflow-x:auto}',
    '.rr table{border-collapse:collapse;width:100%;font-size:12px}',
    '.rr th,.rr td{border-bottom:1px solid #e6ecec;padding:7px 8px;text-align:left;vertical-align:top}',
    '.rr th{color:#65757b;font-weight:600;white-space:nowrap}',
    '.rr td.num,.rr th.num{text-align:right;font-variant-numeric:tabular-nums}',
    '.rr .rr-tabs{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}',
    '.rr .rr-tabs button{border:1px solid #dce3e4;background:#fff;border-radius:16px;padding:6px 12px;font-size:12px;cursor:pointer;color:#192e35}',
    '.rr .rr-tabs button[aria-pressed="true"]{background:#203c48;color:#fff;border-color:#203c48}',
    '.rr .rr-meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin:10px 0}',
    '.rr .rr-meta div{border:1px solid #e6ecec;border-radius:6px;padding:8px 10px;font-size:11px;color:#65757b}',
    '.rr .rr-meta strong{display:block;font-size:14px;color:#192e35;overflow-wrap:anywhere}',
    '.rr .rr-steps{display:flex;flex-wrap:wrap;gap:4px;margin-top:4px}',
    '.rr .rr-step{font-size:10px;padding:2px 6px;border-radius:10px;border:1px solid #dce3e4;color:#65757b;white-space:nowrap}',
    '.rr .rr-step.ok{background:#e7f4ee;border-color:#bfe0d2;color:#14604f}',
    '.rr .rr-step.stop{background:#fdeee6;border-color:#f2c3a9;color:#8a3a12;font-weight:700}',
    '.rr .rr-step.err{background:#fbe9e9;border-color:#eab3b3;color:#8f2020;font-weight:700}',
    '.rr .rr-badge{display:inline-block;font-size:10px;font-weight:700;border-radius:10px;padding:2px 8px;border:1px solid #dce3e4;white-space:nowrap}',
    '.rr .rr-badge.yes{background:#e7f4ee;border-color:#bfe0d2;color:#14604f}',
    '.rr .rr-badge.no{background:#f4f5f5;color:#52514e}',
    '.rr .rr-q{font-weight:600}',
    '.rr .rr-split{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}',
    '.rr ul{margin:4px 0;padding-left:18px}'
  ].join('\n');

  function el(tag, text, cls) { var e = document.createElement(tag); if (text != null) e.textContent = text; if (cls) e.className = cls; return e; }
  function sv(tag, attrs, text) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (text != null) e.textContent = text; return e; }
  function list(items) { var u = el('ul'); (items || []).forEach(function (t) { u.append(el('li', t)); }); return u; }

  function trendChart(trend, tip) {
    var rows = trend.rows, W = 760, left = 150, right = 60, barH = 26, gap = 22, top = 8;
    var H = top + rows.length * (barH + gap) + 26, unit = (W - left - right) / 10;
    var svg = sv('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': '실제 질문 10개가 실행마다 어디서 끝났는지 보여 주는 막대 그림. 아래 표에 같은 값이 있다.' });
    for (var g = 0; g <= 10; g += 2) {
      var gx = left + g * unit;
      svg.append(sv('line', { x1: gx, y1: top, x2: gx, y2: H - 24, stroke: '#e6ecec', 'stroke-width': 1 }));
      svg.append(sv('text', { x: gx, y: H - 8, 'text-anchor': 'middle', 'font-size': 11, fill: '#65757b' }, g + '개'));
    }
    rows.forEach(function (r, i) {
      var y = top + i * (barH + gap), x = left;
      svg.append(sv('text', { x: left - 10, y: y + 11, 'text-anchor': 'end', 'font-size': 12, fill: '#192e35', 'font-weight': 600 }, r.run));
      svg.append(sv('text', { x: left - 10, y: y + 25, 'text-anchor': 'end', 'font-size': 10, fill: '#65757b' }, '코드 ' + r.code_pin));
      ENDED.forEach(function (c) {
        var n = (r.ended || {})[c.key] || 0; if (!n) return;
        var w = n * unit - 2;
        var rect = sv('rect', { x: x, y: y, width: w, height: barH, rx: 3, fill: c.color, tabindex: 0 });
        var msg = r.run + ' · ' + c.label + ' ' + n + '개 / 10개';
        rect.addEventListener('mousemove', function (ev) { tip.textContent = msg; tip.hidden = false; tip.style.left = (ev.clientX + 12) + 'px'; tip.style.top = (ev.clientY + 12) + 'px'; });
        rect.addEventListener('mouseleave', function () { tip.hidden = true; });
        rect.append(sv('title', {}, msg));
        svg.append(rect);
        svg.append(sv('text', { x: x + w / 2, y: y + barH / 2 + 4, 'text-anchor': 'middle', 'font-size': 12, 'font-weight': 700, fill: c.ink || '#fff', 'pointer-events': 'none' }, (c.mark ? c.mark + ' ' : '') + n));
        x += n * unit;
      });
      svg.append(sv('text', { x: left + 10 * unit + 8, y: y + barH / 2 + 4, 'font-size': 11, fill: '#65757b' }, '양성 ' + r.positive));
    });
    return svg;
  }

  function trendBlock(d, tip) {
    var t = d.trend_real10; if (!t) return el('div');
    var box = el('div', null, 'rr-card');
    box.append(el('h4', '실제 질문 10개 — 실행 시각별로 어디서 끝났나'));
    box.append(el('p', '같은 10개 질문을 코드만 바꿔 다시 돌린 기록이다. 파란 칸만 답이 나온 것이다. ' + (t.note || ''), 'rr-note'));
    var lg = el('div', null, 'rr-legend');
    ENDED.forEach(function (c) { var s = el('span'); var i = el('i'); i.style.background = c.color; s.append(i, document.createTextNode(c.label)); lg.append(s); });
    var chartWrap = el('div', null, 'rr-scroll'); chartWrap.append(trendChart(t, tip)); // 좁은 화면: 글자가 줄어드는 대신 가로로 민다
    box.append(lg, chartWrap);
    var wrap = el('div', null, 'rr-scroll'), tb = el('table'), hd = el('tr');
    [['실행', 0], ['코드', 0], ['모델 호출', 1], ['HTTP 200', 1], ['양성 답변', 1], ['경계 최소 보류', 1], ['누락 조건 해소', 1], ['독립 평가', 0]].forEach(function (h) { hd.append(el('th', h[0], h[1] ? 'num' : '')); });
    tb.append(hd);
    t.rows.forEach(function (r) {
      var tr = el('tr');
      [[r.run, 0], [r.code_pin, 0], [r.model_posts + '회', 1], [r.http_200 + '/10', 1], [r.positive, 1], [r.boundary, 1], [r.condition, 1], [r.evaluation, 0]].forEach(function (c) { tr.append(el('td', String(c[0]), c[1] ? 'num' : '')); });
      tb.append(tr);
    });
    wrap.append(tb); box.append(wrap);
    box.append(el('p', 'HTTP 200은 응답이 왔다는 뜻일 뿐 답변 성공이 아니다. 모델 호출 수가 늘어난 것도 성과가 아니다 — 답이 나온 수(파란 칸)와 독립 평가만 본다.', 'rr-note'));
    return box;
  }

  // 답변 흐름 — 구간 상태 3종. 색만으로 구분하지 않고 상태 글자를 함께 쓴다.
  var FLOW_STATE = {
    ok: { label: '통과', fill: '#e7f4ee', stroke: '#14604f', ink: '#14604f' },
    weak: { label: '약함', fill: '#fdf3df', stroke: '#9a6a00', ink: '#7a5300' },
    fail: { label: '품질 미달', fill: '#fbe9e9', stroke: '#a32b2b', ink: '#8f2020' }
  };
  function wrapText(t, n) { var out = [], s = String(t); while (s.length > n) { var cut = s.lastIndexOf(' ', n); if (cut < n / 2) cut = n; out.push(s.slice(0, cut).trim()); s = s.slice(cut).trim(); } if (s) out.push(s); return out; }

  function flowChart(f, tip) {
    var st = f.stages, bw = 132, bh = 150, gap = 16, top = 10, W = st.length * bw + (st.length - 1) * gap + 4, H = top + bh + 12;
    var svg = sv('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': '답변 흐름 그림. 질문에서 화면까지 구간별 연결과 품질 상태. 아래 표에 같은 내용이 있다.' });
    svg.style.maxWidth = '1040px'; svg.style.minWidth = '720px';
    st.forEach(function (s, i) {
      var x = 2 + i * (bw + gap), c = FLOW_STATE[s.state] || FLOW_STATE.weak;
      if (i > 0) {
        var ax = x - gap, ay = top + 40;
        svg.append(sv('line', { x1: ax + 1, y1: ay, x2: x - 4, y2: ay, stroke: '#65757b', 'stroke-width': 1.5 }));
        svg.append(sv('path', { d: 'M' + (x - 4) + ' ' + (ay - 4) + ' L' + x + ' ' + ay + ' L' + (x - 4) + ' ' + (ay + 4) + ' Z', fill: '#65757b' }));
      }
      var g = sv('g', { tabindex: 0 });
      g.append(sv('rect', { x: x, y: top, width: bw, height: bh, rx: 6, fill: c.fill, stroke: c.stroke, 'stroke-width': s.link.indexOf('미연결') >= 0 ? 1 : 1.5, 'stroke-dasharray': s.link.indexOf('미연결') >= 0 ? '4 3' : '' }));
      g.append(sv('text', { x: x + 10, y: top + 22, 'font-size': 13, 'font-weight': 700, fill: '#192e35' }, s.name));
      g.append(sv('text', { x: x + 10, y: top + 40, 'font-size': 10.5, fill: '#3d5158' }, s.link));
      g.append(sv('text', { x: x + 10, y: top + 60, 'font-size': 11, 'font-weight': 700, fill: c.ink }, c.label));
      wrapText(s.quality, 13).slice(0, 5).forEach(function (line, k) { g.append(sv('text', { x: x + 10, y: top + 80 + k * 15, 'font-size': 10.5, fill: '#192e35' }, line)); });
      var msg = s.name + ' — ' + s.link + ' · ' + c.label + ': ' + s.evidence + (s.fix ? ' · 고칠 곳: ' + s.fix : '');
      g.addEventListener('mousemove', function (ev) { tip.textContent = msg; tip.hidden = false; tip.style.left = (ev.clientX + 12) + 'px'; tip.style.top = (ev.clientY + 12) + 'px'; });
      g.addEventListener('mouseleave', function () { tip.hidden = true; });
      g.append(sv('title', {}, msg));
      svg.append(g);
    });
    return svg;
  }

  function flowBlock(d, tip) {
    var f = d.answer_flow; if (!f) return el('div');
    var box = el('div', null, 'rr-card');
    box.append(el('h4', f.title), el('p', f.as_of + ' · ' + f.note, 'rr-note'));
    var lg = el('div', null, 'rr-legend');
    ['ok', 'weak', 'fail'].forEach(function (k) { var s = el('span'); var i = el('i'); i.style.background = FLOW_STATE[k].fill; i.style.border = '1px solid ' + FLOW_STATE[k].stroke; s.append(i, document.createTextNode(FLOW_STATE[k].label)); lg.append(s); });
    var dash = el('span', '점선 테두리: 제품에 연결되지 않은 진단 단계'); lg.append(dash);
    var cw = el('div', null, 'rr-scroll'); cw.append(flowChart(f, tip));
    box.append(lg, cw);
    var wrap = el('div', null, 'rr-scroll'), tb = el('table'), hd = el('tr');
    var hasFix = f.stages.some(function (s) { return s.fix; });
    (hasFix ? ['구간 · 노드', '상태', '막힌 이유와 근거', '모델 교체 효과', '고칠 곳'] : ['구간', '연결', '상태', '근거']).forEach(function (h) { hd.append(el('th', h)); }); tb.append(hd);
    f.stages.forEach(function (s) { var tr = el('tr'); var c = FLOW_STATE[s.state] || FLOW_STATE.weak; var b = el('td'); b.append(el('span', c.label, 'rr-badge ' + (s.state === 'ok' ? 'yes' : 'no'))); var q = el('td'); q.append(el('div', s.quality, 'rr-q'), el('div', s.evidence, 'rr-note'));
      if (hasFix) { var n = el('td'); n.append(el('div', s.name, 'rr-q'), el('div', (s.node || '') + ' · ' + s.link, 'rr-note')); var fx = el('td'); fx.append(el('strong', s.fix || '—')); tr.append(n, b, q, el('td', s.model_effect || '—'), fx); }
      else tr.append(el('td', s.name), el('td', s.link), b, q);
      tb.append(tr); });
    wrap.append(tb); box.append(wrap);
    if (f.next) box.append(el('p', '다음 — ' + f.next.state + ': ' + f.next.text));
    if (f.limit) box.append(el('p', '한계: ' + f.limit, 'rr-note'));
    return box;
  }

  function eveningBlock(d) {
    var e = d.evening_tests; if (!e) return el('div');
    var box = el('div', null, 'rr-card');
    box.append(el('h4', e.title), el('p', e.note, 'rr-note'));
    var wrap = el('div', null, 'rr-scroll'), tb = el('table'), hd = el('tr');
    ['시각', '시험', '모델 호출', '결과', '결정', '판정'].forEach(function (h) { hd.append(el('th', h)); }); tb.append(hd);
    e.rows.forEach(function (r) {
      var tr = el('tr'), nm = el('td'); nm.append(el('div', r.name, 'rr-q'), el('div', r.what, 'rr-note'));
      var dc = el('td'); dc.append(el('div', r.decision), el('div', '근거: ' + r.source, 'rr-note'));
      var v = el('td'); v.append(el('span', r.verdict, 'rr-badge ' + (r.ok ? 'yes' : 'no')));
      tr.append(el('td', r.at), nm, el('td', r.calls, 'num'), el('td', r.result), dc, v); tb.append(tr);
    });
    wrap.append(tb); box.append(wrap);
    box.append(el('p', e.summary));
    if (e.excluded) box.append(el('p', e.excluded, 'rr-note'));
    return box;
  }

  function stepChip(name, state) {
    var cls = 'rr-step';
    if (state === '통과') cls += ' ok'; else if (state === '멈춤') cls += ' stop'; else if (state.indexOf('오류') === 0) cls += ' err'; else if (state.indexOf('미기록') >= 0) cls += ' stop';
    var s = el('span', name + (state === '통과' ? ' ✓' : state === '도달 안 함' ? ' –' : state === '멈춤' ? ' ■' : state.indexOf('오류') === 0 ? ' !' : ' ?'), cls);
    s.title = name + ': ' + state; return s;
  }

  function runDetail(s, stages) {
    var box = el('div', null, 'rr-card');
    box.append(el('h4', s.label));
    box.append(el('p', s.evidence_class + (s.what_changed ? ' · 바뀐 점: ' + s.what_changed : ''), 'rr-note'));
    var m = el('div', null, 'rr-meta');
    var ev = s.independent_evaluation;
    [['실행 시각', s.at], ['코드', s.code_pin + (s.result_pin ? ' / 결과 ' + s.result_pin : '')], ['질문 수(분모)', s.denominator], ['HTTP 200', s.http_200 + (s.http_error ? ' (오류 ' + s.http_error + ')' : '')],
     ['답변 모델 호출', s.model_posts + '회'], ['검색용 임베딩', s.embedding_calls == null ? '기록 없음' : s.embedding_calls + '회'],
     ['독립 평가', ev ? ev.by + ' · 양성 ' + ev.positive_answered + ' · 경계 ' + ev.boundary_minimum_hold + ' · 조건 ' + ev.missing_condition_resolved : '없음'],
     ['평가 근거', ev ? (ev.pin || ev.status || '') : '—']].forEach(function (p) { var d = el('div', p[0]); d.append(el('strong', String(p[1]))); m.append(d); });
    box.append(m);
    if (s.stopped_summary) box.append(el('p', s.stopped_summary));
    if (s.environment) box.append(el('p', '환경: ' + s.environment, 'rr-note'));
    if (s.independent_receipt_check) box.append(el('p', '독립 대조(' + s.independent_receipt_check.by + ' ' + s.independent_receipt_check.pins.join(' · ') + '): ' + s.independent_receipt_check.found, 'rr-note'));
    if (s.rows) {
      box.append(el('h4', '질문별 — 어디서 멈췄나'));
      var wrap = el('div', null, 'rr-scroll'), tb = el('table'), hd = el('tr');
      ['질문', '지나간 단계', '멈춘 이유', '독립 판정'].forEach(function (h) { hd.append(el('th', h)); });
      tb.append(hd);
      s.rows.forEach(function (r) {
        var tr = el('tr'), q = el('td');
        q.append(el('div', r.id + ' · ' + r.group, 'rr-note'), el('div', r.question, 'rr-q'));
        var st = el('td'), chips = el('div', null, 'rr-steps');
        stages.forEach(function (n) { chips.append(stepChip(n, r.stages[n])); });
        st.append(el('div', r.stopped_at), chips, el('div', 'HTTP ' + r.http + ' · 모델 ' + r.model_posts + '회 · ' + r.seconds + '초' + (r.excluded_candidates ? ' · 후보 제외 ' + r.excluded_candidates + '건' : ''), 'rr-note'));
        var why = el('td'); why.append(el('div', r.why_stopped), el('div', '근거: ' + r.why_source, 'rr-note'));
        if (r.note) why.append(el('div', '주의: ' + r.note, 'rr-note'));
        var cmp = r.vs_second_run || r.vs_first_run; if (cmp) why.append(el('div', '앞 실행 대비: ' + cmp, 'rr-note'));
        var v = el('td'); v.append(el('span', r.independent_verdict, 'rr-badge ' + (r.goal_met ? 'yes' : 'no')));
        tr.append(q, st, why, v); tb.append(tr);
      });
      wrap.append(tb); box.append(wrap);
    }
    if (s.known_cause) { box.append(el('h4', s.known_cause.title), el('p', s.known_cause.text), el('p', '근거: ' + s.known_cause.source + ' · 한계: ' + s.known_cause.limit, 'rr-note')); }
    if (s.not_proven) { box.append(el('h4', '아직 입증되지 않은 것'), list(s.not_proven)); }
    if (s.caveat) box.append(el('p', '주의: ' + s.caveat, 'rr-note'));
    if (s.source) box.append(el('p', '출처: ' + s.source, 'rr-note'));
    return box;
  }

  function mount(root) {
    var d = window.RUNS_REVIEW; if (!root || !d) return;
    if (!document.getElementById('rr-style')) { var st = el('style', CSS); st.id = 'rr-style'; document.head.append(st); }
    root.replaceChildren(); root.classList.add('rr');
    var tip = el('div', null, 'rr-tip'); tip.hidden = true; root.append(tip);
    root.append(el('p', '갱신 ' + d.updated_at.replace('T', ' ').replace('+09:00', ' KST') + ' · 작성 ' + d.author, 'rr-note'));
    root.append(el('h3', '읽는 법'), (function () { var u = el('ul', null, 'rr-rules'); d.how_to_read.forEach(function (t) { u.append(el('li', t)); }); return u; })());
    if (d.answer_flow) root.append(el('h3', '답변 흐름'), flowBlock(d, tip));
    if (d.evening_tests) root.append(el('h3', '답변 연결 뒤 시험'), eveningBlock(d));
    root.append(el('h3', '추이 — 실제 질문 10개'), trendBlock(d, tip));
    root.append(el('h3', '실행 기록'));
    var tabs = el('div', null, 'rr-tabs'), holder = el('div');
    function show(id) {
      Array.prototype.forEach.call(tabs.children, function (b) { b.setAttribute('aria-pressed', String(b.dataset.id === id)); });
      holder.replaceChildren(runDetail(d.run_sets.filter(function (s) { return s.id === id; })[0], d.stages));
    }
    d.run_sets.slice().reverse().forEach(function (s) { var b = el('button', (s.period === 'latest' ? '최신 · ' : '') + s.label); b.dataset.id = s.id; b.type = 'button'; b.onclick = function () { show(s.id); }; tabs.append(b); });
    root.append(tabs, holder);
    var latest = d.run_sets.filter(function (s) { return s.period === 'latest'; })[0] || d.run_sets[d.run_sets.length - 1];
    show(latest.id);
    root.append(el('h3', '증거의 종류 — 섞어 세지 않는다'));
    var wrap = el('div', null, 'rr-scroll'), tb = el('table'), hd = el('tr');
    ['종류', '무엇을 보는가', '예', '보여 주지 못하는 것'].forEach(function (h) { hd.append(el('th', h)); }); tb.append(hd);
    d.evidence_classes.forEach(function (c) { var tr = el('tr'); tr.append(el('td', c['class']), el('td', c.means), el('td', c.examples.join(' / ')), el('td', c.does_not_show)); tb.append(tr); });
    wrap.append(tb); root.append(wrap);
    root.append(el('h3', '지금 · 계획 · 확장 · 실험'));
    var sp = el('div', null, 'rr-split');
    [['지금 확인된 것', 'current'], ['계획(구현·평가 전)', 'planned'], ['확장 대상', 'expansion'], ['실험(효용 미입증)', 'experiment']].forEach(function (p) { var c = el('div', null, 'rr-card'); c.append(el('h4', p[0]), list(d.status_split[p[1]])); sp.append(c); });
    root.append(sp, el('p', d.excluded_from_public, 'rr-note'));
  }

  window.RunsReview = { mount: mount };
  document.addEventListener('DOMContentLoaded', function () { var auto = document.querySelector('[data-runs-review]'); if (auto) mount(auto); });
})();
