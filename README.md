# US-China Trade War Newspaper Corpus (2017-2026)

A curated corpus of newspaper and broadcast articles covering US-China trade relations, collected from major US publications via Dow Jones Factiva using constructed week sampling methodology.

## Overview

This dataset contains 559 deduplicated news articles covering US-China trade policy from January 2017 through February 2026, spanning five distinct policy periods from the Trump administration through the Biden administration.

## Periodization

| Period | Date Range | Key Events |
|--------|------------|------------|
| P1 | Jan 20, 2017 - Mar 22, 2018 | Pre-trade war; Trump inauguration to Section 301 announcement |
| P2 | Mar 23, 2018 - Jan 15, 2020 | Trade war escalation; tariffs through Phase One signing |
| P3 | Jan 16, 2020 - Jan 20, 2021 | Phase One implementation; COVID-19 disruption |
| P4 | Jan 21, 2021 - Oct 6, 2022 | Biden administration policy review |
| P5 | Oct 7, 2022 - Feb 2, 2026 | Technology decoupling; semiconductor export controls |

## Sources

**Print Publications:**
- The New York Times (n=177, 31.7%)
- The Washington Post (n=145, 25.9%)
- Financial Times (n=136, 24.3%)
- The Wall Street Journal (n=87, 15.6%)

**Broadcast Outlets:**
- PBS NewsHour (n=7, 1.3%)
- MSNBC (n=5, 0.9%)
- Fox News (n=2, 0.4%)

**Note:** CNN was included in the original search query but no CNN articles appear in the final deduplicated corpus.

## Sampling Methodology

This corpus employs constructed week sampling (Riffe, Aust, & Lacy, 1993), a validated method in media research.

**Search Query:** `(tariff OR tariffs OR "trade war" OR "trade policy") AND (China OR Chinese OR Beijing)`

## Data Files

| File | Description | Size |
|------|-------------|------|
| `corpus_with_sentiment.csv` | Full corpus with article text and sentiment scores | ~4 MB |
| `corpus_metadata_sentiment.csv` | Metadata and sentiment scores only (no full text) | ~105 KB |

## Sentiment Analysis

Each article has been analyzed using two complementary approaches:

1. **Pysentimiento** (Transformer-based): Fine-tuned RoBERTa model
2. **VADER** (Lexicon-based): Rule-based sentiment analyzer

## Key Statistics

- **Total Articles:** 559 (P1=83, P2=303, P3=70, P4=31, P5=72)
- **Date Range:** February 5, 2017 - February 2, 2026
- **Mean Word Count:** 516 (SD = 278)
- **VADER Mean Sentiment:** 0.17 (SD = 0.80)

## License

GNU General Public License v3.0 - see [LICENSE](LICENSE) for details.

## Citation

Leung, Thomas. (2026). US-China Trade War Newspaper Corpus (2017-2026). GitHub: https://github.com/thomaspingleung/us-china-trade-war-corpus

## References

- Hutto, C. J., & Gilbert, E. (2014). VADER: A parsimonious rule-based model for sentiment analysis of social media text.
- Pérez, J. M., Giudici, J. C., & Luque, F. (2021). pysentimiento: A Python toolkit for sentiment analysis and social NLP tasks.
- Riffe, D., Aust, C. F., & Lacy, S. R. (1993). The effectiveness of random, consecutive day and constructed week sampling.
