# Benchmark v2

Measures token savings from the 36 rules using 15 categorized tasks against a Flask test project.

## Quick Start

```bash
# Run with Sonnet (default)
ANTHROPIC_API_KEY=sk-ant-... python3 run_benchmark.py

# Run with Opus
BENCHMARK_MODEL=claude-opus-4-20250514 ANTHROPIC_API_KEY=sk-ant-... python3 run_benchmark.py

# Average across 3 runs (more stable results)
BENCHMARK_RUNS=3 ANTHROPIC_API_KEY=sk-ant-... python3 run_benchmark.py
```

## What it does

1. Builds a system prompt with 5 project files (~400 lines of Flask code)
2. Runs 15 tasks **without** rules — measures baseline output tokens
3. Runs the same 15 tasks **with** the 36 rules injected — measures optimized output
4. Compares per-task, per-category, and total token usage
5. Saves results as JSON and Markdown

## The 15 Tasks

```
test-project/
├── package.json        # Node version info (Task 1)
├── app.py              # Flask app with bugs + TODOs (Tasks 3, 7, 8, 9, 10, 11)
├── db.py               # DB module, one conn per query (Tasks 6, 12)
├── middleware.py        # Auth decorator (Task 4)
├── test_app.py         # Tests with one expected failure (Task 14)
├── screenshot.png       # Sample image (not used in API mode)
└── requirements.txt     # Dependencies (Task 2)
```

| # | Category | Task | Tests rules |
|---|----------|------|-------------|
| 1 | lookup | Node version | 11, 15 |
| 2 | lookup | Python deps | 11, 15 |
| 3 | explain | Explain app.py | 14, 16 |
| 4 | explain | Explain auth decorator | 14, 16 |
| 5 | search | Find TODOs | 18 |
| 6 | search | List db.py functions | 18 |
| 7 | bugfix | Fix divide_numbers | 3, 17 |
| 8 | bugfix | Fix sanitize_input | 3, 17 |
| 9 | feature | Add /health | 10, 13, 17 |
| 10 | feature | Add POST validation | 10, 13, 17 |
| 11 | feature | Add DELETE /users | 10, 13, 17 |
| 12 | refactor | Refactor db.py pooling | 3, 30 |
| 13 | refactor | Rename function | 3, 30 |
| 14 | test | Run tests + fix | 5, 18, 31 |
| 15 | review | Security review | 12, 16 |

## Output

The script generates:
- `results-sonnet-4.json` / `results-opus-4.json` — raw API data
- `results-sonnet-4.md` / `results-opus-4.md` — formatted markdown tables
- Terminal output with per-task, per-category, and total comparison
