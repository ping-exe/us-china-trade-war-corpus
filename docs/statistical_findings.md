# Key Statistical Findings

## Sentiment Analysis Results

### Overall Corpus Characteristics

The final corpus comprises 569 deduplicated articles spanning February 2017 through February 2026, with coverage concentrated in the trade war escalation period (P2: n = 308, 54.1%). Four print sources—The New York Times (32.0%), The Washington Post (26.0%), Financial Times (23.9%), and The Wall Street Journal (15.6%)—account for 97.5% of the corpus, with broadcast sources contributing minimal coverage (PBS NewsHour: 1.2%, MSNBC: 0.9%, Fox News: 0.4%).

### Temporal Patterns in Media Sentiment

Analysis using VADER sentiment scores reveals significant variation across policy periods (one-way ANOVA: F(4, 564) = 4.830, p < .001). Contrary to expectations that sentiment would be most negative during the trade war escalation, the data reveal a more nuanced pattern. The Pre-Trade War period (P1) exhibited moderately positive sentiment (M = 0.376, SD = 0.768), which declined during Escalation (P2: M = 0.110, SD = 0.808) and reached its nadir during the Phase One period (P3: M = -0.051, SD = 0.790). This finding suggests that media coverage became most negative not during tariff announcements, but during the implementation period coinciding with the COVID-19 pandemic—a period marked by supply chain disruptions, compliance disputes, and broader economic uncertainty.

Sentiment recovered during the Biden Review period (P4: M = 0.294, SD = 0.751) and the Technology Decoupling period (P5: M = 0.384, SD = 0.757), returning to levels comparable to the pre-trade war baseline. This recovery may reflect routinization of trade tensions in media coverage, a shift in framing from economic conflict to technology competition, or simply reduced salience of trade issues relative to other policy concerns.

### Cross-Source Variation

The source-by-period heatmap reveals notable heterogeneity in coverage tone. While all four major print sources followed broadly similar temporal trajectories, the Wall Street Journal exhibited distinctively negative sentiment during the Biden Review period (M = -0.52, n = 4), potentially reflecting editorial perspective on the administration's continuation of Trump-era tariffs. The Financial Times maintained the most neutral stance throughout the study period, consistent with its positioning as an international business publication. Sample sizes for broadcast sources are insufficient for reliable cross-source comparison.

### Methodological Divergence Between Sentiment Measures

A critical methodological finding concerns the divergence between VADER and Pysentimiento sentiment classifications. The Pearson correlation between VADER compound scores and Pysentimiento negative probability was weak and negative (r = -0.203, p < .001), indicating that these methods capture different aspects of text sentiment. Most strikingly, Pysentimiento classified 93.3% of articles as neutral, compared to VADER's more distributed classification (54.5% positive, 36.6% negative, 9.0% neutral using standard thresholds).

This divergence likely reflects differences in training data and model architecture. Pysentimiento, trained primarily on social media text, may be poorly calibrated for the formal register and complex sentence structures characteristic of news journalism. VADER, designed for social media but lexicon-based, appears more sensitive to sentiment-laden vocabulary regardless of text genre. These findings underscore the importance of method validation when applying sentiment analysis tools to domains outside their original training context.

### Limitations

Several limitations warrant acknowledgment. First, the constructed week sampling methodology, while efficient, may miss coverage of specific events falling outside sampled dates. Second, sentiment analysis captures tone rather than substantive framing—an article may be classified as "positive" while presenting trade policy critically, if the language used is not explicitly negative. Third, the low representation of broadcast sources limits generalizability to television news coverage. Finally, the study period extends through early 2026, and patterns in the most recent period may shift as additional policy developments unfold.

### Conclusion

This analysis demonstrates that media sentiment toward US-China trade relations varied significantly across policy periods, with the most negative coverage occurring during the Phase One implementation period rather than during active tariff escalation. The substantial divergence between VADER and Pysentimiento classifications highlights the methodological challenges inherent in automated sentiment analysis of political news content and suggests that researchers should employ multiple methods and validate results against human coding when possible.
