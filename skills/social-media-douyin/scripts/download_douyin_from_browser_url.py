#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
import urllib.request
from pathlib import Path
import subprocess

OUTPUT_DIR = Path('/Users/hidream/.openclaw/workspace/output/douyin-download')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def probe_duration_ms(path: Path) -> int | None:
    p = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(path),
    ], capture_output=True, text=True)
    if p.returncode != 0:
        return None
    try:
        return int(float(p.stdout.strip()) * 1000)
    except Exception:
        return None


def main():
    if len(sys.argv) < 3:
        print('usage: download_douyin_from_browser_url.py <media_url> <aweme_id> [output_path]', file=sys.stderr)
        sys.exit(2)

    media_url = sys.argv[1].strip()
    aweme_id = sys.argv[2].strip()
    output_path = Path(sys.argv[3]).expanduser() if len(sys.argv) >= 4 and sys.argv[3].strip() else OUTPUT_DIR / f'{aweme_id}.mp4'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    req = urllib.request.Request(media_url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'Referer': f'https://www.douyin.com/video/{aweme_id}',
    })

    with urllib.request.urlopen(req, timeout=120) as resp, open(output_path, 'wb') as f:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)

    duration_ms = probe_duration_ms(output_path)
    print(json.dumps({
        'ok': True,
        'aweme_id': aweme_id,
        'media_url': media_url,
        'output_path': str(output_path),
        'size_bytes': output_path.stat().st_size,
        'duration_ms': duration_ms,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
