# Token Efficient

### 36 rules that cut Claude's output tokens by ~59%

Drop-in for Claude Code, Cursor, Copilot, Codex, Windsurf, Cline. Works with any project.

[![GitHub Stars](https://img.shields.io/github/stars/israads/token-efficient?style=flat)](https://github.com/israads/token-efficient)
[![License](https://img.shields.io/github/license/israads/token-efficient)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/israads/token-efficient)](https://github.com/israads/token-efficient/commits/main)

```
┌──────────────────────────────────────────────────────────────────┐
│            Output Token Savings (15 tasks, 3-run avg)            │
│                                                                  │
│  Sonnet 4   █████████████████████████████░░░░░░░░░░░░░░░  -59%  │
│  Opus 4     ████████████████████████░░░░░░░░░░░░░░░░░░░░  -42%  │
│                                                                  │
│  By category (Sonnet):                                           │
│    Features   ████████████████████████████████████████░░░  -88%  │
│    Lookups    █████████████████████████████████░░░░░░░░░░  -72%  │
│    Explain    █████████████████████████████░░░░░░░░░░░░░░  -65%  │
│    Bug fixes  ████████████████████████████░░░░░░░░░░░░░░  -64%  │
│    Reviews    ████████████████████████████░░░░░░░░░░░░░░  -64%  │
│    Refactor   ███████████████████░░░░░░░░░░░░░░░░░░░░░░░  -40%  │
│                                                                  │
│  Cost savings:  -22%  ·  Median task saving:  -64%               │
└──────────────────────────────────────────────────────────────────┘
```

[English](#before--after) · [Español](#español)

---

## Before / After

**Task: "What Node version does this project use?"**

```
WITHOUT RULES (114 tokens):                    WITH RULES (10 tokens):

Looking at your project files, I can see       node >=20.11.0
that in `package.json`, there's an             (package.json → engines)
`engines` field specified. The project
requires **Node.js version 20.11.0 or
higher** (>=20.11.0)...
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
...Let me know if you need any changes!
```

## Install

### Claude Code (easiest)

Paste into Claude Code chat:

```
Install this globally: https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md
```

Claude will run the curl command for you. Or manually:

```bash
# Global (all projects)
curl -o ~/.claude/rules/token-efficient.md \
  https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md

# Single project
curl -o CLAUDE.md https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md
```

### Other agents

| Agent | Command |
|-------|---------|
| **Cursor** | `mkdir -p .cursor/rules && curl -o .cursor/rules/token-efficient.mdc https://raw.githubusercontent.com/israads/token-efficient/main/.cursor/rules/token-efficient.mdc` |
| **GitHub Copilot** | `mkdir -p .github && curl -o .github/copilot-instructions.md https://raw.githubusercontent.com/israads/token-efficient/main/.github/copilot-instructions.md` |
| **Codex / Gemini CLI** | `curl -o AGENTS.md https://raw.githubusercontent.com/israads/token-efficient/main/AGENTS.md` |
| **Windsurf** | `curl -o .windsurfrules https://raw.githubusercontent.com/israads/token-efficient/main/AGENTS.md` |
| **Cline** | `curl -o .clinerules https://raw.githubusercontent.com/israads/token-efficient/main/AGENTS.md` |

Rules 1–26 are universal. Rules 27–31 use Claude tool names — adapt for your agent (`Edit` → inline edit, `Glob/Grep` → search). Rules 35–36 apply if your tool supports model selection.

## How It Works

Three layers:

1. **Output behavior** (rules 8–18) — No filler, no echo, no narration. Terse prose. Confirm with results, not explanations.
2. **Context management** (rules 19–26) — Read only needed sections, delegate to subagents, parallelize calls, compact early, batch edits.
3. **Tool & model selection** (rules 27–36) — Cheapest tool first, CLI over MCP, filter shell output, resize images, Sonnet for mechanical work.

Research backing: [arXiv 2601.20404](https://arxiv.org/html/2601.20404v2) — instruction files reduce output tokens 20%, speed up tasks 29%. [arXiv 2603.29919](https://arxiv.org/abs/2603.29919) — compressing system prompts 48% *improved* quality 2.8%.

## Benchmark Results

### Does quality decrease?

**No.** Rules eliminate waste, not substance.

- [SkillReducer (arXiv 2603.29919)](https://arxiv.org/abs/2603.29919): compressing prompts 48% **improved** quality 2.8%.
- [AGENTS.md study (arXiv 2601.20404)](https://arxiv.org/html/2601.20404v2): instruction files cut output 20% while tasks completed **29% faster**.
- Opus "run tests + fix": with rules, Opus produced *more* output (+132%) — it actually ran the tests and fixed them. Rule 5 ("verify before done") pushed quality **up**.

What gets cut: "Great question!", "Let me explain what I'm about to do...", full file rewrites for 3-line changes. What stays: the code, the fix, the answer.

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

### Sonnet 4 — Totals

| Metric | Without | With Rules | Change |
|--------|--------:|----------:|-------:|
| **Output tokens** | **8,949** | **3,642** | **-59%** |
| Input tokens | 26,805 | 37,260 | +39% |
| **Estimated cost** | **$0.2147** | **$0.1664** | **-22%** |

```
Output savings: min -13% · median -64% · mean -60% · max -93%
```

### Opus 4 — Per Task (1 run)

| # | Task | Without | With Rules | Saved |
|---|------|--------:|-----------:|------:|
| 1 | Node version | 92 | **12** | **-87%** |
| 2 | Explain app.py | 532 | **138** | **-74%** |
| 3 | Fix divide_numbers | 171 | **95** | **-44%** |
| 4 | Find TODOs | 371 | **178** | **-52%** |
| 5 | Add POST validation | 372 | **185** | **-50%** |
| 6 | Explain auth decorator | 575 | **171** | **-70%** |
| 7 | Refactor db.py pooling | 1,777 | **1,101** | **-38%** |
| 8 | Run tests + fix | 297 | 688 | +132%* |
| 9 | Add /health | 336 | **74** | **-78%** |

*Rule 5 ("verify before done") pushed Opus to actually run and fix the tests — more output, better result.

### Opus 4 — Totals

| Metric | Without | With Rules | Change |
|--------|--------:|----------:|-------:|
| **Output tokens** | **4,523** | **2,642** | **-42%** |
| Input tokens | 16,072 | 21,841 | +36% |

<details>
<summary><strong>Methodology</strong></summary>

- Sonnet: `claude-sonnet-4-20250514`, 3-run average. Opus: `claude-opus-4-20250514`, 1 run.
- 15 tasks across 7 categories against a Flask project (5 files, ~400 lines)
- Each task: single-turn request, project files inline in system prompt
- Token counts from API `usage` field — exact, not estimated
- Reproducible: `benchmark/run_benchmark.py`

</details>

## Extra Savings (Claude Code)

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

Create `.claudeignore` to block build artifacts from being read:

```
node_modules/
dist/ build/ .next/ coverage/
*.log *.lock __pycache__/ .env* *.min.js vendor/
```

## Comparison with Similar Projects

| Aspect | token-efficient | [caveman](https://github.com/JuliusBrussee/caveman) |
|--------|----------------|---------|
| **Approach** | Behavioral rules (how the agent works + speaks) | Output style compression (caveman speak) |
| **Scope** | Output + context + tools + images + model selection | Output prose only |
| **Output savings** | -59% Sonnet, -42% Opus | ~65% (range 22-87%) |
| **Input optimization** | Rules 19-26 optimize context management | `caveman-compress` shrinks CLAUDE.md ~45% |
| **Format** | Drop-in for 6+ agents | Installable skill |

**They're complementary.** Use both for maximum savings.

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

## Verify It Yourself

```bash
git clone https://github.com/israads/token-efficient.git
cd token-efficient/benchmark
ANTHROPIC_API_KEY=sk-ant-... python3 run_benchmark.py
```

---

<details>
<summary><a id="español"></a><strong>Español</strong></summary>

## ¿Qué es esto?

36 reglas de comportamiento que pones como `CLAUDE.md` en tu proyecto. Claude Code las lee al iniciar y ajusta: respuestas más cortas, sin relleno, sin narración innecesaria, respuestas proporcionales.

### Instalar

Pega en el chat de Claude Code:

```
Instala esto globalmente: https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md
```

O manualmente:

```bash
curl -o ~/.claude/rules/token-efficient.md \
  https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md
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

Opus 4 (9 tareas, 1 corrida): **-42%** output.

Costo total: **-22%** · Mediana por tarea: **-64%**.

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

<details>
<summary><strong>Sources</strong></summary>

- [AGENTS.md Impact Study (arXiv 2601.20404)](https://arxiv.org/html/2601.20404v2)
- [SkillReducer (arXiv 2603.29919)](https://arxiv.org/abs/2603.29919)
- [The Hidden Cost of Readability (arXiv 2508.13666)](https://arxiv.org/html/2508.13666v1)
- [Context Length Hurts (arXiv 2510.05381)](https://arxiv.org/html/2510.05381v1)
- [caveman (JuliusBrussee)](https://github.com/JuliusBrussee/caveman)
- [claude-token-efficient (drona23)](https://github.com/drona23/claude-token-efficient)
- [RTK — AI-aware shell filter](https://github.com/rtk-ai/rtk)
- [Headroom — context proxy](https://github.com/chopratejas/headroom)
- [6 Ways I Cut My Claude Token Usage (Sabrina.dev)](https://www.sabrina.dev/p/6-ways-i-cut-my-claude-token-usage)
- [18 Token Management Hacks (MindStudio)](https://www.mindstudio.ai/blog/claude-code-token-management-hacks-3)
- [Claude Code Docs](https://code.claude.com/docs/en/costs)

</details>

## License

MIT
