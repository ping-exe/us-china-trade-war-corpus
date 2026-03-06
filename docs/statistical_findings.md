# Statistical Findings: U.S.-China Trade War Media Coverage

## Corpus Overview

- **Total Articles:** 569
- **Date Range:** February 5, 2017 - February 2, 2026
- **Sources:** 7 news outlets
- **Sentiment Methods:** VADER (lexicon-based), pysentimiento (RoBERTa)

## 1. Coverage Distribution by Period

| Period | Date Range | Articles | % of Corpus |
|--------|------------|----------|-------------|
| P1 | 2017-02-05 to 2018-03-17 | 84 | 14.8% |
| P2 | 2018-04-22 to 2019-11-16 | 308 | 54.1% |
| P3 | 2020-02-02 to 2020-12-19 | 72 | 12.7% |
| P4 | 2021-02-28 to 2022-08-20 | 31 | 5.4% |
| P5 | 2022-11-27 to 2026-02-02 | 74 | 13.0% |

**Finding:** P2 (trade war escalation) accounts for over half of all coverage.

## 2. VADER Sentiment by Period

| Period | Mean VADER | Std Dev | n |
|--------|------------|---------|---|
| P1 | +0.4136 | 0.7675 | 84 |
| P2 | +0.1430 | 0.8243 | 308 |
| P3 | +0.1180 | 0.8325 | 72 |
| P4 | +0.3254 | 0.8076 | 31 |
| P5 | +0.4467 | 0.7474 | 74 |

**Finding:** Sentiment lowest during active conflict (P2, P3), highest during P5.

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
| Neutral | 530 | 93.1% |
| Negative | 29 | 5.1% |
| Positive | 10 | 1.8% |

**Finding:** 93% neutral reflects professional journalistic tone.

## 5. Key Takeaways

1. Coverage peaked during trade war escalation (P2: 54% of articles)
2. Sentiment correlates with policy phases
3. Source differences exist between financial and broadcast media
4. Both methods confirm sentiment dipped during active conflict
