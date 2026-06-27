"""
============================================================
PIPELINE LAYER 3 — LOADER
============================================================
Role: Data Engineer

Responsibility: Take the CLEAN list of post dicts (from transformer.py)
and write them into the SQLite database using SQLAlchemy.

This layer does NOT know about Lobsters' JSON format and does NOT
do any network calls. It only knows how to save/update rows.

Why a separate layer for this?
  - The transform step doesn't need to know HOW data is stored.
  - We can swap SQLite for PostgreSQL later by only touching db.py
    and this file — fetcher.py and transformer.py stay untouched.

UPSERT LOGIC:
  Posts can be fetched more than once (e.g. running the pipeline daily).
  If a post_id already exists in the database, UPDATE its score and
  num_comments (since those change over time) instead of inserting
  a duplicate row.
============================================================
"""

from pipeline.models import Post
from pipeline.db import get_session


def load_posts(posts: list) -> dict:
    session = get_session()

    inserted = 0
    updated = 0

    for post in posts:
        existing = (
            session.query(Post)
            .filter_by(post_id=post["post_id"])
            .first()
        )

        if existing:
            existing.score = post["score"]
            existing.num_comments = post["num_comments"]
            updated += 1
        else:
            new_post = Post(
                post_id=post["post_id"],
                title=post["title"],
                author=post["author"],
                score=post["score"],
                num_comments=post["num_comments"],
                url=post["url"],
                permalink=post["permalink"],
                created_utc=post["created_utc"],
                fetched_at=post["fetched_at"],
            )

            session.add(new_post)
            inserted += 1

    session.commit()
    session.close()

    return {
        "inserted": inserted,
        "updated": updated,
        "total": len(posts),
    }
