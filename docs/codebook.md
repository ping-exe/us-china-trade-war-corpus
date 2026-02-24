# Codebook: US-China Trade War Corpus

## Variable Definitions

| Variable | Description |
|----------|-------------|
| article_id | Unique identifier (format: P[period]_[source]_[number]) |
| source_normalized | Standardized publication name |
| date_normalized | Publication date (YYYY-MM-DD) |
| headline | Article headline |
| byline | Author name(s) |
| section | Publication section |
| word_count | Article word count |
| period | Policy period (P1-P5) |
| full_text | Complete article text |
| pysentimiento_label | Sentiment label (POS/NEG/NEU) |
| pysentimiento_pos | Positive probability (0-1) |
| pysentimiento_neg | Negative probability (0-1) |
| pysentimiento_neu | Neutral probability (0-1) |
| vader_compound | VADER compound score (-1 to +1) |
| vader_pos | VADER positive proportion |
| vader_neg | VADER negative proportion |
| vader_neu | VADER neutral proportion |

## Period Definitions

| Period | Date Range | Duration | Key Events |
|--------|------------|----------|------------|
| P1 | Jan 20, 2017 - Mar 22, 2018 | 14 months | Trump inauguration; Section 301 investigation |
| P2 | Mar 23, 2018 - Jan 15, 2020 | 22 months | Tariff escalation; multiple rounds |
| P3 | Jan 16, 2020 - Jan 20, 2021 | 12 months | Phase One deal; COVID-19 pandemic |
| P4 | Jan 21, 2021 - Oct 6, 2022 | 21 months | Biden policy review; tariff continuity |
| P5 | Oct 7, 2022 - Feb 2, 2026 | 40 months | Semiconductor controls; tech decoupling |

## VADER Compound Score Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| >= 0.05 | Positive |
| > -0.05 and < 0.05 | Neutral |
| <= -0.05 | Negative |

## Source Abbreviations

| Code | Full Name |
|------|-----------|
| NYT | The New York Times |
| WP | The Washington Post |
| WSJ | The Wall Street Journal |
| FT | Financial Times |
| FOX | Fox News |
| PBS | PBS NewsHour |
| MSNBC | MSNBC |
