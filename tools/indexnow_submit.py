#!/usr/bin/env python
"""
indexnow_submit.py — notify Bing/Yandex/Naver/Seznam of new or updated URLs.

Usage:
  python tools/indexnow_submit.py /insights/my-post/ /ms/insights/my-post/
"""

import os
import sys
import json
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

HUGO_ROOT = Path(__file__).parent.parent
load_dotenv(HUGO_ROOT / ".env")

HOST = "drnorfaizal.com"
BASE_URL = f"https://{HOST}"
ENDPOINT = "https://api.indexnow.org/indexnow"


def submit(paths: list[str]) -> None:
    key = os.environ.get("INDEXNOW_KEY")
    if not key:
        sys.exit("INDEXNOW_KEY not found in .env")

    url_list = [f"{BASE_URL}{p}" if p.startswith("/") else p for p in paths]

    payload = json.dumps({
        "host": HOST,
        "key": key,
        "keyLocation": f"{BASE_URL}/{key}.txt",
        "urlList": url_list,
    }).encode("utf-8")

    req = urllib.request.Request(
        ENDPOINT, data=payload, method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(req) as resp:
        print(f"IndexNow response: {resp.status} {resp.reason}")
        for u in url_list:
            print(f"  submitted: {u}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python tools/indexnow_submit.py <path> [<path> ...]")
    submit(sys.argv[1:])
