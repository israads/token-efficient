# The 36 Rules — Detailed Explanations

Each rule, why it matters, and how many tokens it saves.

---

## Core (1–7)

**1. Read before writing.**
Don't edit code you haven't seen. Blind edits break things, cause rollbacks, and multiply turns — each turn re-sends the full conversation.

**2. Think deep, write brief.**
Extended thinking (internal reasoning) is cheap — it doesn't persist in context. Visible output does. Let the model reason hard internally but respond concisely. [arXiv 2508.03346](https://arxiv.org/abs/2508.03346) showed 80% of intermediate reasoning steps are redundant and prunable without accuracy loss.

**3. Edit over rewrite.**
The `Edit` tool sends only the changed lines (~50 tokens). The `Write` tool sends the entire file (~2000+ tokens). For a 3-line change in a 200-line file, that's a 40x difference.

**4. Don't re-read files already in context.**
Every file read injects its full content into the conversation. Reading the same 300-line file twice = 600 lines of duplicated context sitting there permanently.

**5. Verify before declaring done.**
A failed fix triggers "it didn't work → read error → try again → test again" — 3-4 extra turns. Testing before declaring done avoids the retry spiral.

**6. Simplest working solution.**
More code = more tokens generated. Abstractions, helper functions, and "future-proof" patterns for single-use operations waste generation tokens and clutter context for subsequent turns.

**7. User instructions override all.**
Safety valve. Any rule here can be broken when the user explicitly asks for it.

---

## Output (8–18)

**8. No filler.**
"Great question!", "Sure, I'd be happy to help!", "Let me know if you need anything else!" — 50-100 wasted tokens per turn. Across a 30-turn session, that's 1500-3000 tokens of pure noise.

**9. No echo.**
"You want me to fix the authentication bug in the middleware..." before doing it. The user just said that. Repeating it costs 30-80 tokens and adds zero value.

**10. Act first, report after.**
"First I'll read the config file, then I'll locate the function, then I'll update the parameters, and finally I'll run the tests." — All of this narration happens before any action. Just do it and show the result.

**11. Proportional responses.**
"What Node version?" → "v20.11". Not three paragraphs about Node versioning strategy. Match response length to question complexity.

**12. No soft warnings.**
"Note that this approach...", "Keep in mind that...", "Be aware that..." — filler phrases that pad output without actionable content. Only warn when something could genuinely break.

**13. Stay in scope.**
The user asked to fix a CSS bug. Don't suggest refactoring the component, adding dark mode support, and switching to Tailwind. Each unsolicited suggestion is 100-200 wasted tokens.

**14. Code first, explanation after.**
Most of the time the user can read the code. Explaining why you used a `for` loop before showing it is backwards. Show the code — explain only if the approach is non-obvious.

**15. Plain text default.**
A markdown header + bullet list to say "yes, use v20" is structural overhead. Reserve formatting for responses where structure genuinely aids comprehension.

**16. Terse prose.** *(New — inspired by [caveman](https://github.com/JuliusBrussee/caveman))*
Drop filler words: "just", "really", "basically", "simply", "actually", "in order to". Use sentence fragments and short synonyms. Leave code blocks, technical terms, and git messages untouched. This alone can compress prose output by 20-40% without losing meaning. A 2026 study showed constraining models to brief responses improved accuracy by 26 percentage points on certain benchmarks — brevity isn't just cheaper, it's often better.

**17. Confirm with result, not explanation.**
"Fixed in `app.py:42`" is 6 tokens. "I've updated the divide_numbers function in app.py at line 42 to add a zero-division check that raises a ValueError when the denominator is zero" is 35 tokens. Same information, 6x the cost. Lead with the outcome and location.

**18. Report only changes and failures.**
After running tests, don't list every passing test. Report only what failed or what changed. "All 12 tests pass" is fine. Listing all 12 test names and their results is not. Similarly, when editing files, don't confirm unchanged files are still fine.

---

## Context (19–26)

**19. Read only needed sections.**
A 500-line file = ~2000 tokens. If you need lines 40-60, reading just those 20 lines = ~80 tokens. That's **25x less**. Use `offset` and `limit` parameters.

**20. Delegate to subagents.**
A subagent exploring 15 files consumes tokens in its own context window, not yours. It returns a summary (~200 tokens) instead of flooding your context with ~15,000 tokens of raw file content.

**21. Parallelize tool calls.**
Each turn re-sends the **entire** conversation history as input. Three tools called sequentially = 3 turns = 3x context re-sent. Three tools in parallel = 1 turn = 1x. Same work, one-third the input tokens.

**22. Compact at 60%, not 90%. Preserve decisions.** *(Enhanced)*
`/compact` generates a summary that itself consumes tokens. Compacting at 90% leaves almost no room for the summary + your next message. At 60% you have headroom. Before compacting, explicitly state which files were modified, decisions made, and patterns chosen — compaction loses specifics without explicit anchors. [arXiv 2510.05381](https://arxiv.org/html/2510.05381v1) showed context length alone degrades performance by 13.9-85% even with perfect retrieval — shorter, focused context consistently outperforms longer comprehensive context.

**23. Don't repeat established facts.**
Re-explaining the project structure, re-listing files, re-describing the problem — all of this is already in the conversation history. The model can see it. Only restate after `/compact` if you suspect information was lost.

**24. Assign shorthands.**
"The authentication and authorization middleware in `src/middleware/auth/`" = 12 tokens every time you reference it. "The auth module" = 3 tokens. Define it once, reuse everywhere. Small compression, big savings across a long session.

**25. Batch related edits.**
If you need to edit 3 files for one feature, do all 3 edits in one turn. Each turn re-sends the full conversation history. Three turns for three related edits means 3x the input token cost. Batching them into one turn sends the history once. This is especially impactful in long sessions where the accumulated context is large.

**26. Reference code by `file:line`, not by re-pasting.** *(New — from [arXiv 2508.13666](https://arxiv.org/html/2508.13666v1))*
When referring to code already in context, use `auth.go:142-167` instead of pasting the block again. The content is already in the KV cache from the initial read. Re-pasting forces re-encoding of identical content, wasting both input tokens and cache efficiency. Research shows code formatting alone consumes ~24.5% of input tokens — referencing by location avoids re-paying that cost.

---

## Tools (27–31)

**27. Cheapest tool first.**
`Glob` returns file paths (~100 tokens). `Grep` returns matching lines (~200 tokens). `Agent` can consume ~10,000+ tokens exploring. Use the tool proportional to the problem — don't send a research team when you need a phone book.

**28. CLI over MCP.**
MCP servers inject their full tool schema into context on **both** the request and response. The GitHub MCP schema alone is ~2000 tokens. Running `gh issue view 123` via bash returns ~200 tokens of data. Same information, 10x difference.

**29. Direct paths over search.**
If you know the file is at `src/auth/middleware.ts`, read it directly. Searching for it means: run glob → scan results → pick match → read file. That's 3-4 tool calls instead of 1, each re-sending the full context.

**30. Show only changed lines.**
When presenting code changes, show the modified lines plus 2-3 lines of surrounding context for orientation. Printing a 200-line file to highlight a 3-line change wastes ~800 tokens.

**31. Filter shell output.** *(New — inspired by [RTK](https://github.com/rtk-ai/rtk))*
When running tests, builds, or other verbose commands, don't dump full output into context. Show only failures and changes. Collapse repeated lines (e.g., "connection refused ×47" instead of 47 identical lines). Strip boilerplate headers and formatting. Full test suite output can be 5,000+ tokens; the actionable information (which tests failed and why) is typically under 200. This applies to test runners, build tools, linters, and log output.

---

## Images (32–34)

**32. Resize before reading.**
Images are tokenized proportionally to pixel area. A 2400px screenshot = ~1600 tokens. Resized to 1200px = ~400 tokens. **4x reduction.** Also prevents the "dimension limit for multi-image requests (2000px)" error that blocks all subsequent image reads.

```bash
# macOS
sips --resampleHeightWidthMax 1200 "{path}" --out "/tmp/{filename}"

# Linux
convert "{path}" -resize 1200x1200\> "/tmp/{filename}"
```

**33. Describe observations immediately.**
After viewing a screenshot, write down your observations in text. Text descriptions survive `/compact` efficiently (~50 tokens). The original image stays in context at full token cost and compresses poorly. Your notes replace the need to keep the image around.

**34. Never re-read the same image.**
Each read re-injects the full image encoding. Your text notes from the first viewing are 10-20x cheaper. If you need to reference the image later, read your notes instead.

---

## Model (35–36)

**35. Cheapest model for the task.**
Use Sonnet/Haiku for mechanical work: running tests, formatting, renaming variables, validation checklists, generating boilerplate. Reserve Opus for tasks requiring judgment: architecture decisions, complex debugging, nuanced rewriting. Sonnet is ~5x cheaper than Opus for the same token count.

**36. Lower effort for simple tasks.**
"What's the project name?" doesn't need 10,000 thinking tokens. Use `/effort low` for lookups and simple questions. Save deep reasoning for problems that actually require it.
