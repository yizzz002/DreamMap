import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "dreams.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dreams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dream_date TEXT NOT NULL,
            content TEXT NOT NULL,
            mood TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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