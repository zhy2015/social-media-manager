#!/usr/bin/env python3
import json
import sys
from urllib.parse import urlparse


def normalize_items(lines):
    items = []
    for i, line in enumerate(lines, 1):
        text = (line or '').strip()
        if not text:
            continue
        items.append({
            'rank': i,
            'title': text,
            'hot': None,
            'tags': [],
            'url': None,
        })
    return items


def main():
    data = sys.stdin.read().strip().splitlines()
    items = normalize_items(data)
    print(json.dumps({'ok': True, 'count': len(items), 'items': items}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
