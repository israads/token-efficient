# Benchmark Results — Sonnet 4

Generated on 2026-04-08 01:09 UTC using `claude-sonnet-4-20250514`.

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

| Metric | Without | With | Change |
|--------|--------:|-----:|-------:|
| **Output tokens** | **8,949** | **3,642** | **+59%** |
| Input tokens | 26,805 | 37,260 | +39% |
| **Estimated cost** | **$0.2147** | **$0.1664** | **+22%** |

### By Category

| Category | Without | With | Saved |
|----------|--------:|-----:|------:|
| bugfix | 388 | 139 | 64% |
| explain | 855 | 303 | 65% |
| feature | 2,858 | 329 | 88% |
| lookup | 379 | 107 | 72% |
| refactor | 2,533 | 1,509 | 40% |
| review | 447 | 161 | 64% |
| search | 470 | 295 | 37% |
| test | 1,019 | 799 | 22% |
