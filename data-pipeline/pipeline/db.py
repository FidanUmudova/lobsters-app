"""
============================================================
DATABASE CONNECTION — db.py
============================================================
Responsibility: Creates the SQLAlchemy engine and session that
the rest of the pipeline uses to talk to lobsters.db.

This is plumbing, not business logic — you only need to
understand it, not necessarily write all of it from scratch.
Some of it is already done for you. Read the TODOs carefully.
============================================================
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pipeline.models import Base

# The SQLite database file lives at the project root, shared
# between the pipeline and the backend.
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "lobsters.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# The engine is the entry point to the database.
# echo=False keeps the console quiet; set True for debugging SQL.
engine = create_engine(DATABASE_URL, echo=False)

# A configured "Session" class. Each instance is a single
# conversation with the database (think: one transaction).
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()
