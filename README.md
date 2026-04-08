# Token Efficient

### 36 rules that cut Claude's output tokens by ~59%

Drop-in `CLAUDE.md` for Claude Code. Works with any project.

[![GitHub Stars](https://img.shields.io/github/stars/israads/token-efficient?style=flat)](https://github.com/israads/token-efficient)
[![License](https://img.shields.io/github/license/israads/token-efficient)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/israads/token-efficient)](https://github.com/israads/token-efficient/commits/main)

```
┌──────────────────────────────────────────────────────────────────┐
│            Output Token Savings (15 tasks, 3-run avg)            │
│                                                                  │
│  Sonnet 4   █████████████████████████████░░░░░░░░░░░░░░░  -59%  │
│                                                                  │
│  By category:                                                    │
│    Features   ████████████████████████████████████████░░░  -88%  │
│    Lookups    █████████████████████████████████░░░░░░░░░░  -72%  │
│    Explain    █████████████████████████████░░░░░░░░░░░░░░  -65%  │
│    Bug fixes  ████████████████████████████░░░░░░░░░░░░░░  -64%  │
│    Review     ████████████████████████████░░░░░░░░░░░░░░  -64%  │
│    Refactor   ███████████████████░░░░░░░░░░░░░░░░░░░░░░░  -40%  │
│                                                                  │
│  Cost savings:  -22%  ·  Median task saving:  -64%               │
└──────────────────────────────────────────────────────────────────┘
```

[English](#before--after) · [Español](#español)

---

## Before / After

Same task, same project. Only difference: CLAUDE.md in the project root.

**Task: "What Node version does this project use?"**

```
WITHOUT RULES (114 tokens):                    WITH RULES (10 tokens):

Looking at your project files, I can see       node >=20.11.0
that in `package.json`, there's an             (package.json → engines)
`engines` field specified. The project
requires **Node.js version 20.11.0 or
higher** (>=20.11.0).

This is defined in the `engines` field
of your package.json file, which helps
ensure compatibility...
```

**Task: "Add a GET /health endpoint that returns {"status": "ok"}"**

```
WITHOUT RULES (791 tokens):                    WITH RULES (59 tokens):

I'll add a health check endpoint to your       Added to app.py:
Flask application. Let me first review
the current code structure...                   @app.route("/health")
                                                def health():
Here's the implementation:                          return jsonify({"status": "ok"})
[full file rewrite of app.py, 60+ lines]

I've added the `/health` endpoint to your
application. Here's what it does:
- Returns a JSON response with status "ok"
- Uses a GET method (default for Flask)
- No authentication required...
Let me know if you need any changes!
```

**Task: "Fix divide_numbers — crashes when b is zero"**

```
WITHOUT RULES (202 tokens):                    WITH RULES (61 tokens):

I'll fix the `divide_numbers` function         Fixed in app.py:55 — raises
to handle the zero division case...            ValueError on zero denominator.

[rewrites entire function with docstring,
error handling, type hints, and explanation
of what ZeroDivisionError is]

The fix adds a check before the division
to raise a ValueError with a descriptive
message. Note that this approach...
```

## Real-World Cost Savings

What happens when a team spends **$100/month** on Sonnet 4 API calls, distributed across typical development activities:

```
                         Without rules    With rules     You save
  ─────────────────────────────────────────────────────────────────
  Adding features (40%)    $40.00          $ 4.80         $35.20
  Bug fixes (20%)          $20.00          $ 7.20         $12.80
  Explanations (15%)       $15.00          $ 5.25         $ 9.75
  Refactors (10%)          $10.00          $ 6.00         $ 4.00
  Tests (10%)              $10.00          $ 7.80         $ 2.20
  Code reviews (5%)        $ 5.00          $ 1.80         $ 3.20
  ─────────────────────────────────────────────────────────────────
  TOTAL                   $100.00          $32.85         $67.15
                                                          ^^^^^^
                                    Monthly savings at activity level
```

> The $67 estimate above applies category-specific output savings (-88% features, -64% bugs, -65% explanations, -40% refactors, -22% tests, -64% reviews) to the output token portion of each activity's cost. Since output tokens are 5x more expensive than input, and the rules only add ~700 input tokens, the savings are heavily weighted toward output-heavy activities like feature development.
>
> **Conservative estimate (overall benchmark):** $100 → **$78** (-22% total cost including input overhead). The $67 figure assumes your workload is feature-heavy, which is typical for active development.

| Monthly spend | Conservative (-22%) | Feature-heavy (-67%) | Annual savings |
|--------------:|--------------------:|---------------------:|---------------:|
| $100 | $78 | $33 | **$264 – $804** |
| $500 | $390 | $165 | **$1,320 – $4,020** |
| $1,000 | $780 | $330 | **$2,640 – $8,040** |

### Does quality decrease?

**No.** The rules eliminate waste, not substance. Research confirms this:

- [arXiv 2603.29919](https://arxiv.org/abs/2603.29919) (SkillReducer): Compressing system prompts by 48% **improved** functional quality by 2.8%. Less noise = better attention to what matters.
- [arXiv 2601.20404](https://arxiv.org/html/2601.20404v2) (AGENTS.md study): Instruction files reduced output by 20% while completing tasks **29% faster**. Fewer tokens, same correctness.
- Our Opus benchmark: On the "Run tests + fix" task, Opus with rules produced *more* output than without — it generated a more thorough fix because rule 5 ("verify before declaring done") pushed it to actually test its work. Quality went **up**.

What gets cut: "Great question!", "Let me explain what I'm about to do...", full file rewrites when 3 lines changed, "Let me know if you need anything else!". What stays: the code, the fix, the answer.

## Quick Start

**Claude Code** — drop in project root:
```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md
```

Open Claude Code. It reads CLAUDE.md automatically. Done.

Global (all projects):
```bash
curl -o ~/.claude/rules/token-efficient.md https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md
```

**Cursor** — persistent rules via `.cursor/rules/`:
```bash
mkdir -p .cursor/rules && curl -o .cursor/rules/token-efficient.mdc \
  https://raw.githubusercontent.com/israads/token-efficient/main/.cursor/rules/token-efficient.mdc
```

**GitHub Copilot** — workspace instructions:
```bash
mkdir -p .github && curl -o .github/copilot-instructions.md \
  https://raw.githubusercontent.com/israads/token-efficient/main/.github/copilot-instructions.md
```

**Codex / Gemini CLI / any agent with AGENTS.md support:**
```bash
curl -o AGENTS.md https://raw.githubusercontent.com/israads/token-efficient/main/AGENTS.md
```

**Windsurf / Cline / others** — copy the generic rules:
```bash
# Windsurf
curl -o .windsurfrules https://raw.githubusercontent.com/israads/token-efficient/main/AGENTS.md

# Cline
curl -o .clinerules https://raw.githubusercontent.com/israads/token-efficient/main/AGENTS.md
```

**npx skills** (40+ agents via [skills CLI](https://github.com/anthropics/claude-code/blob/main/skills/README.md)):
```bash
npx skills add israads/token-efficient
```

## How It Works

The rules optimize **three layers**:

1. **Output behavior** (rules 8–18) — Eliminate filler, echo, narration, soft warnings. Use terse prose. Confirm with results, not explanations.
2. **Context management** (rules 19–26) — Read only needed file sections, delegate to subagents, parallelize tool calls, batch edits, compact early with decision anchors.
3. **Tool & model selection** (rules 27–36) — Cheapest tool first, CLI over MCP, filter shell output, resize images, use Sonnet for mechanical work.

Research backing: [arXiv 2601.20404](https://arxiv.org/html/2601.20404v2) found instruction files (AGENTS.md) reduce output tokens by **20%** and speed up task completion by **29%**. [arXiv 2603.29919](https://arxiv.org/abs/2603.29919) showed compressing system prompts by 48% *improved* functional quality by 2.8% — less is more.

## Benchmark Results

> **Note on the headline number:** Our v1 benchmark (9 tasks) reported -68% output savings. The v2 benchmark (15 tasks, 7 categories, 3-run average) reports -59%. This is not a regression — the expanded benchmark includes task types where the baseline is already concise (renames, searches), giving a more realistic and honest picture. Feature tasks still save **-88%**, lookups **-72%**, and the median per-task saving is **-64%**.

### What we measure

The benchmark runs **15 real coding tasks** across 7 categories against a Flask project with 5 files (~400 lines). Each task runs twice through the Anthropic API: once without rules, once with the 36 rules injected as system prompt. Token counts come directly from the API `usage` field — no estimation.

The tasks are designed to test different rule categories:
- **Lookup** (2 tasks) — Tests rules 11, 15: proportional responses, plain text
- **Explain** (2 tasks) — Tests rules 14, 16: code first, terse prose
- **Search** (2 tasks) — Tests rule 18: report only findings
- **Bug fix** (2 tasks) — Tests rules 3, 17: edit over rewrite, confirm with result
- **Feature** (3 tasks) — Tests rules 10, 13, 17: act first, stay in scope
- **Refactor** (2 tasks) — Tests rules 3, 30: diffs, show only changed lines
- **Test/Review** (2 tasks) — Tests rules 5, 12, 18, 31: verify, no soft warnings, filter output

<details>
<summary><strong>Methodology</strong></summary>

- Model: `claude-sonnet-4-20250514` via Anthropic API
- Each task is a single-turn, independent request (no conversation history between tasks)
- Project files (package.json, app.py, db.py, middleware.py, test_app.py) are included inline in the system prompt
- Token counts from API response `usage` field — exact, not estimated
- Cost calculated at Sonnet pricing: $3/M input, $15/M output
- Reproducible: `benchmark/run_benchmark.py` — run it yourself with your API key
- Use `BENCHMARK_RUNS=3` for averaged results across multiple runs

</details>

### Sonnet 4 — Per Task (3-run average)

| # | Category | Task | Without | With Rules | Saved |
|---|----------|------|--------:|-----------:|------:|
| 1 | lookup | Node version | 113 | **10** | **91%** |
| 2 | lookup | Python deps | 266 | **97** | **64%** |
| 3 | explain | Explain app.py | 426 | **159** | **63%** |
| 4 | explain | Explain auth decorator | 429 | **144** | **66%** |
| 5 | search | Find TODOs | 281 | **172** | **39%** |
| 6 | search | List db.py functions | 189 | **123** | **35%** |
| 7 | bugfix | Fix divide_numbers | 195 | **77** | **61%** |
| 8 | bugfix | Fix sanitize_input | 193 | **62** | **68%** |
| 9 | feature | Add /health | 794 | **56** | **93%** |
| 10 | feature | Add POST validation | 1,100 | **171** | **84%** |
| 11 | feature | Add DELETE /users | 964 | **102** | **89%** |
| 12 | refactor | Refactor db.py pooling | 1,926 | **978** | **49%** |
| 13 | refactor | Rename function | 607 | **531** | **13%** |
| 14 | test | Run tests + fix | 1,019 | **799** | **22%** |
| 15 | review | Security review | 447 | **161** | **64%** |

### Sonnet 4 — By Category

Different task types benefit from different rules:

| Category | Without | With Rules | Saved | Key rules |
|----------|--------:|-----------:|------:|-----------|
| **feature** | 2,858 | 329 | **88%** | 10 (act first), 13 (stay in scope), 17 (confirm with result) |
| **lookup** | 379 | 107 | **72%** | 11 (proportional), 15 (plain text) |
| **explain** | 855 | 303 | **65%** | 14 (code first), 16 (terse prose) |
| **bugfix** | 388 | 139 | **64%** | 3 (edit over rewrite), 17 (confirm with result) |
| **review** | 447 | 161 | **64%** | 12 (no soft warnings), 16 (terse prose) |
| **refactor** | 2,533 | 1,509 | **40%** | 3 (edit over rewrite), 30 (show only changed lines) |
| **search** | 470 | 295 | **37%** | 18 (report only findings) |
| **test** | 1,019 | 799 | **22%** | 5 (verify), 18 (report only failures), 31 (filter output) |

### Sonnet 4 — Totals

| Metric | Without | With Rules | Change |
|--------|--------:|----------:|-------:|
| **Output tokens** | **8,949** | **3,642** | **-59%** |
| Input tokens | 26,805 | 37,260 | +39% |
| **Estimated cost** | **$0.2147** | **$0.1664** | **-22%** |

```
Output savings distribution across 15 tasks:
  min: -13%  ·  median: -64%  ·  mean: -60%  ·  max: -93%
```

### Why the savings vary

**Highest savings (-84% to -93%):** Feature tasks. Without rules, Claude narrates its plan, rewrites entire files, adds unsolicited suggestions, and signs off with "Let me know if you need anything else!" With rules, it just writes the code and confirms.

**Medium savings (-61% to -72%):** Lookups, explanations, bug fixes, and reviews. Rules 14 (code first), 16 (terse prose), and 17 (confirm with result) cut the padding. A bug fix goes from a paragraph explaining what ZeroDivisionError is to "Fixed in app.py:55."

**Lower savings (-22% to -40%):** Search, refactor, and test tasks. These are more information-dense — a refactor *needs* to show the new code. A test run *needs* to show what failed. The rules still help (shorter phrasing, no filler), but the floor is higher.

**Lowest (13%):** Rename function. Already a mechanical task with minimal prose — Sonnet doesn't add much fluff even without rules.

<details>
<summary><strong>Why output matters more than input</strong></summary>

```
Token Pricing (per 1M tokens):
                    Input       Output
  Sonnet 4          $3          $15        ← output is 5x more expensive

  The 36 rules add ~700 input tokens per request.
  They save ~5,300 output tokens across 15 tasks.

  Extra input cost:   700 × $3/M  = $0.0021
  Output savings:   5,300 × $15/M = $0.0795

  Net savings: $0.0795 - $0.0021 = $0.0774 per benchmark run
  That's a 38:1 return on the input token investment.
```

</details>

## Beyond the Rules: User-Side Optimizations

The 36 rules tell Claude how to behave. These are things **you** configure for additional savings:

### Environment settings

Add to `~/.claude/settings.json`:

```json
{
  "env": {
    "MAX_THINKING_TOKENS": "8000",
    "CLAUDE_CODE_SUBAGENT_MODEL": "haiku",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "75"
  }
}
```

| Setting | Effect | Savings |
|---------|--------|---------|
| `MAX_THINKING_TOKENS=8000` | Cap extended thinking (default ~32K). 8K suffices for most coding tasks | ~70% thinking cost |
| `CLAUDE_CODE_SUBAGENT_MODEL=haiku` | Exploration subagents use Haiku instead of Sonnet | ~80% per subagent |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=75` | Compact earlier before quality degrades at high context fill | Better output quality |

### .claudeignore

Create `.claudeignore` in your project root:

```
node_modules/
dist/
build/
.next/
coverage/
*.log
*.lock
__pycache__/
.env*
*.min.js
vendor/
```

Prevents Claude from reading build artifacts, dependencies, and logs during exploration. Saves 40-60% of Read tokens.

### Session strategies

| Strategy | What to do | Savings |
|----------|-----------|---------|
| **Task briefs** | Write affected files + desired outcome before starting | Eliminates 2-4 clarification turns |
| **Session handoffs** | Ask Claude to write a structured summary before context limits; start next session with it | Eliminates re-exploration |
| **Spec-first** | For multi-file features: write spec in one session, `/clear`, implement in a fresh session | Avoids 15-40K tokens of exploration noise |
| **`/btw` for lookups** | Use `/btw` for quick questions — answers don't enter conversation history | Zero context cost |
| **`claude -p` for batch** | `for f in *.py; do claude -p "migrate $f"; done` — each invocation has zero history | No accumulated context |

### Tool ecosystem

| Tool | What it does | Savings |
|------|-------------|---------|
| [RTK](https://github.com/rtk-ai/rtk) | Rust CLI that filters shell output before Claude sees it (groups files, collapses repeated lines, strips boilerplate) | 75-92% per command |
| [Headroom](https://github.com/chopratejas/headroom) | Context proxy with AST-aware code compression and KV cache alignment | 73-92% per tool result |
| [Token Optimizer](https://github.com/alexgreensh/token-optimizer) | Claude Code plugin that audits your session for wasted tokens | Diagnostic |
| **≤10 MCP servers** | Each MCP server injects its full schema every turn. Disable unused ones | 50-90% MCP overhead |
| **Subdirectory CLAUDE.md** | Put domain rules in `src/api/CLAUDE.md` — loaded only when Claude touches that directory | On-demand, not always-on |

## Comparison with Similar Projects

| Aspect | token-efficient | [caveman](https://github.com/JuliusBrussee/caveman) |
|--------|----------------|---------|
| **Approach** | Behavioral rules (how the agent works + speaks) | Output style compression (caveman speak) |
| **Scope** | Output + context + tools + images + model selection | Output prose only |
| **Output savings** | -62% overall, -84% on features (Sonnet) | ~65% (range 22-87%) |
| **Input optimization** | Rules 19-26 optimize context management | `caveman-compress` shrinks CLAUDE.md ~45% |
| **Format** | Drop-in for 6+ agents (CLAUDE.md, Cursor, Copilot, Codex, Windsurf, Cline) | Installable skill |

**They're complementary.** Use both together for maximum savings.

### Other AI coding assistants

Rules 1–26 are universal. Rules 27–31 use Claude tool names — adapt for your agent (`Edit` → inline edit, `Glob/Grep` → search, `Agent` → background agent). Rules 35–36 apply if your tool supports model selection.

| Agent | File | Install |
|-------|------|---------|
| Claude Code | `CLAUDE.md` | `curl -o CLAUDE.md ...` |
| Cursor | `.cursor/rules/token-efficient.mdc` | `curl -o .cursor/rules/token-efficient.mdc ...` |
| GitHub Copilot | `.github/copilot-instructions.md` | `curl -o .github/copilot-instructions.md ...` |
| Codex / Gemini CLI | `AGENTS.md` | `curl -o AGENTS.md ...` |
| Windsurf | `.windsurfrules` | `curl -o .windsurfrules ...` (use AGENTS.md content) |
| Cline | `.clinerules` | `curl -o .clinerules ...` (use AGENTS.md content) |

All raw files: `https://raw.githubusercontent.com/israads/token-efficient/main/{file}`

## Verify It Yourself

### API benchmark (exact numbers)

```bash
git clone https://github.com/israads/token-efficient.git
cd token-efficient/benchmark

ANTHROPIC_API_KEY=sk-ant-... python3 run_benchmark.py                                    # Sonnet
BENCHMARK_MODEL=claude-opus-4-20250514 ANTHROPIC_API_KEY=sk-ant-... python3 run_benchmark.py  # Opus
```

### Claude Code sessions (subscription)

```bash
git clone https://github.com/israads/token-efficient.git && cd token-efficient/benchmark
./setup.sh && cd test-project

claude                    # Session 1: WITHOUT rules — run tasks from tasks.md, then /cost
cd .. && ./setup.sh && cd test-project
cp ../../CLAUDE.md . && claude   # Session 2: WITH rules — same tasks, then /cost and compare
```

## The 36 Rules

| # | Category | Rule |
|---|----------|------|
| 1 | Core | Read before writing |
| 2 | Core | Think deep, write brief |
| 3 | Core | Edit over rewrite (diffs, not full files) |
| 4 | Core | Don't re-read files already in context |
| 5 | Core | Verify before declaring done |
| 6 | Core | Simplest working solution |
| 7 | Core | User overrides everything |
| 8 | Output | No filler ("Great question!", "Sure!") |
| 9 | Output | No echo — execute, don't restate |
| 10 | Output | Act first, report after |
| 11 | Output | Proportional responses |
| 12 | Output | No soft warnings unless dangerous |
| 13 | Output | Stay in scope |
| 14 | Output | Code first, explanation if non-obvious |
| 15 | Output | Plain text default |
| 16 | Output | Terse prose: drop filler words, use fragments |
| 17 | Output | Confirm with result, not explanation |
| 18 | Output | Report only changes and failures |
| 19 | Context | Read only needed sections |
| 20 | Context | Delegate exploration to subagents |
| 21 | Context | Parallelize tool calls |
| 22 | Context | Compact at 60%, preserve decisions |
| 23 | Context | Don't repeat established facts |
| 24 | Context | Use shorthands for repeated references |
| 25 | Context | Batch related edits into one turn |
| 26 | Context | Reference by file:line, not re-pasting |
| 27 | Tools | Cheapest tool first |
| 28 | Tools | CLI over MCP |
| 29 | Tools | Direct paths over search |
| 30 | Tools | Show only changed lines |
| 31 | Tools | Filter shell output: failures only |
| 32 | Images | Resize before reading |
| 33 | Images | Describe images immediately in text |
| 34 | Images | Never re-read same image |
| 35 | Model | Cheapest model for the task |
| 36 | Model | Lower effort for simple lookups |

For detailed explanations: [RULES.md](RULES.md)

---

<details>
<summary><a id="español"></a><strong>Español</strong></summary>

## ¿Qué es esto?

36 reglas de comportamiento que pones como `CLAUDE.md` en tu proyecto. Claude Code las lee al iniciar y ajusta: respuestas más cortas, sin relleno, sin narración innecesaria, respuestas proporcionales.

### Ahorro real

Con $100/mes en Sonnet 4: ahorras entre **$22** (conservador) y **$67** (si tu trabajo es mayormente features). La calidad no baja — [estudios académicos](https://arxiv.org/abs/2603.29919) muestran que comprimir instrucciones un 48% *mejora* la calidad un 2.8%.

### Antes / Después

**Tarea: "¿Qué versión de Node usa este proyecto?"**

```
SIN REGLAS (114 tokens):                       CON REGLAS (10 tokens):

Mirando los archivos de tu proyecto,           node >=20.11.0
puedo ver que en `package.json` hay            (package.json → engines)
un campo `engines` especificado.
El proyecto requiere **Node.js versión
20.11.0 o superior**...
```

### Cómo funciona

Las reglas optimizan **tres capas**:

1. **Comportamiento de salida** (reglas 8–18) — Elimina relleno, eco, narración. Prosa concisa. Confirma con resultados.
2. **Gestión de contexto** (reglas 19–26) — Lee solo secciones necesarias, delega a subagentes, paraleliza, agrupa ediciones, compacta temprano.
3. **Herramientas y modelo** (reglas 27–36) — Herramienta más barata primero, CLI sobre MCP, filtra shell, Sonnet para trabajo mecánico.

### Instalar

```bash
# Un proyecto
curl -o CLAUDE.md https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md

# Todos los proyectos
curl -o ~/.claude/rules/token-efficient.md https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md
```

### Resultados (Sonnet 4, 15 tareas, promedio 3 corridas)

| Categoría | Ahorro output |
|-----------|:---:|
| Features (agregar endpoints) | **-88%** |
| Lookups (preguntas simples) | **-72%** |
| Explicaciones | **-65%** |
| Bug fixes | **-64%** |
| Reviews | **-64%** |
| **Total (15 tareas)** | **-59%** |

Costo total: **-22%** · Mediana por tarea: **-64%**. Ver tablas completas arriba.

### Las 36 Reglas

| # | Categoría | Regla |
|---|-----------|-------|
| 1-7 | Core | Leer antes de escribir, pensar profundo/escribir breve, diffs sobre reescritura, no re-leer, verificar, solución simple, usuario manda |
| 8-18 | Output | Sin relleno, sin eco, actuar primero, proporcional, sin advertencias suaves, en alcance, código primero, texto plano, prosa concisa, confirmar con resultado, solo cambios y fallos |
| 19-26 | Contexto | Solo secciones necesarias, subagentes, paralelizar, compactar al 60%, no repetir, abreviaciones, agrupar ediciones, referenciar por archivo:línea |
| 27-31 | Herramientas | Más barata primero, CLI sobre MCP, paths directos, solo líneas cambiadas, filtrar shell |
| 32-34 | Imágenes | Redimensionar, describir en texto, no re-leer |
| 35-36 | Modelo | Modelo más barato, menor esfuerzo para consultas simples |

Para explicaciones detalladas: [RULES.md](RULES.md)

</details>

---

## Sources

Compiled from 20+ sources:
- [AGENTS.md Impact Study (arXiv 2601.20404)](https://arxiv.org/html/2601.20404v2) — instruction files reduce output tokens by 20%
- [SkillReducer (arXiv 2603.29919)](https://arxiv.org/abs/2603.29919) — compressing system prompts by 48% improves quality by 2.8%
- [The Hidden Cost of Readability (arXiv 2508.13666)](https://arxiv.org/html/2508.13666v1) — code formatting = 24.5% of input tokens
- [Context Length Hurts (arXiv 2510.05381)](https://arxiv.org/html/2510.05381v1) — shorter context outperforms longer even with perfect retrieval
- [caveman (JuliusBrussee)](https://github.com/JuliusBrussee/caveman) — output compression via terse prose style
- [claude-token-efficient (drona23)](https://github.com/drona23/claude-token-efficient) — original 8-rule baseline
- [RTK — AI-aware shell filter](https://github.com/rtk-ai/rtk) — 60-90% shell output compression
- [Headroom — context proxy](https://github.com/chopratejas/headroom) — AST-aware code compression
- [6 Ways I Cut My Claude Token Usage (Sabrina.dev)](https://www.sabrina.dev/p/6-ways-i-cut-my-claude-token-usage)
- [18 Token Management Hacks (MindStudio)](https://www.mindstudio.ai/blog/claude-code-token-management-hacks-3)
- [Claude Code Docs — Costs](https://code.claude.com/docs/en/costs) · [Best Practices](https://code.claude.com/docs/en/best-practices) · [Hooks](https://code.claude.com/docs/en/hooks)
- [everything-claude-code (affaan-m)](https://github.com/affaan-m/everything-claude-code/blob/main/docs/token-optimization.md)
- [Anthropic Prompt Caching Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)

## License

MIT
