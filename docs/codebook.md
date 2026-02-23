# Codebook: US-China Trade War Corpus

## Sentiment Coding Schema

### Pysentimiento (BERT-based)
| Label | Definition |
|-------|------------|
| NEG | Negative sentiment |
| NEU | Neutral sentiment |
| POS | Positive sentiment |

### VADER Compound Score Interpretation
| Score Range | Interpretation |
|-------------|----------------|
| >= 0.05 | Positive |
| > -0.05 and < 0.05 | Neutral |
| <= -0.05 | Negative |

## Period Definitions

| Period | Date Range | Duration | Key Events |
|--------|------------|----------|------------|
| P1 | Jan 20, 2017 - Mar 22, 2018 | 14 months | Trump inauguration; Section 301 investigation |
| P2 | Mar 23, 2018 - Jan 15, 2020 | 22 months | Tariff escalation; multiple rounds |
| P3 | Jan 16, 2020 - Jan 20, 2021 | 12 months | Phase One deal; COVID-19 pandemic |
| P4 | Jan 21, 2021 - Oct 6, 2022 | 21 months | Biden policy review; tariff continuity |
| P5 | Oct 7, 2022 - Dec 31, 2025 | 39 months | Semiconductor controls; tech decoupling |

## Source Abbreviations

| Code | Full Name |
|------|-----------|
| NYT | The New York Times |
| WP | The Washington Post |
| WSJ | The Wall Street Journal |
| FT | Financial Times |
| FOX | Fox News |
| PBS | PBS NewsHour |

## Article ID Format

Format: P[period]_[source]_[number]

Example: P2_NYT_0045 = Period 2, New York Times, article 45
