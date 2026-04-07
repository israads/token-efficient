#!/bin/bash
# Creates a sample project for benchmarking token-efficient rules

set -e

DIR="test-project"
rm -rf "$DIR"
mkdir -p "$DIR"

# package.json (for Task 1 — version lookup)
cat > "$DIR/package.json" << 'EOF'
{
  "name": "benchmark-app",
  "version": "1.0.0",
  "engines": { "node": ">=20.11.0" },
  "scripts": { "test": "pytest" },
  "dependencies": {}
}
EOF

# app.py — main application with intentional bugs (Tasks 2, 3, 5, 10)
cat > "$DIR/app.py" << 'PYEOF'
"""Simple REST API for user management."""

from flask import Flask, request, jsonify
from functools import wraps
from db import get_user, create_user, list_users, get_db_connection
import time

app = Flask(__name__)

# --- Auth ---

def auth_required(f):
    """Decorator that checks for valid API key in Authorization header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return jsonify({"error": "unauthorized"}), 401
        token = auth.split(" ")[1]
        if len(token) < 16:
            return jsonify({"error": "invalid token"}), 403
        return f(*args, **kwargs)
    return decorated


# --- Routes ---

@app.route("/users", methods=["GET"])
@auth_required
def get_users():
    """List all users."""
    users = list_users()
    return jsonify(users)


@app.route("/users", methods=["POST"])
def create_new_user():
    """Create a user. TODO: add input validation"""
    data = request.get_json()
    user = create_user(data["name"], data["email"])
    return jsonify(user), 201


def divide_numbers(a, b):
    """Utility function for calculations. Bug: no zero check."""
    result = a / b
    return result


def format_user(user):
    # TODO: add avatar URL field
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "created": user["created_at"],
    }


def calculate_stats(users):
    """Calculate user statistics."""
    total = len(users)
    # TODO: add active/inactive breakdown
    active = total  # placeholder
    return {"total": total, "active": active}


# --- Padding to make file ~100 lines ---

def validate_email_format(email):
    """Basic email validation."""
    if "@" not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    if not parts[0] or not parts[1]:
        return False
    if "." not in parts[1]:
        return False
    return True


def generate_api_key():
    """Generate a random API key."""
    import secrets
    return secrets.token_hex(32)


def sanitize_input(text):
    """Remove potentially dangerous characters."""
    return text.strip().replace("<", "").replace(">", "")


def paginate(items, page=1, per_page=20):
    """Paginate a list of items."""
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "items": items[start:end],
        "total": len(items),
        "page": page,
        "per_page": per_page,
        "pages": (len(items) + per_page - 1) // per_page,
    }


if __name__ == "__main__":
    app.run(debug=True)
PYEOF

# db.py — database module (Task 7)
cat > "$DIR/db.py" << 'PYEOF'
"""Database operations — one connection per query (inefficient)."""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "app.db")


def get_db_connection():
    """Create a new connection every time (should use pooling)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def create_user(name, email):
    conn = get_db_connection()
    now = datetime.utcnow().isoformat()
    cursor = conn.execute(
        "INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)",
        (name, email, now),
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": user_id, "name": name, "email": email, "created_at": now}


def get_user(user_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def list_users():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def update_user(user_id, name=None, email=None):
    conn = get_db_connection()
    user = get_user(user_id)
    if not user:
        conn.close()
        return None
    conn.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (name or user["name"], email or user["email"], user_id),
    )
    conn.commit()
    conn.close()
    return get_user(user_id)


def search_users(query):
    """Search users by name or email."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?",
        (f"%{query}%", f"%{query}%"),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# TODO: add bulk import function
# TODO: add export to CSV
PYEOF

# middleware.py (Task 6)
cat > "$DIR/middleware.py" << 'PYEOF'
"""Authentication middleware for the API."""

from functools import wraps
from flask import request, jsonify
import hashlib
import time

API_KEYS = {}  # In production, load from DB or env


def auth_required(f):
    """
    Decorator that enforces Bearer token authentication.

    Checks the Authorization header for a valid Bearer token.
    Tokens must be at least 16 characters. Rejects requests
    with missing, malformed, or short tokens.

    Returns 401 for missing auth, 403 for invalid tokens.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "missing authorization header"}), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "invalid auth scheme, use Bearer"}), 401

        token = auth_header.split(" ", 1)[1]

        if len(token) < 16:
            return jsonify({"error": "token too short"}), 403

        # TODO: validate token against database
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        return f(*args, **kwargs)
    return decorated


def rate_limit(max_requests=100, window=3600):
    """Rate limiting decorator. TODO: implement with Redis."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Placeholder — no actual rate limiting
            return f(*args, **kwargs)
        return decorated
    return decorator
PYEOF

# test_app.py — tests with one failure (Task 9)
cat > "$DIR/test_app.py" << 'PYEOF'
"""Tests for the application."""

import pytest
from app import divide_numbers, validate_email_format, paginate, sanitize_input


def test_divide_numbers():
    assert divide_numbers(10, 2) == 5.0
    assert divide_numbers(7, 3) == pytest.approx(2.333, rel=1e-2)


def test_divide_by_zero():
    """This test will FAIL because divide_numbers has no zero-division handling."""
    with pytest.raises(ValueError):
        divide_numbers(10, 0)


def test_validate_email():
    assert validate_email_format("user@example.com") is True
    assert validate_email_format("bad-email") is False
    assert validate_email_format("@no-local.com") is False
    assert validate_email_format("no-domain@") is False


def test_paginate():
    items = list(range(50))
    result = paginate(items, page=1, per_page=10)
    assert len(result["items"]) == 10
    assert result["total"] == 50
    assert result["pages"] == 5


def test_sanitize():
    assert sanitize_input("  hello  ") == "hello"
    assert sanitize_input("<script>alert(1)</script>") == "script>alert(1)/script>"
PYEOF

# requirements.txt
cat > "$DIR/requirements.txt" << 'EOF'
flask==3.1.1
pytest==8.3.5
EOF

# Generate a dummy screenshot (1x1 white PNG — enough to trigger image rules)
python3 -c "
import base64, os
# Minimal 100x100 PNG
png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAIAAAD/gAIDAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAA3SURBVHhe7cEBDQAAAMKg909tDjcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPgaBTgAAZl+mgsAAAAASUVORK5CYII=')
with open('$DIR/screenshot.png', 'wb') as f:
    f.write(png)
"

# results template
cat > "$DIR/../results.md" << 'EOF'
# Benchmark Results

## Session A — WITH token-efficient rules

Date: ____
Model: ____

| Metric | Value |
|--------|-------|
| Input tokens | |
| Output tokens | |
| Total tokens | |
| Cost ($) | |
| Turns | |
| Cache read | |
| Cache write | |

Notes:


## Session B — WITHOUT rules (default behavior)

Date: ____
Model: ____

| Metric | Value |
|--------|-------|
| Input tokens | |
| Output tokens | |
| Total tokens | |
| Cost ($) | |
| Turns | |
| Cache read | |
| Cache write | |

Notes:


## Comparison

| Metric | With Rules | Without Rules | Reduction |
|--------|-----------|--------------|-----------|
| Input tokens | | | % |
| Output tokens | | | % |
| Total tokens | | | % |
| Cost ($) | | | % |
| Turns | | | % |
EOF

echo "✅ Test project created at $DIR/"
echo "Files: $(find $DIR -type f | wc -l | tr -d ' ')"
echo ""
echo "Next steps:"
echo "  1. cd $DIR"
echo "  2. cp ../../CLAUDE.md . (for Session A)"
echo "  3. claude  (run the 10 tasks)"
echo "  4. /cost   (record results)"
echo "  5. rm CLAUDE.md (for Session B)"
echo "  6. claude  (run same 10 tasks)"
echo "  7. /cost   (record results)"
