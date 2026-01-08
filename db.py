# db.py
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, List

DB_PATH = Path("data/app.db")

def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_conn()
    try:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            uploaded_at TEXT NOT NULL,
            sha256 TEXT NOT NULL UNIQUE,
            phash TEXT NOT NULL
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_images_sha256 ON images(sha256);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_images_uploaded_at ON images(uploaded_at);")
        conn.commit()
    finally:
        conn.close()

def count_images() -> int:
    conn = get_conn()
    try:
        row = conn.execute("SELECT COUNT(*) AS c FROM images;").fetchone()
        return int(row["c"]) if row else 0
    finally:
        conn.close()

def find_by_sha256(sha256_hex: str) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM images WHERE sha256 = ? LIMIT 1;",
            (sha256_hex,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def insert_image(filename: str, uploaded_at_iso: str, sha256_hex: str, phash_hex: str) -> int:
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO images (filename, uploaded_at, sha256, phash) VALUES (?, ?, ?, ?);",
            (filename, uploaded_at_iso, sha256_hex, phash_hex),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()

def get_all_images(limit: int = 500) -> List[Dict[str, Any]]:
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM images ORDER BY id DESC LIMIT ?;",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def get_image_by_id(image_id: int) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM images WHERE id = ? LIMIT 1;",
            (image_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
