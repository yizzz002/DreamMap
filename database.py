import sqlite3
from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "dreams.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)

    # 開啟 SQLite Foreign Key 支援
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dream_id INTEGER NOT NULL,
            reflection TEXT NOT NULL,
            concepts_json TEXT,
            model_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (dream_id)
            REFERENCES dreams(id)
            ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def add_dream(dream_date, content, mood):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO dreams (dream_date, content, mood)
        VALUES (?, ?, ?)
    """, (dream_date, content, mood))

    conn.commit()
    conn.close()


def get_all_dreams():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, dream_date, content, mood, created_at
        FROM dreams
        ORDER BY dream_date DESC, id DESC
    """)

    dreams = cursor.fetchall()

    conn.close()

    return dreams


def update_dream(dream_id, dream_date, content, mood):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE dreams
        SET dream_date = ?, content = ?, mood = ?
        WHERE id = ?
    """, (
        dream_date,
        content,
        mood,
        dream_id
    ))

    conn.commit()
    conn.close()

def delete_dream(dream_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM dreams WHERE id = ?",
        (dream_id,)
    )

    conn.commit()
    conn.close()

def add_analysis(
    dream_id,
    reflection,
    concepts,
    model_name="qwen3:1.7b"
):
    conn = get_connection()
    cursor = conn.cursor()

    concepts_json = json.dumps(
        concepts,
        ensure_ascii=False
    )

    cursor.execute("""
        INSERT INTO analyses (
            dream_id,
            reflection,
            concepts_json,
            model_name
        )
        VALUES (?, ?, ?, ?)
    """, (
        dream_id,
        reflection,
        concepts_json,
        model_name
    ))

    conn.commit()
    conn.close()

def get_latest_analysis(dream_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            reflection,
            concepts_json,
            model_name,
            created_at
        FROM analyses
        WHERE dream_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (dream_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "reflection": row[1],
        "concepts": json.loads(
            row[2]
        ) if row[2] else [],
        "model_name": row[3],
        "created_at": row[4]
    }