#!/usr/bin/env python3
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

OUTPUT_DIR = Path('/Users/hidream/.openclaw/workspace/output/douyin-download')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def pick_ytdlp() -> str | None:
    candidates = [
        'yt-dlp',
        '/opt/homebrew/bin/yt-dlp',
        str(Path.home() / '.local' / 'bin' / 'yt-dlp'),
        str(Path.home() / 'Library' / 'Python' / '3.9' / 'bin' / 'yt-dlp'),
    ]
    for c in candidates:
        code, out, err = run(['bash', '-lc', f'command -v {c} >/dev/null 2>&1 && printf %s {c}']) if '/' not in c else (0 if Path(c).exists() else 1, c, '')
        if code == 0:
            return c
    return None


def extract_aweme_id(text: str) -> str | None:
    patterns = [
        r'/video/(\d+)',
        r'modal_id=(\d+)',
        r'note/(\d+)',
        r'aweme_id=(\d+)',
        r'group_id=(\d+)',
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(1)
    try:
        u = urlparse(text)
        q = parse_qs(u.query)
        for key in ('modal_id', 'aweme_id', 'group_id'):
            if key in q and q[key]:
                return q[key][0]
    except Exception:
        pass
    return None


def choose_output_path(aweme_id: str | None) -> Path:
    if aweme_id:
        return OUTPUT_DIR / f'{aweme_id}.mp4'
    idx = 1
    while True:
        p = OUTPUT_DIR / f'douyin-video-{idx}.mp4'
        if not p.exists():
            return p
        idx += 1


def probe_duration_ms(path: Path) -> int | None:
    code, out, err = run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(path),
    ])
    if code != 0:
        return None
    try:
        return int(float(out.strip()) * 1000)
    except Exception:
        return None


def main():
    if len(sys.argv) < 2:
        print('usage: download_douyin_video.py <share_link_or_url> [output_path] [cookies.txt]', file=sys.stderr)
        sys.exit(2)

    source = sys.argv[1].strip()
    aweme_id = extract_aweme_id(source)
    output_path = Path(sys.argv[2]).expanduser() if len(sys.argv) >= 3 and sys.argv[2].strip() else choose_output_path(aweme_id)
    cookies_path = Path(sys.argv[3]).expanduser() if len(sys.argv) >= 4 and sys.argv[3].strip() else None
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ytdlp = pick_ytdlp()
    if not ytdlp:
        print(json.dumps({
            'ok': False,
            'source': source,
            'aweme_id': aweme_id,
            'output_path': str(output_path),
            'error': 'yt-dlp not found; install it first',
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    cmd = [
        ytdlp,
        '--no-playlist',
        '--no-progress',
    ]
    if cookies_path:
        cmd += ['--cookies', str(cookies_path)]
    cmd += [
        '-o', str(output_path),
        source,
    ]
    code, out, err = run(cmd)
    if code != 0:
        print(json.dumps({
            'ok': False,
            'source': source,
            'aweme_id': aweme_id,
            'output_path': str(output_path),
            'error': err.strip() or out.strip() or 'yt-dlp failed',
            'cookies_path': str(cookies_path) if cookies_path else None,
            'command': cmd,
        }, ensure_ascii=False, indent=2))
        sys.exit(code)

    final_path = output_path
    if not final_path.exists():
        matches = sorted(output_path.parent.glob(output_path.name + '*'))
        if matches:
            final_path = matches[0]

    if not final_path.exists():
        print(json.dumps({
            'ok': False,
            'source': source,
            'aweme_id': aweme_id,
            'output_path': str(output_path),
            'error': 'download finished but output file not found',
            'command': cmd,
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    duration_ms = probe_duration_ms(final_path)
    print(json.dumps({
        'ok': True,
        'source': source,
        'aweme_id': aweme_id,
        'output_path': str(final_path),
        'size_bytes': final_path.stat().st_size,
        'duration_ms': duration_ms,
        'cookies_path': str(cookies_path) if cookies_path else None,
        'command': cmd,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
