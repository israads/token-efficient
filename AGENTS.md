# Token Efficient Rules

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
27. Cheapest operation first: search → read section → read full file → agent exploration.
28. Prefer CLI commands over plugin/extension APIs when both work. Schemas add overhead.
29. Direct paths over search when location is known.
30. Show only changed lines + minimal surrounding context.
31. Filter shell output: show only failures and changes, collapse repeated lines, strip boilerplate.

## Images
32. Resize before reading. Cap at 1200px to reduce token cost ~4x.
33. Describe observations immediately in text. Text survives compaction; images don't.
34. Never re-read same image. Notes are 10-20x cheaper than re-encoding.

## Model
35. Cheapest model for the task. Use smaller models for mechanical work; reserve larger for judgment.
36. Lower effort for simple lookups. Not every question needs deep reasoning.
