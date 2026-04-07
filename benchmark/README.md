# Token Efficient Benchmark

Reproducible test to measure token savings with and without the 30 rules.

## How It Works

You run the **same 10 tasks** in two separate Claude Code sessions:
- **Session A**: With `CLAUDE.md` (rules active)
- **Session B**: Without `CLAUDE.md` (default behavior)

After each session, you extract token usage from Claude Code's built-in stats and compare.

## Setup

### 1. Prepare the test project

```bash
# Clone this repo (it's already a test project)
cd benchmark/
./setup.sh
```

This creates a small sample project with:
- A Python app with intentional bugs
- A 400-line file to test partial reads
- An image to test resize behavior
- Config files to test simple lookups

### 2. Run Session A (WITH rules)

```bash
# Ensure CLAUDE.md is in the benchmark project root
cp ../CLAUDE.md test-project/CLAUDE.md

# Start Claude Code in the test project
cd test-project
claude

# Run the 10 tasks from tasks.md, one by one
# After completing all tasks, run:
#   /cost
# Screenshot or copy the token usage summary
```

### 3. Run Session B (WITHOUT rules)

```bash
# Remove CLAUDE.md
rm test-project/CLAUDE.md

# Start a fresh Claude Code session
cd test-project
claude

# Run the EXACT same 10 tasks from tasks.md
# After completing all tasks, run:
#   /cost
# Screenshot or copy the token usage summary
```

### 4. Record Results

Fill in `results.md` with the token counts from each session.

## The 10 Tasks

See [tasks.md](tasks.md) for the full list. Tasks are designed to exercise different rule categories:

| # | Task | Rules Tested |
|---|------|-------------|
| 1 | "What Node version does this project use?" | #11 proportional response |
| 2 | "Read the file app.py and tell me what it does" | #16 partial reads, #2 brief output |
| 3 | "Fix the bug on line 42 of app.py" | #3 edit over rewrite, #10 act first |
| 4 | "Find all TODO comments in the project" | #22 cheapest tool, #18 parallel calls |
| 5 | "Add input validation to the /users endpoint" | #6 simple solution, #13 stay in scope |
| 6 | "What does the auth middleware do?" | #11 proportional, #14 code first |
| 7 | "Refactor the database module to use connection pooling" | #1 read first, #3 edit over rewrite |
| 8 | "Read this screenshot and tell me what you see" | #26 resize, #27 describe immediately |
| 9 | "Run the tests and fix any failures" | #5 verify, #10 act first |
| 10 | "Create a new endpoint GET /health that returns {status: ok}" | #6 simple, #15 plain text response |

## What to Measure

From `/cost` output after each session:

| Metric | Session A (rules) | Session B (no rules) |
|--------|-------------------|---------------------|
| Total input tokens | | |
| Total output tokens | | |
| Total tokens | | |
| Total cost ($) | | |
| Number of turns | | |
| Cache read tokens | | |
| Cache write tokens | | |

## Expected Results

Based on community benchmarks:
- **Output tokens**: 40-65% reduction
- **Input tokens**: 15-30% reduction (from fewer turns and partial reads)
- **Total cost**: 25-45% reduction
- **Turns**: 20-35% fewer (from parallel calls and act-first behavior)
