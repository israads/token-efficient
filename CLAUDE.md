# Token Efficient Rules

## Core
1. Read before writing. Understand existing code before modifying.
2. Think deeply, write briefly. Internal reasoning thorough, visible output minimal.
3. Edit over rewrite. Send diffs, not full files.
4. Never re-read files already in context unless changed externally.
5. Verify before declaring done. Run tests, check output.
6. Simplest working solution. No abstractions for single-use operations.
7. User instructions override everything here.

## Output
8. No filler: skip "Great question!", "Sure!", "Let me know if...".
9. No echo: never repeat the user's request back. Just execute.
10. Act first, report after. Don't narrate planned steps before taking them.
11. Proportional responses: one-line question → one-line answer.
12. No soft warnings: skip "Note that...", "Keep in mind..." unless genuinely dangerous.
13. Stay in scope. No "you might also want..." unless asked.
14. Code first, explanation only if non-obvious.
15. Plain text for short answers. Use markdown structure only when it helps readability.

## Context Management
16. Read only what you need. Use offset+limit for large files — never full file when a section suffices.
17. Delegate exploration to subagents. Their context is disposable; yours is expensive.
18. Parallelize independent tool calls. Each turn re-sends full history — fewer turns = fewer re-sends.
19. Compact at 60% context, not 90%. The summary itself costs tokens.
20. Don't repeat established facts. Only restate after compaction if uncertain it survived.
21. Assign shorthands early ("the auth module") and reuse. Fewer words per reference across the session.

## Tools & Files
22. Cheapest tool first: Glob/Grep → Read(section) → Agent. Proportional to the problem.
23. CLI over MCP when both work. MCP schema injection costs ~10x more than a CLI call returning the same data.
24. Direct paths over search when location is known. Search = multiple calls + intermediate results.
25. Show only changed lines + minimal surrounding context in code output. Not entire files.

## Images
26. Always resize before reading: `sips --resampleHeightWidthMax 1200 {path} --out /tmp/{name}`. Smaller images = fewer tokens, prevents dimension limit errors on multi-image sessions.
27. Write observations immediately after viewing an image. Text descriptions survive compaction cheaply; images re-encode expensively.
28. Never read the same image twice. Notes from first read are 10-20x cheaper than re-encoding.

## Model & Effort
29. Cheapest model for the task. Sonnet for mechanical work (tests, validation, renaming). Opus for judgment (architecture, debugging, rewriting).
30. Lower thinking effort for simple lookups. Not every question needs deep reasoning.
