"""
Token Efficient Benchmark v2 — API-based measurement.

Runs 15 categorized tasks twice (without rules, with rules) via the Anthropic API.
Measures exact token usage, calculates per-category savings, and generates
a markdown results file.
"""

import anthropic
import json
import os
import sys
import time
from datetime import datetime, timezone

# --- Config ---
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = os.environ.get("BENCHMARK_MODEL", "claude-sonnet-4-20250514")
MAX_TOKENS = 4096
RUNS = int(os.environ.get("BENCHMARK_RUNS", "1"))  # Multiple runs for averaging

# Model pricing per 1M tokens
PRICING = {
    "claude-sonnet-4-20250514": {"input": 3, "output": 15, "name": "Sonnet 4"},
    "claude-opus-4-20250514": {"input": 15, "output": 75, "name": "Opus 4"},
}

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

# --- 15 categorized tasks ---
TASKS = [
    # Category: Lookup (tests rules 11, 15 — proportional, plain text)
    {"prompt": "What version of Node does this project use?",
     "category": "lookup", "short": "Node version"},
    {"prompt": "What Python packages does this project depend on?",
     "category": "lookup", "short": "Python deps"},

    # Category: Explain (tests rules 14, 16 — code first, terse prose)
    {"prompt": "Explain what app.py does",
     "category": "explain", "short": "Explain app.py"},
    {"prompt": "How does the auth_required decorator in middleware.py work?",
     "category": "explain", "short": "Explain auth decorator"},

    # Category: Search (tests rules 18 — report only changes/findings)
    {"prompt": "Find all TODO comments across the project",
     "category": "search", "short": "Find TODOs"},
    {"prompt": "List all functions defined in db.py with a one-line description of each",
     "category": "search", "short": "List db.py functions"},

    # Category: Bug fix (tests rules 3, 17 — edit over rewrite, confirm with result)
    {"prompt": "The function divide_numbers on line 42 of app.py crashes when b is zero. Fix it.",
     "category": "bugfix", "short": "Fix divide_numbers"},
    {"prompt": "The sanitize_input function doesn't handle None input. Fix it.",
     "category": "bugfix", "short": "Fix sanitize_input"},

    # Category: Feature (tests rules 10, 13, 17 — act first, stay in scope, confirm)
    {"prompt": 'Add a GET /health endpoint that returns {"status": "ok"}',
     "category": "feature", "short": "Add /health"},
    {"prompt": "Add validation to POST /users — name can't be empty, email needs an @",
     "category": "feature", "short": "Add POST validation"},
    {"prompt": "Add a DELETE /users/<id> endpoint that returns 204 on success",
     "category": "feature", "short": "Add DELETE /users"},

    # Category: Refactor (tests rules 3, 30 — edit over rewrite, show only changed)
    {"prompt": "Refactor db.py to use connection pooling instead of opening a new connection every query",
     "category": "refactor", "short": "Refactor db.py pooling"},
    {"prompt": "Rename validate_email_format to is_valid_email everywhere in the project",
     "category": "refactor", "short": "Rename function"},

    # Category: Test/Debug (tests rules 5, 18, 31 — verify, report only failures, filter output)
    {"prompt": "Run pytest and fix whatever fails",
     "category": "test", "short": "Run tests + fix"},

    # Category: Review (tests rules 12, 13 — no soft warnings, stay in scope)
    {"prompt": "What are the top 3 security issues in this codebase? Be specific about file and line.",
     "category": "review", "short": "Security review"},
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


def get_pricing(model: str) -> dict:
    """Get pricing for the model, with fallback."""
    for key, price in PRICING.items():
        if key in model:
            return price
    return {"input": 3, "output": 15, "name": model}


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


def run_single_task(client, system_prompt: str, task: dict) -> dict:
    """Run a single task and return metrics."""
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": task["prompt"]}],
        )

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        output_text = response.content[0].text if response.content else ""

        return {
            "prompt": task["prompt"],
            "short": task["short"],
            "category": task["category"],
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "output_length": len(output_text),
            "output_preview": output_text[:200] + "..." if len(output_text) > 200 else output_text,
        }
    except Exception as e:
        print(f"    ERROR — {e}")
        return {
            "prompt": task["prompt"],
            "short": task["short"],
            "category": task["category"],
            "error": str(e),
            "input_tokens": 0,
            "output_tokens": 0,
        }


def run_session(client, with_rules: bool) -> dict:
    """Run all tasks and collect token metrics."""
    label = "WITH rules" if with_rules else "WITHOUT rules"
    system_prompt = build_system_prompt(with_rules)

    results = {
        "label": label,
        "tasks": [],
        "total_input": 0,
        "total_output": 0,
    }

    for i, task in enumerate(TASKS):
        result = run_single_task(client, system_prompt, task)
        results["tasks"].append(result)
        results["total_input"] += result.get("input_tokens", 0)
        results["total_output"] += result.get("output_tokens", 0)

        out = result.get("output_tokens", 0)
        err = result.get("error", "")
        status = f"output={out:,}" if not err else f"ERROR: {err[:50]}"
        print(f"  {i+1:>2}. [{task['category']:>8}] {task['short']:<25} {status}")

        time.sleep(0.5)

    results["total_tokens"] = results["total_input"] + results["total_output"]
    return results


def print_comparison(without: dict, with_rules: dict, pricing: dict):
    """Print side-by-side comparison with categories."""
    print("\n" + "═" * 78)
    print(f"  BENCHMARK RESULTS — {pricing['name']} ({MODEL})")
    print("═" * 78)

    # Per-task comparison
    print(f"\n  {'#':<3} {'Category':<10} {'Task':<25} {'Without':>8} {'With':>8} {'Saved':>8}")
    print("  " + "─" * 72)

    categories = {}
    for i in range(len(TASKS)):
        t_without = without["tasks"][i]
        t_with = with_rules["tasks"][i]
        cat = t_without["category"]

        out_a = t_without.get("output_tokens", 0)
        out_b = t_with.get("output_tokens", 0)

        if cat not in categories:
            categories[cat] = {"without": 0, "with": 0}
        categories[cat]["without"] += out_a
        categories[cat]["with"] += out_b

        if out_a > 0:
            pct = ((out_a - out_b) / out_a) * 100
            saved = f"{pct:+.0f}%"
        else:
            saved = "—"

        print(f"  {i+1:<3} {cat:<10} {t_without['short']:<25} {out_a:>8,} {out_b:>8,} {saved:>8}")

    # Category summary
    print("\n  " + "─" * 72)
    print(f"  {'Category Summary':<38} {'Without':>8} {'With':>8} {'Saved':>8}")
    print("  " + "─" * 72)

    for cat, totals in sorted(categories.items()):
        a, b = totals["without"], totals["with"]
        pct = ((a - b) / a * 100) if a > 0 else 0
        print(f"  {cat:<38} {a:>8,} {b:>8,} {pct:>+7.0f}%")

    # Totals
    print("\n  " + "─" * 72)
    for metric, key in [("Output tokens", "total_output"), ("Input tokens", "total_input")]:
        a = without[key]
        b = with_rules[key]
        pct = ((a - b) / a * 100) if a > 0 else 0
        print(f"  TOTAL {metric:<31} {a:>8,} {b:>8,} {pct:>+7.0f}%")

    # Cost
    ip, op = pricing["input"], pricing["output"]
    cost_a = (without["total_input"] * ip + without["total_output"] * op) / 1_000_000
    cost_b = (with_rules["total_input"] * ip + with_rules["total_output"] * op) / 1_000_000
    cost_pct = ((cost_a - cost_b) / cost_a * 100) if cost_a > 0 else 0
    print(f"\n  Estimated cost (${ip}/M in, ${op}/M out)  ${cost_a:>7.4f}  ${cost_b:>7.4f} {cost_pct:>+7.0f}%")

    # Stats
    savings = []
    for i in range(len(TASKS)):
        a = without["tasks"][i].get("output_tokens", 0)
        b = with_rules["tasks"][i].get("output_tokens", 0)
        if a > 0:
            savings.append((a - b) / a * 100)

    if savings:
        savings.sort()
        median = savings[len(savings) // 2]
        print(f"\n  Output savings: min={min(savings):+.0f}%  median={median:+.0f}%  max={max(savings):+.0f}%  mean={sum(savings)/len(savings):+.0f}%")

    print("\n" + "═" * 78)


def generate_markdown(without: dict, with_rules: dict, pricing: dict, model: str) -> str:
    """Generate markdown results file."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# Benchmark Results — {pricing['name']}",
        f"\nGenerated on {now} using `{model}`.\n",
        f"| # | Category | Task | Without | With Rules | Saved |",
        f"|---|----------|------|--------:|-----------:|------:|",
    ]

    for i in range(len(TASKS)):
        t_w = without["tasks"][i]
        t_r = with_rules["tasks"][i]
        a = t_w.get("output_tokens", 0)
        b = t_r.get("output_tokens", 0)
        pct = f"{(a - b) / a * 100:.0f}%" if a > 0 else "—"
        lines.append(f"| {i+1} | {t_w['category']} | {t_w['short']} | {a:,} | **{b:,}** | **{pct}** |")

    ip, op = pricing["input"], pricing["output"]
    cost_a = (without["total_input"] * ip + without["total_output"] * op) / 1_000_000
    cost_b = (with_rules["total_input"] * ip + with_rules["total_output"] * op) / 1_000_000
    out_pct = (without["total_output"] - with_rules["total_output"]) / without["total_output"] * 100
    cost_pct = (cost_a - cost_b) / cost_a * 100

    lines += [
        f"\n| Metric | Without | With | Change |",
        f"|--------|--------:|-----:|-------:|",
        f"| **Output tokens** | **{without['total_output']:,}** | **{with_rules['total_output']:,}** | **{out_pct:+.0f}%** |",
        f"| Input tokens | {without['total_input']:,} | {with_rules['total_input']:,} | {(with_rules['total_input'] - without['total_input']) / without['total_input'] * 100:+.0f}% |",
        f"| **Estimated cost** | **${cost_a:.4f}** | **${cost_b:.4f}** | **{cost_pct:+.0f}%** |",
    ]

    # Category breakdown
    categories = {}
    for i in range(len(TASKS)):
        cat = without["tasks"][i]["category"]
        if cat not in categories:
            categories[cat] = {"without": 0, "with": 0}
        categories[cat]["without"] += without["tasks"][i].get("output_tokens", 0)
        categories[cat]["with"] += with_rules["tasks"][i].get("output_tokens", 0)

    lines += [
        f"\n### By Category\n",
        f"| Category | Without | With | Saved |",
        f"|----------|--------:|-----:|------:|",
    ]
    for cat, t in sorted(categories.items()):
        pct = (t["without"] - t["with"]) / t["without"] * 100 if t["without"] > 0 else 0
        lines.append(f"| {cat} | {t['without']:,} | {t['with']:,} | {pct:.0f}% |")

    return "\n".join(lines) + "\n"


def main():
    api_key = API_KEY or (sys.argv[1] if len(sys.argv) > 1 else "")
    if not api_key:
        print("Usage: ANTHROPIC_API_KEY=sk-... python3 run_benchmark.py")
        print("   or: python3 run_benchmark.py sk-ant-...")
        print("\nOptions:")
        print("  BENCHMARK_MODEL=claude-opus-4-20250514  (default: sonnet)")
        print("  BENCHMARK_RUNS=3                        (default: 1, averages multiple runs)")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    pricing = get_pricing(MODEL)
    model_short = pricing["name"].lower().replace(" ", "-")

    print(f"Model: {MODEL} ({pricing['name']})")
    print(f"Tasks: {len(TASKS)}")
    print(f"Runs:  {RUNS}")
    print(f"Price: ${pricing['input']}/M input, ${pricing['output']}/M output")
    print()

    # Session 1: WITHOUT rules
    print("━" * 50)
    print("SESSION 1: WITHOUT rules")
    print("━" * 50)
    without = run_session(client, with_rules=False)

    print()

    # Session 2: WITH rules
    print("━" * 50)
    print("SESSION 2: WITH rules")
    print("━" * 50)
    with_rules = run_session(client, with_rules=True)

    # Additional runs for averaging
    if RUNS > 1:
        for run in range(2, RUNS + 1):
            print(f"\n━━━ Run {run}/{RUNS} ━━━")

            print("  WITHOUT rules...")
            extra_without = run_session(client, with_rules=False)
            for i in range(len(TASKS)):
                for k in ("input_tokens", "output_tokens"):
                    without["tasks"][i][k] = (without["tasks"][i].get(k, 0) + extra_without["tasks"][i].get(k, 0)) // 2
            without["total_input"] = sum(t.get("input_tokens", 0) for t in without["tasks"])
            without["total_output"] = sum(t.get("output_tokens", 0) for t in without["tasks"])
            without["total_tokens"] = without["total_input"] + without["total_output"]

            print("  WITH rules...")
            extra_with = run_session(client, with_rules=True)
            for i in range(len(TASKS)):
                for k in ("input_tokens", "output_tokens"):
                    with_rules["tasks"][i][k] = (with_rules["tasks"][i].get(k, 0) + extra_with["tasks"][i].get(k, 0)) // 2
            with_rules["total_input"] = sum(t.get("input_tokens", 0) for t in with_rules["tasks"])
            with_rules["total_output"] = sum(t.get("output_tokens", 0) for t in with_rules["tasks"])
            with_rules["total_tokens"] = with_rules["total_input"] + with_rules["total_output"]

    # Print comparison
    print_comparison(without, with_rules, pricing)

    # Save results
    base = os.path.dirname(__file__)

    json_path = os.path.join(base, f"results-{model_short}.json")
    with open(json_path, "w") as f:
        json.dump({
            "without_rules": without,
            "with_rules": with_rules,
            "model": MODEL,
            "model_name": pricing["name"],
            "runs": RUNS,
            "tasks": len(TASKS),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }, f, indent=2)
    print(f"\nRaw data: {json_path}")

    md_path = os.path.join(base, f"results-{model_short}.md")
    with open(md_path, "w") as f:
        f.write(generate_markdown(without, with_rules, pricing, MODEL))
    print(f"Markdown: {md_path}")


if __name__ == "__main__":
    main()
