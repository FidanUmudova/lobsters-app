"""
============================================================
PIPELINE LAYER 2 — TRANSFORMER
============================================================
Role: Data Engineer

Responsibility: Take the RAW Lobsters JSON (from fetcher.py) and turn
it into a clean list of plain Python dicts that match our database
schema exactly (see pipeline/models.py).

This layer does NOT touch the network and does NOT touch the database.
It is pure data transformation — easy to test, easy to reason about.

Why a separate layer for this?
  - Lobsters' raw JSON has fields we don't need and some nesting
    (like submitter_user) we wangrep -n ">>>>>\|<<<<<\|=====" pipeline/transformer.pyt flattened. This layer is the ONE
    place that knows how to translate "Lobsters' shape" into "our
    shape".
  - If our database schema changes, only this file (and models.py)
    need to change — not the fetcher.
============================================================
"""
from datetime import datetime, timezone


def transform_post(raw_post_data: dict) -> dict:
    parsed = datetime.fromisoformat(raw_post_data["created_at"])

    author_data = raw_post_data.get("submitter_user")

    if isinstance(author_data, dict):
        author = author_data.get("username")
    else:
        author = author_data

    return {
        "post_id": raw_post_data["short_id"],
        "title": raw_post_data["title"],
        "author": author,
        "score": raw_post_data["score"],
        "num_comments": raw_post_data["comment_count"],
        "url": raw_post_data["url"],
        "permalink": raw_post_data["comments_url"],
        "created_utc": parsed.timestamp(),
        "fetched_at": datetime.now(timezone.utc),
    }


def transform_posts(raw_json: list, limit: int = 10) -> list:
    return [transform_post(post) for post in raw_json[:limit]]