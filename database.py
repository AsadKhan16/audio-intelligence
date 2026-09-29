import sqlite3
from datetime import datetime , timezone

DB_PATH = "maindatabase.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            created_at TEXT NOT NULL
        );
 
        CREATE TABLE IF NOT EXISTS statements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            speaker_label TEXT,        -- e.g. 'SPEAKER_00', or a resolved name later
            start_time REAL,           -- seconds from start of the audio chunk
            end_time REAL,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        );
 
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            statement_id INTEGER NOT NULL,
            type TEXT,                 -- e.g. 'PERSON', 'ORG', 'DATE'
            value TEXT,
            FOREIGN KEY (statement_id) REFERENCES statements(id)
        );



        """
    )
    conn.commit()
    conn.close()
    print(f"Databse ready at {DB_PATH}")
    

def create_session(title: str) -> int:
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO sessions (title, created_at) VALUES (?, ?)",
        (title, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    session_id = cur.lastrowid
    conn.close()
    return session_id

def add_statement(session_id: int, text: str, start_time: float = None,
                   end_time: float = None, speaker_label: str = None) -> int:
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO statements
           (session_id, speaker_label, start_time, end_time, text, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (session_id, speaker_label, start_time, end_time, text,
         datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    statement_id = cur.lastrowid
    conn.close()
    return statement_id

if __name__ == "__main__":
    init_db()
