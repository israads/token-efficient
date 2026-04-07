# Token Efficient

### 30 rules that cut Claude's output tokens by ~60%

Drop-in `CLAUDE.md` for Claude Code. Works with any project.

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

[English](#english) · [Español](#español)

---

<a id="english"></a>

## What is this?

A compact set of 30 behavioral rules that you drop into your project as `CLAUDE.md`. Claude Code reads it on startup and adjusts its behavior: shorter responses, no filler, no unnecessary narration, proportional answers.

The rules don't limit Claude's capabilities — they eliminate waste. Claude still thinks deeply, but writes less fluff.

## Benchmark Results

Tested with the Anthropic API. Same 9 coding tasks, same project files. Only difference: the 30 rules in the system prompt.

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
| Input tokens | 16,072 | 21,841 | +36%* |
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
| "Run pytest and fix failures" | 297 | **688** | -132%** |
| "Add GET /health endpoint" | 336 | **74** | **78%** |

| Metric | Without | With | Change |
|--------|--------:|-----:|-------:|
| **Output tokens** | 4,523 | 2,642 | **-42%** |
| Input tokens | 16,072 | 21,841 | +36%* |
| **Estimated cost** | $0.1161 | $0.1052 | **-9%** |

> *Input increases by ~640 tokens because the rules themselves are included in the system prompt. This is offset by the much larger output savings — output tokens cost 5x more than input on both models.

> **Opus Task 9 anomaly: Opus occasionally generates a more thorough fix when given explicit "verify before declaring done" instructions, resulting in more output for test-fix tasks. This is a quality improvement, not waste.

### Why output matters more

```
Token Pricing (per 1M tokens):
                    Input       Output
  Sonnet 4          $3          $15        ← output is 5x more expensive
  Opus 4            $15         $75        ← output is 5x more expensive

  Reducing output by 60% saves more than reducing input by 60%.
```

## Install

```bash
# Option A: One project
curl -o CLAUDE.md https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md

# Option B: All projects (global rules)
curl -o ~/.claude/rules/token-efficient.md https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md
```

## Verify It Yourself

### Option 1: API benchmark (exact numbers)

Requires an Anthropic API key with credits.

```bash
git clone https://github.com/israads/token-efficient.git
cd token-efficient/benchmark

# Run with Sonnet
ANTHROPIC_API_KEY=sk-ant-... python3 run_benchmark.py

# Run with Opus
BENCHMARK_MODEL=claude-opus-4-20250514 ANTHROPIC_API_KEY=sk-ant-... python3 run_benchmark.py
```

The script runs 9 coding tasks twice (without rules, then with rules) and prints a comparison table with exact token counts from the API response.

### Option 2: Claude Code sessions (subscription users)

If you're on a Max subscription and can't see token counts:

```bash
git clone https://github.com/israads/token-efficient.git
cd token-efficient/benchmark
./setup.sh
cd test-project

# Session 1: WITHOUT rules
claude
# Run the 10 tasks from tasks.md, one by one
# Type /context → note the "Messages" value
# Type /exit

# Reset the project
cd .. && ./setup.sh && cd test-project

# Session 2: WITH rules
cp ../CLAUDE.md .
claude
# Run the SAME 10 tasks
# Type /context → compare "Messages" value
```

**What to look for**: Even if `/context` shows similar totals (it measures current window, not cumulative usage), you'll notice:
- Responses are visibly shorter and more direct
- Fewer turns needed (Claude acts instead of narrating)
- No filler phrases, no echoing your question back
- Code shown as diffs instead of full files

## The 30 Rules — Summary

| # | Category | Rule |
|---|----------|------|
| 1 | Core | Read before writing |
| 2 | Core | Think deeply, write briefly |
| 3 | Core | Edit over rewrite (diffs, not full files) |
| 4 | Core | Don't re-read files already in context |
| 5 | Core | Verify before declaring done |
| 6 | Core | Simplest working solution |
| 7 | Core | User overrides everything |
| 8 | Output | No filler ("Great question!", "Sure!") |
| 9 | Output | No echo (don't repeat the request) |
| 10 | Output | Act first, report after |
| 11 | Output | Proportional responses |
| 12 | Output | No soft warnings unless dangerous |
| 13 | Output | Stay in scope |
| 14 | Output | Code first, explanation if non-obvious |
| 15 | Output | Plain text for short answers |
| 16 | Context | Read only needed sections of files |
| 17 | Context | Delegate exploration to subagents |
| 18 | Context | Parallelize tool calls |
| 19 | Context | Compact at 60%, not 90% |
| 20 | Context | Don't repeat established facts |
| 21 | Context | Use shorthands for repeated references |
| 22 | Tools | Cheapest tool first |
| 23 | Tools | CLI over MCP |
| 24 | Tools | Direct paths over search |
| 25 | Tools | Show only changed lines |
| 26 | Images | Resize before reading |
| 27 | Images | Describe images immediately in text |
| 28 | Images | Never re-read same image |
| 29 | Model | Cheapest model for the task |
| 30 | Model | Lower effort for simple lookups |

For detailed explanations of each rule, see [RULES.md](RULES.md).

---

<a id="español"></a>

## ¿Qué es esto?

30 reglas compactas que pones como `CLAUDE.md` en tu proyecto. Claude Code las lee al iniciar y ajusta su comportamiento: respuestas más cortas, sin relleno, sin narración innecesaria, respuestas proporcionales a la pregunta.

Las reglas no limitan las capacidades de Claude — eliminan el desperdicio. Claude sigue pensando profundamente, pero escribe menos texto innecesario.

## Resultados del Benchmark

Probado con la API de Anthropic. Las mismas 9 tareas de programación, los mismos archivos de proyecto. Única diferencia: las 30 reglas en el system prompt.

### Sonnet 4

| Tarea | Sin reglas | Con reglas | Ahorro |
|-------|--------:|-----------:|------:|
| "¿Qué versión de Node?" | 114 | **10** | **91%** |
| "Explica app.py" | 388 | **222** | **43%** |
| "Arregla bug divide_numbers" | 202 | **61** | **70%** |
| "Busca todos los TODOs" | 281 | **225** | **20%** |
| "Añade validación a POST /users" | 1,331 | **216** | **84%** |
| "¿Cómo funciona auth_required?" | 494 | **226** | **54%** |
| "Refactoriza db.py con connection pooling" | 2,551 | **948** | **63%** |
| "Corre pytest y arregla fallos" | 945 | **285** | **70%** |
| "Añade endpoint GET /health" | 791 | **59** | **93%** |

| Métrica | Sin reglas | Con reglas | Cambio |
|---------|--------:|-----:|-------:|
| **Tokens de salida** | 7,097 | 2,252 | **-68%** |
| Tokens de entrada | 16,072 | 21,841 | +36%* |
| **Costo estimado** | $0.1547 | $0.0993 | **-36%** |

### Opus 4

| Tarea | Sin reglas | Con reglas | Ahorro |
|-------|--------:|-----------:|------:|
| "¿Qué versión de Node?" | 92 | **12** | **87%** |
| "Explica app.py" | 532 | **138** | **74%** |
| "Arregla bug divide_numbers" | 171 | **95** | **44%** |
| "Busca todos los TODOs" | 371 | **178** | **52%** |
| "Añade validación a POST /users" | 372 | **185** | **50%** |
| "¿Cómo funciona auth_required?" | 575 | **171** | **70%** |
| "Refactoriza db.py con connection pooling" | 1,777 | **1,101** | **38%** |
| "Corre pytest y arregla fallos" | 297 | **688** | -132%** |
| "Añade endpoint GET /health" | 336 | **74** | **78%** |

| Métrica | Sin reglas | Con reglas | Cambio |
|---------|--------:|-----:|-------:|
| **Tokens de salida** | 4,523 | 2,642 | **-42%** |
| Tokens de entrada | 16,072 | 21,841 | +36%* |
| **Costo estimado** | $0.1161 | $0.1052 | **-9%** |

> *La entrada sube ~640 tokens porque las reglas se incluyen en el prompt. Esto se compensa con el ahorro mucho mayor en salida — los tokens de salida cuestan 5x más que los de entrada en ambos modelos.

> **Anomalía en Opus Tarea 9: Opus ocasionalmente genera una corrección más exhaustiva cuando recibe la instrucción "verificar antes de declarar terminado", produciendo más output en tareas de test+fix. Es una mejora de calidad, no desperdicio.

### Por qué importa más la salida

```
Precios por token (por 1M tokens):
                    Entrada     Salida
  Sonnet 4          $3          $15        ← salida es 5x más cara
  Opus 4            $15         $75        ← salida es 5x más cara

  Reducir salida 60% ahorra más que reducir entrada 60%.
```

## Instalar

```bash
# Opción A: Un proyecto
curl -o CLAUDE.md https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md

# Opción B: Todos los proyectos (reglas globales)
curl -o ~/.claude/rules/token-efficient.md https://raw.githubusercontent.com/israads/token-efficient/main/CLAUDE.md
```

## Verifica Tú Mismo

### Opción 1: Benchmark con API (números exactos)

Requiere API key de Anthropic con créditos.

```bash
git clone https://github.com/israads/token-efficient.git
cd token-efficient/benchmark

# Con Sonnet
ANTHROPIC_API_KEY=sk-ant-... python3 run_benchmark.py

# Con Opus
BENCHMARK_MODEL=claude-opus-4-20250514 ANTHROPIC_API_KEY=sk-ant-... python3 run_benchmark.py
```

El script corre 9 tareas de programación dos veces (sin reglas, luego con reglas) e imprime una tabla comparativa con los tokens exactos de la respuesta de la API.

### Opción 2: Sesiones de Claude Code (suscripción)

Si tienes suscripción Max y no ves conteo de tokens:

```bash
git clone https://github.com/israads/token-efficient.git
cd token-efficient/benchmark
./setup.sh
cd test-project

# Sesión 1: SIN reglas
claude
# Corre las 10 tareas de tasks.md, una por una
# Escribe /context → anota el valor de "Messages"
# Escribe /exit

# Resetea el proyecto
cd .. && ./setup.sh && cd test-project

# Sesión 2: CON reglas
cp ../CLAUDE.md .
claude
# Corre las MISMAS 10 tareas
# Escribe /context → compara el valor de "Messages"
```

**Qué observar**: Aunque `/context` muestre totales similares (mide la ventana actual, no el uso acumulado), notarás:
- Respuestas visiblemente más cortas y directas
- Menos turnos necesarios (Claude actúa en vez de narrar)
- Sin frases de relleno, sin repetir tu pregunta
- Código mostrado como diffs en vez de archivos completos

## Las 30 Reglas — Resumen

| # | Categoría | Regla |
|---|-----------|-------|
| 1 | Core | Leer antes de escribir |
| 2 | Core | Pensar profundo, escribir breve |
| 3 | Core | Editar sobre reescribir (diffs, no archivos completos) |
| 4 | Core | No re-leer archivos que ya están en contexto |
| 5 | Core | Verificar antes de declarar terminado |
| 6 | Core | Solución más simple que funcione |
| 7 | Core | El usuario tiene prioridad sobre todo |
| 8 | Output | Sin relleno ("¡Buena pregunta!", "¡Claro!") |
| 9 | Output | Sin eco (no repetir la petición) |
| 10 | Output | Actuar primero, reportar después |
| 11 | Output | Respuestas proporcionales |
| 12 | Output | Sin advertencias suaves salvo peligro real |
| 13 | Output | Mantenerse en el alcance pedido |
| 14 | Output | Código primero, explicación si no es obvio |
| 15 | Output | Texto plano para respuestas cortas |
| 16 | Contexto | Leer solo secciones necesarias |
| 17 | Contexto | Delegar exploración a subagentes |
| 18 | Contexto | Paralelizar llamadas de herramientas |
| 19 | Contexto | Compactar al 60%, no al 90% |
| 20 | Contexto | No repetir hechos ya establecidos |
| 21 | Contexto | Usar abreviaciones para referencias repetidas |
| 22 | Herramientas | Herramienta más barata primero |
| 23 | Herramientas | CLI sobre MCP |
| 24 | Herramientas | Paths directos sobre búsqueda |
| 25 | Herramientas | Mostrar solo líneas cambiadas |
| 26 | Imágenes | Redimensionar antes de leer |
| 27 | Imágenes | Describir imágenes inmediatamente en texto |
| 28 | Imágenes | Nunca re-leer la misma imagen |
| 29 | Modelo | Modelo más barato para la tarea |
| 30 | Modelo | Menor esfuerzo para consultas simples |

Para explicaciones detalladas de cada regla, ver [RULES.md](RULES.md).

---

## Sources / Fuentes

Compiled from 15+ sources / Compilado de 15+ fuentes:
- [claude-token-efficient (drona23)](https://github.com/drona23/claude-token-efficient) — original 8-rule baseline
- [6 Ways I Cut My Claude Token Usage (Sabrina.dev)](https://www.sabrina.dev/p/6-ways-i-cut-my-claude-token-usage)
- [Optimize Context by 60% (Medium)](https://medium.com/@jpranav97/stop-wasting-tokens-how-to-optimize-claude-code-context-by-60-bfad6fd477e5)
- [HN: Universal Claude.md Discussion](https://news.ycombinator.com/item?id=47581701)
- [18 Token Management Hacks (MindStudio)](https://www.mindstudio.ai/blog/claude-code-token-management-hacks-3)
- [Claude Code Official Docs — Costs](https://code.claude.com/docs/en/costs)
- [Claude Code Official Docs — Best Practices](https://code.claude.com/docs/en/best-practices)

## License

MIT
