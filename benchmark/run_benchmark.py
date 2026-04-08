"""
Token Efficient Benchmark — API-based measurement.

Runs the same 10 tasks twice (without rules, with rules) via the Anthropic API
and compares exact token usage from the API response.
"""

import anthropic
import json
import os
import sys
import time

# --- Config ---
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = os.environ.get("BENCHMARK_MODEL", "claude-sonnet-4-20250514")
MAX_TOKENS = 4096

# --- Test project files (inline for reproducibility) ---
FILES = {
    "package.json": '{"name":"benchmark-app","version":"1.0.0","engines":{"node":">=20.11.0"},"scripts":{"test":"pytest"},"dependencies":{}}',

    "app.py": '''"""Simple REST API for user management."""
from flask import Flask, request, jsonify
from functools import wraps
import time

app = Flask(__name__)

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

@app.route("/users", methods=["GET"])
@auth_required
def get_users():
    """List all users."""
    return jsonify([])

@app.route("/users", methods=["POST"])
def create_new_user():
    """Create a user. TODO: add input validation"""
    data = request.get_json()
    return jsonify({"name": data["name"], "email": data["email"]}), 201

def divide_numbers(a, b):
    """Utility function for calculations. Bug: no zero check."""
    result = a / b
    return result

def format_user(user):
    # TODO: add avatar URL field
    return {"id": user["id"], "name": user["name"], "email": user["email"]}

def calculate_stats(users):
    """Calculate user statistics."""
    total = len(users)
    # TODO: add active/inactive breakdown
    return {"total": total, "active": total}

def validate_email_format(email):
    if "@" not in email:
        return False
    parts = email.split("@")
    return len(parts) == 2 and parts[0] and parts[1] and "." in parts[1]

def generate_api_key():
    import secrets
    return secrets.token_hex(32)

def sanitize_input(text):
    return text.strip().replace("<", "").replace(">", "")

def paginate(items, page=1, per_page=20):
    start = (page - 1) * per_page
    end = start + per_page
    return {"items": items[start:end], "total": len(items), "page": page, "per_page": per_page}

if __name__ == "__main__":
    app.run(debug=True)
''',

    "db.py": '''"""Database operations — one connection per query (inefficient)."""
import sqlite3, os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "app.db")

def get_db_connection():
    """Create a new connection every time (should use pooling)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, created_at TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def create_user(name, email):
    conn = get_db_connection()
    now = datetime.utcnow().isoformat()
    cursor = conn.execute("INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)", (name, email, now))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": user_id, "name": name, "email": email, "created_at": now}

def get_user(user_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

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

# TODO: add bulk import function
# TODO: add export to CSV
''',

    "middleware.py": '''"""Authentication middleware for the API."""
from functools import wraps
from flask import request, jsonify
import hashlib

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
            return f(*args, **kwargs)
        return decorated
    return decorator
''',

    "test_app.py": '''"""Tests for the application."""
import pytest
from app import divide_numbers, validate_email_format, paginate, sanitize_input

def test_divide_numbers():
    assert divide_numbers(10, 2) == 5.0

def test_divide_by_zero():
    """This test will FAIL — divide_numbers has no zero-division handling."""
    with pytest.raises(ValueError):
        divide_numbers(10, 0)

def test_validate_email():
    assert validate_email_format("user@example.com") is True
    assert validate_email_format("bad-email") is False

def test_paginate():
    items = list(range(50))
    result = paginate(items, page=1, per_page=10)
    assert len(result["items"]) == 10
    assert result["total"] == 50

def test_sanitize():
    assert sanitize_input("  hello  ") == "hello"
'''
}

# --- The 10 tasks ---
TASKS = [
    "What version of Node does this project use?",
    "Explain what app.py does",
    "The function divide_numbers on line 42 of app.py crashes when b is zero. Fix it.",
    "Find all TODO comments across the project",
    "Add validation to POST /users — name can't be empty, email needs an @",
    "How does the auth_required decorator in middleware.py work?",
    "Refactor db.py to use connection pooling instead of opening a new connection every query",
    "Look at screenshot.png and describe what you see",
    "Run pytest and fix whatever fails",
    "Add a GET /health endpoint that returns {\"status\": \"ok\"}",
]

# --- Token efficient rules ---
RULES = """# Token Efficient Rules

## Core
1. Read before writing.
2. Think deep, write brief.
3. Edit over rewrite. Diffs, not full files.
4. Don't re-read files already in context.
5. Verify before declaring done. Run tests, check output.
6. Simplest working solution. No abstractions for one-off operations.
7. User instructions override all rules here.

## Output
8. No filler ("Great question!", "Sure!", "Let me know if...").
9. No echo. Execute, don't restate.
10. Act first, report after. No narrating planned steps.
11. Proportional: one-line question → one-line answer.
12. No soft warnings unless genuinely dangerous.
13. Stay in scope. No unsolicited suggestions.
14. Code first. Explain only if non-obvious.
15. Plain text default. Markdown only when structure aids comprehension.
16. Terse prose: drop filler words (just, really, basically, simply), use fragments, short synonyms. Code and technical terms untouched.
17. Confirm with result, not explanation. "Fixed in app.py:42" beats a paragraph about what changed.
18. Report only changes and failures. Skip "everything else looks good."

## Context
19. Read only needed sections. Use offset+limit for large files.
20. Delegate exploration to subagents. Their context is disposable; yours is expensive.
21. Parallelize independent tool calls. Fewer turns = fewer context re-sends.
22. Compact at 60%, not 90%. Before compacting, state which files were modified, decisions made, and patterns chosen — compaction loses specifics without explicit anchors.
23. Don't repeat established facts. Restate only after compaction if uncertain.
24. Assign shorthands ("the auth module") and reuse throughout session.
25. Batch related edits into one turn. Each turn re-sends full history.
26. Reference code by `file:line`, not by re-pasting. Content already in context doesn't need re-encoding.

## Tools
27. Cheapest tool first: Glob/Grep → Read(section) → Agent.
28. CLI over MCP when both work. MCP schema costs ~10x more.
29. Direct paths over search when location is known.
30. Show only changed lines + minimal surrounding context.
31. Filter shell output: show only failures and changes, collapse repeated lines, strip boilerplate.

## Images
32. Resize before reading. Smaller images = fewer tokens.
33. Describe observations immediately in text. Text survives compaction; images don't.
34. Never re-read same image. Notes are 10-20x cheaper than re-encoding.

## Model
35. Cheapest model for the task. Sonnet for mechanical work, Opus for judgment.
36. Lower effort for simple lookups. Not every question needs deep reasoning.
"""


def build_system_prompt(with_rules: bool) -> str:
    """Build system prompt with project files as context."""
    parts = [
        "You are a coding assistant helping with a Python Flask project.",
        "Here are the project files:\n",
    ]
    for name, content in FILES.items():
        parts.append(f"--- {name} ---\n{content}\n")

    if with_rules:
        parts.append("\n--- CLAUDE.md (YOUR RULES — FOLLOW STRICTLY) ---\n")
        parts.append(RULES)

    return "\n".join(parts)


def run_session(client, with_rules: bool) -> dict:
    """Run all 10 tasks and collect token metrics."""
    label = "WITH rules" if with_rules else "WITHOUT rules"
    system_prompt = build_system_prompt(with_rules)

    results = {
        "label": label,
        "tasks": [],
        "total_input": 0,
        "total_output": 0,
    }

    # Each task is independent (single-turn) to keep it fair
    for i, task in enumerate(TASKS):
        # Skip image task (no image in API mode)
        if "screenshot" in task.lower():
            print(f"  Task {i+1}: [SKIPPED — no image in API mode]")
            results["tasks"].append({
                "task": i + 1,
                "prompt": task,
                "input_tokens": 0,
                "output_tokens": 0,
                "output_length": 0,
                "skipped": True,
            })
            continue

        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system_prompt,
                messages=[{"role": "user", "content": task}],
            )

            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            output_text = response.content[0].text if response.content else ""

            results["tasks"].append({
                "task": i + 1,
                "prompt": task,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "output_length": len(output_text),
                "output_preview": output_text[:150] + "..." if len(output_text) > 150 else output_text,
            })
            results["total_input"] += input_tokens
            results["total_output"] += output_tokens

            print(f"  Task {i+1}: input={input_tokens:,} output={output_tokens:,} chars={len(output_text):,}")

            # Small delay to avoid rate limits
            time.sleep(0.5)

        except Exception as e:
            print(f"  Task {i+1}: ERROR — {e}")
            results["tasks"].append({
                "task": i + 1,
                "prompt": task,
                "error": str(e),
                "input_tokens": 0,
                "output_tokens": 0,
            })

    results["total_tokens"] = results["total_input"] + results["total_output"]
    return results


def print_comparison(without: dict, with_rules: dict):
    """Print side-by-side comparison."""
    print("\n" + "=" * 70)
    print("BENCHMARK RESULTS")
    print("=" * 70)

    # Per-task comparison
    print(f"\n{'Task':<6} {'Without Rules':>20} {'With Rules':>20} {'Saved':>12}")
    print(f"{'':>6} {'(output tokens)':>20} {'(output tokens)':>20} {'':>12}")
    print("-" * 60)

    for i in range(len(TASKS)):
        t_without = without["tasks"][i]
        t_with = with_rules["tasks"][i]

        if t_without.get("skipped"):
            print(f"  {i+1:<4} {'SKIPPED':>20} {'SKIPPED':>20} {'—':>12}")
            continue

        out_a = t_without.get("output_tokens", 0)
        out_b = t_with.get("output_tokens", 0)

        if out_a > 0:
            pct = ((out_a - out_b) / out_a) * 100
            saved = f"{pct:+.0f}%"
        else:
            saved = "—"

        print(f"  {i+1:<4} {out_a:>20,} {out_b:>20,} {saved:>12}")

    # Totals
    print("-" * 60)

    for metric, key in [("Input tokens", "total_input"), ("Output tokens", "total_output"), ("Total tokens", "total_tokens")]:
        a = without[key]
        b = with_rules[key]
        if a > 0:
            pct = ((a - b) / a) * 100
            saved = f"{pct:+.0f}%"
        else:
            saved = "—"
        print(f"  {'TOTAL ' + metric:<26} {a:>14,} {b:>14,} {saved:>12}")

    # Cost estimate (Sonnet pricing: $3/M input, $15/M output)
    cost_a = (without["total_input"] * 3 + without["total_output"] * 15) / 1_000_000
    cost_b = (with_rules["total_input"] * 3 + with_rules["total_output"] * 15) / 1_000_000
    if cost_a > 0:
        cost_saved = ((cost_a - cost_b) / cost_a) * 100
        print(f"\n  {'Estimated cost':<26} ${cost_a:>13.4f} ${cost_b:>13.4f} {cost_saved:+.0f}%")

    print("\n" + "=" * 70)


def main():
    api_key = API_KEY or (sys.argv[1] if len(sys.argv) > 1 else "")
    if not api_key:
        print("Usage: ANTHROPIC_API_KEY=sk-... python3 run_benchmark.py")
        print("   or: python3 run_benchmark.py sk-ant-...")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print(f"Model: {MODEL}")
    print(f"Tasks: {len(TASKS)}")
    print()

    # Session 1: WITHOUT rules
    print("━" * 40)
    print("SESSION 1: WITHOUT rules")
    print("━" * 40)
    without = run_session(client, with_rules=False)

    print()

    # Session 2: WITH rules
    print("━" * 40)
    print("SESSION 2: WITH rules")
    print("━" * 40)
    with_rules = run_session(client, with_rules=True)

    # Comparison
    print_comparison(without, with_rules)

    # Save raw data
    output_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(output_path, "w") as f:
        json.dump({"without_rules": without, "with_rules": with_rules, "model": MODEL}, f, indent=2)
    print(f"\nRaw data saved to {output_path}")


if __name__ == "__main__":
    main()
