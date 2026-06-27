"""
============================================================
BACKEND LAYER 1 — REPOSITORY
============================================================
Role: Backend Developer

Responsibility: This is the ONLY layer that writes database queries
(session.query(...)). It knows how to ask the database for posts,
but it does NOT know about HTTP, JSON, or Flask routes.

Why a separate layer for this?
  - If we ever swap SQLite for PostgreSQL, only db.py changes.
  - If our query logic gets complex (filters, pagination), it stays
    contained here instead of cluttering the API routes.
  - We can unit-test queries directly, without spinning up a server.
============================================================
"""

from app.models import Post
from app.db import get_session


def get_top_posts(limit: int = 10) -> list:
    """
    Fetches the top N posts ordered by score, highest first.

    Args:
        limit (int): How many posts to return. Default 10.

    Returns:
        list[Post]: A list of Post ORM objects, ordered by score descending.
    """
    session = get_session()

    posts = (
        session.query(Post)
        .order_by(Post.score.desc())
        .limit(limit)
        .all()
    )

    session.close()
    return posts


def get_post_by_id(post_id: str):
    """
    Fetches a single post by its Lobsters post_id.

    Args:
        post_id (str): The Lobsters post_id, e.g. "1abcde"

    Returns:
        Post | None: The matching Post object, or None if not found.
    """
    session = get_session()

    post = session.query(Post).filter_by(post_id=post_id).first()

    session.close()
    return post


def count_posts() -> int:
    """
    Returns the total number of posts currently stored in the database.
    Useful for a health-check or stats endpoint.

    Returns:
        int: Total row count in the posts table.
    """
    session = get_session()

    count = session.query(Post).count()

    session.close()
    return count