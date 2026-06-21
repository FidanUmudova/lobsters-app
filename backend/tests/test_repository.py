"""
============================================================
TESTS — Backend Layer 1: Repository
============================================================
Run with:  python tests/test_repository.py

These tests use a SEPARATE test database (test_lobsters.db), seeded
with known sample data, so results are predictable and don't depend
on your real lobsters.db or whether the pipeline has been run.
============================================================
"""

import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ─────────────────────────────────────────────
# SET UP AN ISOLATED, SEEDED TEST DATABASE
# ─────────────────────────────────────────────

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "test_lobsters.db")
if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

import app.db as db_module
db_module.DB_PATH = TEST_DB_PATH
db_module.DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
db_module.engine = create_engine(db_module.DATABASE_URL, echo=False)
db_module.SessionLocal = sessionmaker(bind=db_module.engine)

from app.models import Base, Post
Base.metadata.create_all(bind=db_module.engine)

# Seed with 3 known posts, different scores
seed_session = db_module.SessionLocal()
seed_session.add_all([
    Post(post_id="low123", title="Low score post", author="alice", score=10,
         num_comments=2, url="https://example.com/low", permalink="https://lobste.rs/s/low123/low-score-post",
         created_utc=1716000000.0, fetched_at=datetime.now(timezone.utc)),
    Post(post_id="mid456", title="Mid score post", author="bob", score=500,
         num_comments=50, url="https://example.com/mid", permalink="https://lobste.rs/s/mid456/mid-score-post",
         created_utc=1716000000.0, fetched_at=datetime.now(timezone.utc)),
    Post(post_id="high789", title="High score post", author="carol", score=9999,
         num_comments=400, url="https://example.com/high", permalink="https://lobste.rs/s/high789/high-score-post",
         created_utc=1716000000.0, fetched_at=datetime.now(timezone.utc)),
])
seed_session.commit()
seed_session.close()

from app import repository

# ─────────────────────────────────────────────
# TEST RUNNER HELPER
# ─────────────────────────────────────────────

passed = 0
failed = 0

def assert_that(label: str, condition: bool) -> None:
    global passed, failed
    if condition:
        print(f"  ✅ PASS — {label}")
        passed += 1
    else:
        print(f"  ❌ FAIL — {label}")
        failed += 1

# ─────────────────────────────────────────────
# TEST A — get_top_posts() ordering and limit
# ─────────────────────────────────────────────

print("TEST A: get_top_posts()")

top_2 = repository.get_top_posts(limit=2)
assert_that("Returns a list", isinstance(top_2, list))
assert_that("Respects the limit argument", len(top_2) == 2)
assert_that("Highest score comes first", top_2[0].post_id == "high789")
assert_that("Second highest comes second", top_2[1].post_id == "mid456")

top_all = repository.get_top_posts(limit=10)
assert_that("limit larger than dataset returns all rows", len(top_all) == 3)
assert_that("Lowest score post is last when limit covers everything", top_all[2].post_id == "low123")

print()

# ─────────────────────────────────────────────
# TEST B — get_post_by_id()
# ─────────────────────────────────────────────

print("TEST B: get_post_by_id()")

found = repository.get_post_by_id("mid456")
assert_that("Found post is not None", found is not None)
assert_that("Found post has correct title", found.title == "Mid score post")

not_found = repository.get_post_by_id("does_not_exist")
assert_that("Returns None for unknown post_id", not_found is None)

print()

# ─────────────────────────────────────────────
# TEST C — count_posts()
# ─────────────────────────────────────────────

print("TEST C: count_posts()")

total = repository.count_posts()
assert_that("Counts all 3 seeded posts", total == 3)

print()

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────

print("─" * 45)
print(f"Results: {passed} passed, {failed} failed")
if failed == 0:
    print("🎉 All repository tests passed!")
else:
    print("⚠️  Some tests failed. Complete the TODOs in app/repository.py")

if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)
