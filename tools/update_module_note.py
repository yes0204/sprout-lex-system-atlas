"""담당 모듈 메모 갱신기 — module-notes.json 을 고치고 module-notes-data.js 를 다시 만든다(표준 라이브러리만).

작업을 끝낸 담당자(또는 대행)가 한 줄로 갱신한다:
  python tools/update_module_note.py --module alice --latest "04 무결성 보류 원인 확인(핀 abc1234)" --source "PR357 abc1234"
  python tools/update_module_note.py --module david --fix "따옴표 규칙 정밀화 완료 · 다음: 호 단위 unit" --status weak
  python tools/update_module_note.py --rebuild          # json 을 손으로 고친 뒤 data.js 만 다시 만들기

규칙: --latest 를 주면 이전 latest 는 history_log 맨 앞으로 내려간다(지우지 않는다). 시각은 실행 시각(KST)이다.
"""
import argparse, datetime, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON, DATA = ROOT / 'module-notes.json', ROOT / 'module-notes-data.js'
STATUS = {'ok', 'weak', 'fail'}


def now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M')


def write(d):
    JSON.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    DATA.write_text('/* 기계 생성 — module-notes.json 에서 tools/update_module_note.py 로 만든다. 직접 고치지 않는다. */\n'
                    'window.MODULE_NOTES = ' + json.dumps(d, ensure_ascii=False) + ';\n', encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--module')
    ap.add_argument('--fix', help='지금 고칠 곳(한두 문장)')
    ap.add_argument('--latest', help='방금 끝낸 일(한 문장)')
    ap.add_argument('--source', default='', help='근거 핀·문서')
    ap.add_argument('--status', choices=sorted(STATUS))
    ap.add_argument('--rebuild', action='store_true')
    a = ap.parse_args()
    d = json.loads(JSON.read_text(encoding='utf-8'))
    if not a.rebuild:
        mods = {m['id']: m for m in d['modules']}
        if a.module not in mods:
            sys.exit('모듈 id 는 ' + ', '.join(mods) + ' 중 하나다')
        m = mods[a.module]
        if a.fix: m['fix_now'] = a.fix
        if a.status: m['status'] = a.status
        if a.latest:
            if m.get('latest'): m.setdefault('history_log', []).insert(0, m['latest'])
            m['latest'] = {'at': now(), 'text': a.latest, 'source': a.source}
        if not (a.fix or a.status or a.latest):
            sys.exit('--fix · --latest · --status 중 하나는 있어야 한다')
        d['updated_at'] = now()
    write(d)
    print('갱신', d['updated_at'], '→', DATA.name)


if __name__ == '__main__':
    main()
