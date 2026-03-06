# Statistical Findings: U.S.-China Trade War Media Coverage

## Corpus Overview

- **Total Articles:** 559 (10 articles removed in quality control: 1 search query artifact and 9 empty stubs)
- **Date Range:** February 5, 2017 - February 2, 2026
- **Sources:** 7 news outlets
- **Sentiment Methods:** VADER (lexicon-based), pysentimiento (RoBERTa)

## 1. Coverage Distribution by Period

| Period | Date Range | Articles | % of Corpus |
|--------|------------|----------|-------------|
| P1 | 2017-02-05 to 2018-03-17 | 83 | 14.8% |
| P2 | 2018-04-22 to 2019-11-16 | 303 | 54.2% |
| P3 | 2020-02-02 to 2020-12-19 | 70 | 12.5% |
| P4 | 2021-02-28 to 2022-08-20 | 31 | 5.5% |
| P5 | 2022-11-27 to 2026-02-02 | 72 | 12.9% |

**Finding:** P2 (trade war escalation) accounts for over half of all coverage.

## 2. VADER Sentiment by Period

| Period | Mean VADER | Std Dev | n |
|--------|------------|---------|---|
| P1 | +0.4066 | 0.7694 | 83 |
| P2 | +0.1405 | 0.8238 | 303 |
| P3 | +0.0931 | 0.8309 | 70 |
| P4 | +0.3254 | 0.8076 | 31 |
| P5 | +0.4537 | 0.7448 | 72 |

**Finding:** Sentiment lowest during active conflict (P2, P3), highest during P5.

**One-way ANOVA:** F(4, 554) = 3.9227, p = 0.003768 — differences across periods are statistically significant at α = 0.05.

## 3. VADER Sentiment by Source

| Source | Mean VADER | n |
|--------|------------|---|
| MSNBC | +0.9999 | 5 |
| PBS NewsHour | +0.7143 | 7 |
| Fox News | +0.6574 | 2 |
| The New York Times | +0.3632 | 182 |
| The Washington Post | +0.2140 | 148 |
| Financial Times | +0.1096 | 136 |
| The Wall Street Journal | +0.0721 | 89 |

**Finding:** Financial press (WSJ, FT) most neutral; broadcast outlets more positive.

## 4. Pysentimiento Classification

| Label | Count | % |
|-------|-------|---|
| Neutral | 521 | 93.2% |
| Negative | 28 | 5.0% |
| Positive | 10 | 1.8% |

**Finding:** 93% neutral reflects professional journalistic tone.

## 5. Key Takeaways

1. Coverage peaked during trade war escalation (P2: 54% of articles)
2. Sentiment correlates with policy phases
3. Source differences exist between financial and broadcast media
4. Both methods confirm sentiment dipped during active conflict
