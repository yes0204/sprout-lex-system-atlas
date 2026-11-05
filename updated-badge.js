/* 페이지 오른쪽 위 「갱신 시각」 표시 (작성: Sarah · 공통 파일과 독립 · 외부 호출 없음)
   시각의 출처
   - 실행 기록 페이지: 기록 데이터의 updated_at(내용을 고친 시각)
   - 그 밖의 페이지: 브라우저가 받은 이 페이지 파일의 최종 수정 시각(document.lastModified = 배포 시각)
   둘 다 한국 시간(KST)으로 보인다. */
(function () {
  'use strict';
  function kst(d) {
    var k = new Date(d.getTime() + 9 * 3600 * 1000), p = function (n) { return (n < 10 ? '0' : '') + n; };
    return k.getUTCFullYear() + '-' + p(k.getUTCMonth() + 1) + '-' + p(k.getUTCDate()) + ' ' + p(k.getUTCHours()) + ':' + p(k.getUTCMinutes()) + ' KST';
  }
  function show() {
    if (document.getElementById('updated-badge')) return;
    var label, title;
    var rr = window.RUNS_REVIEW && window.RUNS_REVIEW.updated_at;
    if (rr) {
      label = '갱신 ' + rr.replace('T', ' ').replace('+09:00', ' KST');
      title = '기록 내용을 마지막으로 고친 시각';
    } else {
      var d = new Date(document.lastModified);
      if (isNaN(d.getTime())) return;
      label = '갱신 ' + kst(d);
      title = '이 페이지 파일이 마지막으로 배포된 시각';
    }
    var b = document.createElement('div');
    b.id = 'updated-badge'; b.textContent = label; b.title = title;
    b.setAttribute('role', 'status');
    var pill = 'font:600 12px/1.4 system-ui,-apple-system,"Segoe UI","Malgun Gothic",sans-serif;color:#192e35;background:#fff;border:1px solid #dce3e4;border-radius:14px;padding:4px 10px;white-space:nowrap;box-shadow:0 1px 2px rgba(25,46,53,.06)';
    // 머리 막대의 오른쪽 링크 묶음이 있으면 그 맨 앞에 끼워 링크를 가리지 않는다(시스템 보드). 없으면 페이지 오른쪽 위에 둔다.
    var links = document.querySelector('header.masthead .header-links');
    if (links) {
      b.style.cssText = pill + ';display:inline-block;margin:0 10px 4px 0;vertical-align:middle';
      links.insertBefore(b, links.firstChild);
    } else {
      b.style.cssText = pill + ';position:absolute;top:10px;right:16px;z-index:30';
      document.body.appendChild(b);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', show); else show();
})();
