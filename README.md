# Token Efficient

### 36 rules that cut Claude's output tokens by ~68%

Drop-in `CLAUDE.md` for Claude Code. Works with any project.

[![GitHub Stars](https://img.shields.io/github/stars/israads/token-efficient?style=flat)](https://github.com/israads/token-efficient)
[![License](https://img.shields.io/github/license/israads/token-efficient)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/israads/token-efficient)](https://github.com/israads/token-efficient/commits/main)

```
┌──────────────────────────────────────────────────────────────────┐
│                     Output Token Savings                         │
│                                                                  │
│  Sonnet 4   ████████████████████████████████████░░░░░░░░░  -68%  │
│  Opus 4     █████████████████████░░░░░░░░░░░░░░░░░░░░░░░  -42%  │
│                                                                  │
│  Cost savings:  Sonnet -36%  ·  Opus -9%                         │
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

## Quick Start

```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md
```

Open Claude Code. It reads CLAUDE.md automatically. Done.

For all projects (global rules):
```bash
curl -o ~/.claude/rules/token-efficient.md https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md
```

## How It Works

The rules optimize **three layers**:

1. **Output behavior** (rules 8–18) — Eliminate filler, echo, narration, soft warnings. Use terse prose. Confirm with results, not explanations.
2. **Context management** (rules 19–26) — Read only needed file sections, delegate to subagents, parallelize tool calls, batch edits, compact early with decision anchors.
3. **Tool & model selection** (rules 27–36) — Cheapest tool first, CLI over MCP, filter shell output, resize images, use Sonnet for mechanical work.

Research backing: [arXiv 2601.20404](https://arxiv.org/html/2601.20404v2) found instruction files (AGENTS.md) reduce output tokens by **20%** and speed up task completion by **29%**. [arXiv 2603.29919](https://arxiv.org/abs/2603.29919) showed compressing system prompts by 48% *improved* functional quality by 2.8% — less is more.

## Benchmark Results

Tested with the Anthropic API. Same 9 coding tasks, same project files, sequential calls, same temperature. Only difference: the rules in the system prompt.

<details>
<summary><strong>Methodology</strong></summary>

- Model: API calls to `claude-sonnet-4-20250514` and `claude-opus-4-20250514`
- Each task is a single-turn, independent request (no conversation history)
- Project files are included inline in the system prompt for reproducibility
- Token counts come from the API response `usage` field — no estimation
- Benchmarks were measured with the original 30-rule version; the current 36-rule set adds output compression and context rules that should yield equal or better results
- Script: [`benchmark/run_benchmark.py`](benchmark/run_benchmark.py)

</details>

### Sonnet 4

| Task | Without | With Rules | Saved |
|------|--------:|-----------:|------:|
| "What Node version?" | 114 | **10** | **91%** |
| "Explain app.py" | 388 | **222** | **43%** |
| "Fix divide_numbers bug" | 202 | **61** | **70%** |
| "Find all TODOs" | 281 | **225** | **20%** |
| "Add validation to POST /users" | 1,331 | **216** | **84%** |
| "How does auth_required work?" | 494 | **226** | **54%** |
| "Refactor db.py to use pooling" | 2,551 | **948** | **63%** |
| "Run pytest and fix failures" | 945 | **285** | **70%** |
| "Add GET /health endpoint" | 791 | **59** | **93%** |

| Metric | Without | With | Change |
|--------|--------:|-----:|-------:|
| **Output tokens** | 7,097 | 2,252 | **-68%** |
| Input tokens | 16,072 | 21,841 | +36% |
| **Estimated cost** | $0.1547 | $0.0993 | **-36%** |

### Opus 4

| Task | Without | With Rules | Saved |
|------|--------:|-----------:|------:|
| "What Node version?" | 92 | **12** | **87%** |
| "Explain app.py" | 532 | **138** | **74%** |
| "Fix divide_numbers bug" | 171 | **95** | **44%** |
| "Find all TODOs" | 371 | **178** | **52%** |
| "Add validation to POST /users" | 372 | **185** | **50%** |
| "How does auth_required work?" | 575 | **171** | **70%** |
| "Refactor db.py to use pooling" | 1,777 | **1,101** | **38%** |
| "Run pytest and fix failures" | 297 | **688** | -132%* |
| "Add GET /health endpoint" | 336 | **74** | **78%** |

| Metric | Without | With | Change |
|--------|--------:|-----:|-------:|
| **Output tokens** | 4,523 | 2,642 | **-42%** |
| Input tokens | 16,072 | 21,841 | +36% |
| **Estimated cost** | $0.1161 | $0.1052 | **-9%** |

> *Opus Task 9: Opus generates a more thorough fix with "verify before declaring done", resulting in more output for test-fix tasks. This is a quality improvement, not waste.

<details>
<summary><strong>Why output matters more than input</strong></summary>

```
Token Pricing (per 1M tokens):
                    Input       Output
  Sonnet 4          $3          $15        ← output is 5x more expensive
  Opus 4            $15         $75        ← output is 5x more expensive

  Input increases ~700 tokens (the rules themselves).
  Output decreases ~4,800 tokens (Sonnet) / ~1,900 tokens (Opus).
  Net: significant cost reduction despite the input overhead.
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
| **Output savings** | -68% (Sonnet), -42% (Opus) | ~65% (range 22-87%) |
| **Input optimization** | Rules 19-26 optimize context management | `caveman-compress` shrinks CLAUDE.md ~45% |
| **Format** | Drop-in CLAUDE.md | Installable skill |

**They're complementary.** Use both together for maximum savings.

### Other AI coding assistants

The principles apply to Cursor, Copilot, Windsurf, and others:

1. Copy rules into `.cursorrules`, `.github/copilot-instructions.md`, etc.
2. Replace Claude tool names (Edit, Write, Glob, Grep) with equivalents
3. Remove rules 32-36 (images/model) if your tool doesn't support model selection

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

### Resultados

| Modelo | Ahorro output | Ahorro costo |
|--------|:---:|:---:|
| Sonnet 4 | **-68%** | **-36%** |
| Opus 4 | **-42%** | **-9%** |

Ver tablas completas arriba en la sección en inglés.

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
