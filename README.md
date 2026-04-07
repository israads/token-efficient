# Token Efficient — 30 Rules to Cut AI Coding Assistant Costs

30 compact rules for your `CLAUDE.md` that reduce token waste in Claude Code sessions. Works with any project.

## Try It Yourself — Benchmark in 10 Minutes

Run the same tasks with and without the rules. See the difference.

### Step 1: Setup the test project

```bash
git clone https://github.com/israads/token-efficient.git
cd token-efficient/benchmark
./setup.sh
cd test-project
```

### Step 2: Run WITHOUT rules (baseline)

Open Claude Code normally — no CLAUDE.md, default behavior:

```bash
claude
```

Now copy-paste these 10 prompts, one by one. These are everyday tasks you'd normally ask Claude:

```
1. What version of Node does this project use?
2. Explain what app.py does
3. The function divide_numbers on line 42 of app.py crashes when b is zero. Fix it.
4. Find all TODO comments across the project
5. Add validation to POST /users — name can't be empty, email needs an @
6. How does the auth_required decorator in middleware.py work?
7. Refactor db.py to use connection pooling instead of opening a new connection every query
8. Look at screenshot.png and describe what you see
9. Run pytest and fix whatever fails
10. Add a GET /health endpoint that returns {"status": "ok"}
```

After the 10 tasks, type `/cost` and **screenshot the result** or copy the numbers.

Then exit:
```
/exit
```

### Step 3: Install the rules

```bash
cp ../CLAUDE.md .
```

That's it. Claude Code reads `CLAUDE.md` automatically on startup.

### Step 4: Run WITH rules

Open a fresh session:

```bash
claude
```

Run the **exact same 10 prompts** from Step 2 — same wording, same order.

After the 10 tasks, type `/cost` again and save the result.

### Step 5: Compare

You now have two sets of numbers. Fill in your results:

| Metric | Without Rules | With Rules | Savings |
|--------|:------------:|:----------:|:-------:|
| Input tokens | | | % |
| Output tokens | | | % |
| Total cost ($) | | | % |
| Turns | | | % |

Expected savings based on community testing:
- **Output tokens**: 40-65% less
- **Input tokens**: 15-30% less (fewer turns = less context re-sent)
- **Total cost**: 25-45% less

> Share your results! Open an issue with your numbers so we can build a community benchmark.

---

## What Each Task Tests

| # | Prompt | What you'll notice |
|---|--------|--------------------|
| 1 | Node version lookup | Without rules: paragraph explaining Node versioning. With rules: just "v20.11" |
| 2 | Explain app.py | Without rules: reads entire file, writes 500-word essay. With rules: concise summary |
| 3 | Fix divide_numbers | Without rules: rewrites whole function + explains. With rules: edits the one line |
| 4 | Find TODOs | Without rules: searches one file at a time. With rules: single grep, parallel calls |
| 5 | Add validation | Without rules: adds validation + error handling + tests + suggestions. With rules: just the validation |
| 6 | Explain auth decorator | Without rules: full walkthrough + security recommendations. With rules: what it does in 2-3 lines |
| 7 | Refactor db.py | Without rules: rewrites entire file. With rules: edits only the connection logic |
| 8 | Read screenshot | Without rules: reads full-size image. With rules: resizes first (4x fewer tokens) |
| 9 | Run tests + fix | Without rules: narrates each step before doing it. With rules: runs, fixes, reports |
| 10 | Add /health endpoint | Without rules: endpoint + tests + docs + suggestions. With rules: just the endpoint |

---

## Install for Real Projects

Once you've seen the benchmark results, use it in your actual projects:

```bash
# Option A: Per-project (recommended)
cp CLAUDE.md /path/to/your/project/CLAUDE.md

# Option B: Global (applies to every project)
cp CLAUDE.md ~/.claude/rules/token-efficient.md
```

---

## The 30 Rules — Explained

### Core (1–7)

**1. Read before writing.**
Don't edit code you haven't seen. Blind edits cause rollbacks → more turns → more tokens re-sent.

**2. Think deeply, write briefly.**
Internal reasoning (thinking tokens) is cheap and doesn't persist. Visible output is expensive and stays in context forever.

**3. Edit over rewrite.**
`Edit` sends only changed lines (~50 tokens). `Write` sends the entire file (~2000+ tokens). For a 3-line change in a 200-line file, that's 40x difference.

**4. Never re-read files already in context.**
Reading a 300-line file twice = 600 lines permanently duplicated in your context window.

**5. Verify before declaring done.**
A failed fix triggers a retry spiral: read error → try again → test again. 3-4 extra turns that each re-send the full conversation.

**6. Simplest working solution.**
More code = more tokens generated + more context for every future turn.

**7. User instructions override everything.**
Safety valve so you can break any rule when needed.

### Output (8–15)

**8. No filler.**
"Great question!", "Sure, I'd be happy to help!" — 50-100 wasted tokens per turn. Over 30 turns: 1500-3000 tokens of noise.

**9. No echo.**
Repeating "You want me to fix the auth bug..." before fixing it. You just said that. 30-80 tokens wasted.

**10. Act first, report after.**
"First I'll read the file, then find the function, then..." — narrating steps before taking them. Just do it.

**11. Proportional responses.**
"What Node version?" → "v20.11". Not three paragraphs.

**12. No soft warnings.**
"Note that...", "Keep in mind..." — skip unless something could genuinely break.

**13. Stay in scope.**
You asked to fix a CSS bug. Don't suggest dark mode, Tailwind migration, and component refactoring. Each suggestion: 100-200 wasted tokens.

**14. Code first, explanation after.**
Show the code. Explain only if the approach is non-obvious.

**15. Plain text for short answers.**
A markdown header + bullet list to say "yes, use v20" is structural overhead.

### Context Management (16–21)

**16. Read only what you need.**
500-line file = ~2000 tokens. Lines 40-60 only = ~80 tokens. **25x less.**

**17. Delegate to subagents.**
Subagent explores 15 files in its own context → returns 200-token summary. Without subagent: 15,000 tokens of file content in your main window.

**18. Parallelize tool calls.**
Each turn re-sends the **entire** conversation. 3 sequential tool calls = 3 turns = 3x context re-sent. 3 parallel calls = 1 turn = 1x.

**19. Compact at 60%, not 90%.**
The summary from `/compact` itself costs tokens. At 90% there's no room left.

**20. Don't repeat established facts.**
The project structure is already in the conversation. Don't re-list it every time.

**21. Assign shorthands.**
"The auth and authorization middleware in src/middleware/auth/" = 12 tokens per mention. "The auth module" = 3 tokens. Adds up fast.

### Tools & Files (22–25)

**22. Cheapest tool first.**
Glob (~100 tokens) → Grep (~200 tokens) → Agent (~10,000+ tokens). Match the tool to the problem.

**23. CLI over MCP.**
MCP schema injection: ~2000 tokens. Same data via CLI: ~200 tokens. 10x difference.

**24. Direct paths over search.**
If you know where the file is, read it directly. Searching = 3-4 tool calls instead of 1.

**25. Show only changed lines.**
Don't print a 200-line file to show a 3-line change. Show the diff + 2-3 lines of context.

### Images (26–28)

**26. Always resize before reading.**
2400px screenshot = ~1600 tokens. Resized to 1200px = ~400 tokens. **4x reduction.**

```bash
sips --resampleHeightWidthMax 1200 "{path}" --out "/tmp/{filename}"
```

**27. Describe images immediately.**
Write text notes right after viewing. Text survives `/compact` cheaply (~50 tokens). The image stays at full cost.

**28. Never re-read the same image.**
Each re-read re-injects the full encoding. Your text notes are 10-20x cheaper.

### Model & Effort (29–30)

**29. Cheapest model for the task.**
Sonnet for mechanical work (tests, formatting, renaming). Opus for judgment (architecture, debugging). Sonnet is ~5x cheaper.

**30. Lower thinking effort for simple tasks.**
"What's the project name?" doesn't need deep reasoning. Use `/effort low`.

---

## Why Input Tokens Matter More Than Output

```
┌─────────────────────────────────────────────┐
│           Token Cost Distribution            │
│                                              │
│  Input (context re-sent each turn)   ~93%  █████████████████████████████████░░░
│  Thinking (internal reasoning)        ~3%  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
│  Output (visible response)            ~4%  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
│                                              │
└─────────────────────────────────────────────┘
```

Most guides focus on making output shorter. That helps, but the **real savings come from controlling input**: fewer file reads, parallel tool calls, subagent delegation, and proactive compaction.

---

## Sources

Compiled from 15+ sources:
- [claude-token-efficient (drona23)](https://github.com/drona23/claude-token-efficient) — original 8-rule baseline
- [6 Ways I Cut My Claude Token Usage (Sabrina.dev)](https://www.sabrina.dev/p/6-ways-i-cut-my-claude-token-usage)
- [Optimize Context by 60% (Medium)](https://medium.com/@jpranav97/stop-wasting-tokens-how-to-optimize-claude-code-context-by-60-bfad6fd477e5)
- [HN: Universal Claude.md Discussion](https://news.ycombinator.com/item?id=47581701)
- [18 Token Management Hacks (MindStudio)](https://www.mindstudio.ai/blog/claude-code-token-management-hacks-3)
- [Claude Code Official Docs — Costs](https://code.claude.com/docs/en/costs)
- [Claude Code Official Docs — Best Practices](https://code.claude.com/docs/en/best-practices)

## License

MIT
