/* 한 페이지 — 흐름(runs-review) × 구조(atlas data.js) × 진행(tracks) · 작성 Sarah
   읽는 데이터: window.RUNS_REVIEW.answer_flow.stages / .onepage, window.ATLAS.nodes
   그리기만 한다 — 질문 재실행·모델 호출·외부 주소 호출 없음. */
(function () {
  'use strict';
  var CSS = [
    '.op{--ink:#192e35;--mute:#65757b;--line:#9fb0b5;--soft:#eef3f3;--tobe:#1f5a66;--asis:#8f4a2a;color:var(--ink);font-size:14px;line-height:1.45}',
    '.op section{border:1.5px dashed var(--line);padding:12px 12px 12px;margin:14px 0;position:relative;background:#fff}',
    '.op section>h2{position:absolute;top:-10px;left:10px;background:#fff;padding:0 6px;font-size:12px;letter-spacing:.06em;color:var(--mute);margin:0}',
    '.op .bar-top{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;margin:4px 0 2px}',
    '.op .toggle{display:inline-flex;border:1.5px solid var(--ink);border-radius:4px;overflow:hidden}.op .toggle button{border:0;background:#fff;padding:5px 12px;font:inherit;cursor:pointer;color:var(--ink)}.op .toggle button[aria-pressed=true]{background:var(--ink);color:#fff}',
    '.op .legend{display:flex;gap:10px;flex-wrap:wrap;font-size:12px;color:var(--mute)}.op .legend span::before{content:"";display:inline-block;width:10px;height:10px;border:1.5px solid var(--line);margin-right:4px;vertical-align:-1px}.op .legend .l-tobe::before{background:var(--tobe);border-color:var(--tobe)}.op .legend .l-k::before{background:repeating-linear-gradient(45deg,#fff 0 2px,#9fb0b5 2px 4px)}.op .legend .l-prog::before{background:linear-gradient(90deg,#345 50%,#eee 50%)}',
    '.op .flow{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:8px}',
    '.op .stage{border:1.5px solid var(--ink);border-radius:4px;padding:8px;min-height:160px;position:relative;background:#fff;text-decoration:none;color:inherit;display:block}.op .stage:hover{background:#f4f8f8}',
    '.op .stage .id{font-size:11px;color:var(--mute)}.op .stage .nm{font-weight:700}.op .stage .goal{font-size:11px;color:var(--mute);margin-top:4px;min-height:30px}',
    '.op .stage.weak{border-color:#8a6d1f}.op .stage.fail{border-color:#8f2020}.op .stage .st{font-size:10px;position:absolute;left:8px;bottom:6px;color:var(--mute)}',
    '.op .bar{height:6px;border:1px solid var(--line);margin-top:6px;background:#fff}.op .bar i{display:block;height:100%;background:#345}.op .pct{font-size:11px;color:var(--mute)}',
    '.op .badge{position:absolute;top:-9px;right:6px;font-size:11px;padding:0 6px;border:1.5px solid var(--tobe);border-radius:3px;background:#fff;color:var(--tobe);font-weight:700;display:none}.op.tobe .badge{display:inline-block}',
    '.op .mods{margin-top:6px;margin-bottom:14px;display:flex;flex-wrap:wrap;gap:3px}.op .mods b{font-weight:500;font-size:10px;border:1px solid var(--line);padding:0 4px;color:#333;background:var(--soft);border-radius:2px}',
    '.op .shadow{margin-top:6px;border:1.5px dashed var(--tobe);padding:3px 5px;font-size:11px;color:var(--tobe);display:none}.op.tobe .shadow{display:block}.op .note-asis{margin-top:6px;font-size:11px;color:var(--asis)}.op.tobe .note-asis{display:none}',
    '.op .arch{display:grid;grid-template-columns:1.1fr 1fr 1.3fr .8fr;gap:10px}.op .col{border:1px solid var(--line);border-radius:4px;padding:8px}.op .col h3{margin:0 0 6px;font-size:12px;color:var(--mute);font-weight:600}',
    '.op .mod{display:block;border:1.5px solid var(--ink);border-radius:4px;padding:6px 8px;margin-bottom:6px;background:#fff;position:relative;text-decoration:none;color:inherit}.op .mod:hover{background:#f4f8f8}.op .mod .nm{font-weight:700;font-size:13px}.op .mod .ds{font-size:11px;color:var(--mute)}',
    '.op .mod .st{font-size:10px;margin-top:3px;display:flex;gap:3px;flex-wrap:wrap}.op .mod .st b{font-weight:500;border:1px solid var(--line);padding:0 4px;background:var(--soft);border-radius:2px}.op .mod.k{background:repeating-linear-gradient(45deg,#fff 0 6px,#f1f4f4 6px 12px)}.op .mod.gray{border-style:dotted;color:var(--mute)}',
    '.op .mod .tag{position:absolute;top:-8px;right:6px;font-size:10px;border:1.5px solid var(--tobe);border-radius:3px;color:var(--tobe);background:#fff;padding:0 4px;display:none}.op.tobe .mod .tag{display:inline-block}.op .mod.k .tag{display:inline-block;border-color:var(--mute);color:var(--mute)}',
    '.op .hl .stage,.op .hl .mod{opacity:.35}.op .hl .stage.on,.op .hl .mod.on{opacity:1;box-shadow:0 0 0 2px #345 inset}',
    '.op .board{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:6px}.op .card{display:block;border:1px solid var(--ink);border-radius:4px;padding:6px;min-height:92px;font-size:12px;background:#fff;text-decoration:none;color:inherit}.op .card .t{font-weight:700}.op .card .s{display:inline-block;font-size:10px;border:1px solid var(--line);padding:0 4px;margin:4px 0;background:var(--soft);border-radius:2px}.op .card .d{font-size:11px;color:var(--mute)}.op .card.k{background:repeating-linear-gradient(45deg,#fff 0 6px,#f1f4f4 6px 12px)}',
    '.op .foot{font-size:11px;color:var(--mute);margin-top:8px}.op details{margin-top:8px;font-size:12px}.op summary{cursor:pointer;color:#345}',
    '.op .truth{display:inline-flex;gap:4px;flex-wrap:wrap;margin-top:4px}.op .truth i{font-style:normal;font-size:9px;padding:0 4px;border:1px solid var(--line);border-radius:2px;color:#333;background:#fff}.op .truth i.observed{border-color:#345;color:#345}.op .truth i.pinned{border-color:#147360;color:#147360}.op .truth i.agreed{border-color:#8a6d1f;color:#8a6d1f}.op .truth i.proposed{border-style:dashed;color:var(--tobe);border-color:var(--tobe)}',
    '@media (max-width:1100px){.op .flow{grid-template-columns:repeat(4,1fr)}.op .arch{grid-template-columns:1fr 1fr}.op .board{grid-template-columns:repeat(3,1fr)}}',
    '@media (max-width:600px){.op .flow{grid-template-columns:1fr 1fr}.op .arch{grid-template-columns:1fr}.op .board{grid-template-columns:1fr 1fr}}'
  ].join('\n');

  function el(tag, text, cls) { var e = document.createElement(tag); if (text != null) e.textContent = text; if (cls) e.className = cls; return e; }
  function chip(t) { return el('b', t); }
  // R3 표지 칩: as_of · truth · evidence — atlas-model.js(기계 생성)에서 읽는다. 없으면 그리지 않는다.
  var TRUTH = { observed: '관측', pinned: '코드 고정', agreed: '합의', proposed: '제안' };
  function modelEntity(id) { var M = window.ATLAS_MODEL; if (!M) return null; for (var i = 0; i < M.entities.length; i++) if (M.entities[i].id === id) return M.entities[i]; return null; }
  function truthChips(id) {
    var e = modelEntity(id); if (!e) return null;
    var box = el('span', null, 'truth'), t = el('i', TRUTH[e.truth] || e.truth, e.truth); t.title = 'truth: ' + e.truth; box.append(t);
    if (e.as_of) box.append(el('i', e.as_of));
    var ev = e.evidence || {}, label = ev.commit ? 'commit ' + String(ev.commit).slice(0, 7) + (ev.file ? ' · ' + ev.file.split('/').pop() + (ev.line ? ':' + ev.line : '') : '') : ev.code_pin ? 'pin ' + ev.code_pin : ev.run_set ? 'run ' + ev.run_set : ev.run_sets && ev.run_sets.length ? 'run ' + ev.run_sets[0] : ev.doc ? ev.doc : '';
    if (label) { var v = el('i', label); v.title = JSON.stringify(ev); box.append(v); }
    return box;
  }

  function mount(root) {
    var d = window.RUNS_REVIEW, A = window.ATLAS, op = d && d.onepage; if (!root || !op) { if (root) root.textContent = '한 페이지 데이터(onepage)가 기록 파일에 없다.'; return; }
    if (!document.getElementById('op-style')) { var st = el('style', CSS); st.id = 'op-style'; document.head.append(st); }
    root.replaceChildren(); root.classList.add('op');
    var nodeTitle = {}; (A && A.nodes || []).forEach(function (n) { nodeTitle[n.id] = n.title; });

    // 상단: 토글·범례
    var top = el('div', null, 'bar-top');
    var tg = el('div', null, 'toggle'); tg.setAttribute('role', 'group'); tg.setAttribute('aria-label', '보기 전환');
    var bAs = el('button', 'AS-IS'), bTo = el('button', 'TO-BE 겹쳐 보기'); bAs.type = bTo.type = 'button';
    function set(t) { root.classList.toggle('tobe', t); bAs.setAttribute('aria-pressed', String(!t)); bTo.setAttribute('aria-pressed', String(t)); history.replaceState(null, '', t ? '#view=tobe' : '#view=asis'); }
    bAs.onclick = function () { set(false); }; bTo.onclick = function () { set(true); }; tg.append(bAs, bTo);
    var lg = el('div', null, 'legend'); lg.append(el('span', '실선 = 지금 있는 것'), el('span', '색 테두리 = TO-BE A~D 덧씌움', 'l-tobe'), el('span', '빗금 = Track K(온톨로지·KG)', 'l-k'), el('span', '막대 = ' + (d.day_log_1108 ? '11/8 목표 대비 진행' : d.day_log_1107 ? '11/7 목표 대비 진행' : '목표 대비 진행'), 'l-prog'));
    if (window.ATLAS_MODEL) { var M = window.ATLAS_MODEL, ltr = el('span', null, 'truth'); Object.keys(TRUTH).forEach(function (k) { var i = el('i', TRUTH[k] + ' ' + (M.counts.by_truth[k] || 0), k); ltr.append(i); }); var wrap = el('span', '표지(엔티티 ' + M.counts.entities + ' · 관계 ' + M.counts.relations + '): '); wrap.append(ltr); lg.append(wrap); }
    top.append(tg, lg); root.append(el('p', '갱신 ' + d.updated_at.replace('T', ' ').replace('+09:00', ' KST') + ' · 기준일 ' + op.as_of + ' · ' + op.note, 'sub'), top);

    // 하이라이트: 단계 ↔ 모듈 ↔ 보드 칸을 이름으로 잇는다
    var stageEls = {}, modEls = [];
    function highlight(stages) {
      if (!stages) { root.classList.remove('hl'); Object.keys(stageEls).forEach(function (k) { stageEls[k].classList.remove('on'); }); modEls.forEach(function (m) { m.el.classList.remove('on'); }); return; }
      root.classList.add('hl');
      Object.keys(stageEls).forEach(function (k) { stageEls[k].classList.toggle('on', stages.indexOf(k) >= 0); });
      modEls.forEach(function (m) { m.el.classList.toggle('on', m.stages.some(function (s) { return stages.indexOf(s) >= 0; })); });
    }

    // 1 · 흐름
    var s1 = el('section'); s1.append(el('h2', '1 · 흐름 — 질문이 답이 되기까지 ' + d.answer_flow.stages.length + '단계'));
    var flow = el('div', null, 'flow');
    d.answer_flow.stages.forEach(function (s) {
      var m = op.stage_meta[s.id] || {}, a = el('a', null, 'stage ' + (s.state || ''));
      a.href = 'runs-review.html'; a.title = (s.quality || '') + (s.fix ? ' · 고칠 것: ' + s.fix : '');
      if (m.tobe) a.append(el('span', m.tobe.tag, 'badge'));
      a.append(el('div', s.id, 'id'), el('div', s.name, 'nm'), el('div', '목표: ' + (m.goal || '—'), 'goal'));
      if (m.ratio) { var bar = el('div', null, 'bar'), fill = el('i'); fill.style.width = (m.ratio[1] ? Math.round(100 * m.ratio[0] / m.ratio[1]) : 0) + '%'; bar.append(fill); a.append(bar, el('div', m.ratio[0] + '/' + m.ratio[1] + (m.extra ? ' · ' + m.extra : ''), 'pct')); }
      var mods = el('div', null, 'mods'); (m.modules || []).forEach(function (id) { mods.append(chip(nodeTitle[id] || id)); }); a.append(mods);
      if (m.tobe) a.append(el('div', m.tobe.tag.split(' ')[0] + ': ' + m.tobe.text, 'shadow'));
      if (m.asis && m.asis !== '현행') a.append(el('div', m.asis, 'note-asis'));
      var tc = truthChips('stage:' + s.id); if (tc) a.append(tc);
      a.append(el('span', '상태 ' + ({ ok: '정상', weak: '약함', fail: '실패' }[s.state] || s.state || ''), 'st'));
      a.onmouseenter = function () { highlight([s.id]); }; a.onmouseleave = function () { highlight(null); };
      stageEls[s.id] = a; flow.append(a);
    });
    s1.append(flow, el('p', '읽는 법: 칸 안 회색 칩이 아래 「구조」 모듈 이름과 같다 — 선을 긋지 않고 이름으로 잇는다. 칸에 마우스를 올리면 떠받치는 모듈이 밝아진다. 칸을 누르면 실행 기록 페이지로 간다.', 'foot'));
    root.append(s1);

    // 2 · 구조
    var s2 = el('section'); s2.append(el('h2', '2 · 구조 — 무엇이 무엇을 떠받치나(왼쪽이 규칙, 오른쪽이 실행)'));
    var arch = el('div', null, 'arch');
    op.structure.forEach(function (c) {
      var col = el('div', null, 'col'); col.append(el('h3', c.title));
      c.modules.forEach(function (m) {
        var a = el('a', null, 'mod' + (m.k ? ' k' : '') + (m.gray ? ' gray' : ''));
        a.href = m.link || (m.node ? 'index.html#node=' + m.node : 'index.html');
        if (m.tag) a.append(el('span', m.tag, 'tag'));
        a.append(el('div', m.label, 'nm'), el('div', m.desc + (m.node && nodeTitle[m.node] ? ' · atlas: ' + nodeTitle[m.node] : ''), 'ds'));
        var st = el('div', null, 'st'); m.stages.forEach(function (s) { st.append(chip(s)); }); a.append(st);
        var mc = truthChips('module:' + m.label.replace(/[^0-9A-Za-z가-힣]+/g, '-').replace(/^-|-$/g, '')); if (mc) a.append(mc);
        a.onmouseenter = function () { highlight(m.stages); }; a.onmouseleave = function () { highlight(null); };
        modEls.push({ el: a, stages: m.stages }); col.append(a);
      });
      arch.append(col);
    });
    s2.append(arch, el('p', '모듈을 누르면 시스템 보드(index.html)의 그 노드 절차로 간다. 빗금 모듈은 Track K — 아직 제품 노드가 아니라 보드·관계 지도로 연결된다.', 'foot'));
    root.append(s2);

    // 3 · 진행
    var s3 = el('section'); s3.append(el('h2', '3 · 진행 — TO-BE A~D · Track K (한 칸 = 한 작업 · 상태는 기록 기준)'));
    var board = el('div', null, 'board');
    op.tracks.forEach(function (t) {
      var a = el('a', null, 'card' + (t.k ? ' k' : '')); a.href = t.run ? 'runs-review.html#run=' + t.run : 'index.html#tab=kanban';
      a.append(el('div', t.title, 't'), el('span', t.status, 's'), el('div', t.desc, 'd'));
      var kc = truthChips('track:' + t.id); if (kc) a.append(kc);
      if (t.stages) { a.onmouseenter = function () { highlight(t.stages); }; a.onmouseleave = function () { highlight(null); }; }
      board.append(a);
    });
    s3.append(board);
    if (op.day_log) { var dt = el('details'); dt.append(el('summary', '일지(토글) — 날짜별 요약')); op.day_log.forEach(function (x) { dt.append(el('p', x.day + ': ' + x.text, 'd')); }); s3.append(dt); }
    s3.append(el('p', '배정안은 사용자 확인 뒤 — 이 보드는 「무엇이 어디까지 왔나」만 보여준다. 칸을 누르면 실행 기록(run_set) 또는 작업 보드로 간다.', 'foot'));
    root.append(s3);

    set(location.hash.indexOf('view=tobe') >= 0);
  }
  window.OnePage = { mount: mount };
})();
