# Benchmark

Measures token savings from the 30 rules using a controlled test project.

## Quick Start

```bash
./setup.sh
cd test-project
```

Then follow the steps in the main [README.md](../README.md#try-it-yourself--benchmark-in-10-minutes).

## What setup.sh creates

```
test-project/
├── package.json        # Node version info (Task 1)
├── app.py              # Flask app with bug + TODOs (Tasks 2, 3, 5, 10)
├── db.py               # DB module, one conn per query (Task 7)
├── middleware.py        # Auth decorator (Task 6)
├── test_app.py          # Tests with one expected failure (Task 9)
├── screenshot.png       # Sample image (Task 8)
└── requirements.txt     # Dependencies
```

## Recording results

After each session, run `/cost` in Claude Code. Copy the numbers into `results.md`.

The key metrics to compare:
- **Total tokens** (input + output) — overall savings
- **Output tokens** — how much shorter the responses are
- **Turns** — fewer turns = less context re-sent = lower input cost
- **Cost ($)** — the bottom line
