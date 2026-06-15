#!/usr/bin/env python
"""
Database initialization script.
Creates all tables in the database based on SQLAlchemy models.

Usage:
    python init_db.py
"""

from app.database import Base, engine
from app.models import Shipment


def init_db():
    """Initialize database by creating all tables"""
    print("Creating database tables...")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully!")
        print("\nTables created:")
        print("  - shipments")
        return True
    except Exception as e:
        print(f"✗ Error creating database tables: {e}")
        return False


if __name__ == "__main__":
    success = init_db()
    exit(0 if success else 1)
