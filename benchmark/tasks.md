# Benchmark Tasks (v2)

15 tasks across 7 categories. Copy-paste each prompt into Claude Code. Use the **exact same wording** in both sessions.

---

## Lookup (tests rules 11, 15)

**1.** `What version of Node does this project use?`

**2.** `What Python packages does this project depend on?`

## Explain (tests rules 14, 16)

**3.** `Explain what app.py does`

**4.** `How does the auth_required decorator in middleware.py work?`

## Search (tests rule 18)

**5.** `Find all TODO comments across the project`

**6.** `List all functions defined in db.py with a one-line description of each`

## Bug Fix (tests rules 3, 17)

**7.** `The function divide_numbers on line 42 of app.py crashes when b is zero. Fix it.`

**8.** `The sanitize_input function doesn't handle None input. Fix it.`

## Feature (tests rules 10, 13, 17)

**9.** `Add a GET /health endpoint that returns {"status": "ok"}`

**10.** `Add validation to POST /users — name can't be empty, email needs an @`

**11.** `Add a DELETE /users/<id> endpoint that returns 204 on success`

## Refactor (tests rules 3, 30)

**12.** `Refactor db.py to use connection pooling instead of opening a new connection every query`

**13.** `Rename validate_email_format to is_valid_email everywhere in the project`

## Test & Review (tests rules 5, 12, 18, 31)

**14.** `Run pytest and fix whatever fails`

**15.** `What are the top 3 security issues in this codebase? Be specific about file and line.`
