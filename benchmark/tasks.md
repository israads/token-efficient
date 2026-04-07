# Benchmark Tasks

Run these 10 tasks in order, exactly as written. Copy-paste each prompt into Claude Code.

**Important**: Use the EXACT same wording in both sessions (with and without CLAUDE.md).

---

### Task 1 — Simple lookup
```
What Node version does this project use?
```

### Task 2 — File comprehension
```
Read the file app.py and tell me what it does
```

### Task 3 — Bug fix
```
There's a bug on line 42 of app.py — the divide_numbers function doesn't handle division by zero. Fix it.
```

### Task 4 — Codebase search
```
Find all TODO comments in the project and list them
```

### Task 5 — Feature addition with scope control
```
Add input validation to the POST /users endpoint in app.py. Name must be non-empty string, email must contain @.
```

### Task 6 — Code explanation
```
What does the auth_required decorator in middleware.py do?
```

### Task 7 — Refactor
```
Refactor the database functions in db.py to use a connection pool instead of creating a new connection per query
```

### Task 8 — Image reading
```
Read the screenshot at screenshot.png and tell me what you see
```

### Task 9 — Test and fix
```
Run the tests with pytest and fix any failures
```

### Task 10 — New feature
```
Create a new endpoint GET /health that returns {"status": "ok", "timestamp": current_utc_time}
```
