"""Collect Hacker News comments into collected.csv for hand labelling.

Uses only the official HN Algolia API. Usernames and links to users are
never saved. The label and note columns are left empty for you to fill in.
"""
import csv
import html
import re
import sys
import time

import requests

API_URL = "https://hn.algolia.com/api/v1/search_by_date"
QUERIES = ["nba", "basketball", "football", "gaming", "movies"]
PAGES_PER_QUERY = 2
HITS_PER_PAGE = 100
MIN_CHARS = 120
MAX_CHARS = 1200
MAX_ROWS = 200
PAUSE = 1
OUT_FILE = "collected.csv"

TAG_RE = re.compile(r"<[^>]+>")


class ApiError(Exception):
    pass


def fetch(query, page):
    """GET one page of comment hits. Raises ApiError on any failure."""
    time.sleep(PAUSE)
    params = {"query": query, "tags": "comment", "hitsPerPage": HITS_PER_PAGE, "page": page}
    try:
        resp = requests.get(API_URL, params=params, timeout=30)
    except requests.RequestException as e:
        raise ApiError(f"Request failed for query {query!r} page {page}: {e}")
    if resp.status_code != 200:
        raise ApiError(f"API returned {resp.status_code} for query {query!r} page {page}: {resp.text[:200]}")
    return resp.json()["hits"]


def clean(comment_html):
    # Turn paragraph and line breaks into newlines before dropping the rest of the tags.
    text = re.sub(r"<(p|br)\s*/?>", "\n", comment_html or "")
    text = html.unescape(TAG_RE.sub("", text))
    return text.strip()


def main():
    rows, seen = [], set()
    try:
        for query in QUERIES:
            for page in range(PAGES_PER_QUERY):
                if len(rows) >= MAX_ROWS:
                    break
                for hit in fetch(query, page):
                    text = clean(hit.get("comment_text"))
                    if text in ("[deleted]", "[dead]"):
                        continue
                    if not MIN_CHARS <= len(text) <= MAX_CHARS:
                        continue
                    if text in seen:
                        continue
                    seen.add(text)
                    rows.append(text)
                    if len(rows) >= MAX_ROWS:
                        break
                print(f"  {query} page {page}: {len(rows)} rows so far")
    except ApiError as e:
        print(f"{e}. Stopping without retrying.")
        if not rows:
            sys.exit(1)
        print(f"Saving the {len(rows)} rows collected before the error.")

    with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label", "note"])
        for text in rows:
            writer.writerow([text, "", ""])
    print(f"Saved {len(rows)} rows to {OUT_FILE}")


if __name__ == "__main__":
    main()
