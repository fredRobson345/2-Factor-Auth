import sqlite3
import os
import hashlib
import hmac
from pathlib import Path
from typing import Optional, Dict, Any

DB_FILENAME = Path(__file__).parent / "users.db"
_PBKDF2_ITERATIONS = 100_000

def _get_conn(db_path: Optional[Path] = None) -> sqlite3.Connection:
    path = str(db_path or DB_FILENAME)
    conn = sqlite3.connect(path, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: Optional[Path] = None) -> None:
    """Create users table if it doesn't exist."""
    with _get_conn(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                email TEXT
            )
            """
        )
        conn.commit()

def _hash_password(password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
    """Return dict with hex 'salt' and hex 'hash' using PBKDF2-HMAC-SHA256."""
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS)
    return {"salt": salt.hex(), "hash": dk.hex()}

def add_user(username: str, password: str, email: Optional[str] = None, db_path: Optional[Path] = None) -> bool:
    """
    Add a user. Returns True on success, False if username already exists or error.
    """
    init_db(db_path)
    hp = _hash_password(password)
    try:
        with _get_conn(db_path) as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, salt, email) VALUES (?, ?, ?, ?)",
                (username, hp["hash"], hp["salt"], email),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False

def get_user(username: str, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """Return user row as dict or None if not found."""
    init_db(db_path)
    with _get_conn(db_path) as conn:
        cur = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        return dict(row) if row else None

def verify_user(username: str, password: str, db_path: Optional[Path] = None) -> bool:
    """
    Verify username and password against the database.
    Returns True if credentials match, False otherwise.
    """
    user = get_user(username, db_path)
    if not user:
        return False
    try:
        salt = bytes.fromhex(user["salt"])
        expected_hash = user["password_hash"]
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS)
        return hmac.compare_digest(dk.hex(), expected_hash)
    except Exception:
        return False

# convenience: create example user if none exist
if __name__ == "__main__":
    init_db()
    created = add_user("example123", "password123", "freddie.robson2004@gmail.com")
    print("example user created:" , created)
    print("verify example:", verify_user("example123", "password123"))