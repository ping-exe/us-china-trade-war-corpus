import pandas as pd
import altair as alt

# Load data
df = pd.read_csv('data/corpus_metadata_sentiment.csv')
df['date_normalized'] = pd.to_datetime(df['date_normalized'])

# ============================================
# CHART 1: Multifeature Scatter Plot
# (Based on: altair-viz.github.io/gallery/multifeature_scatter_plot.html)
# ============================================
scatter = alt.Chart(df).mark_circle().encode(
    alt.X('date_normalized:T').scale(zero=False),
    alt.Y('vader_compound:Q').scale(zero=False, padding=1),
    alt.Size('word_count:Q').scale(zero=False),
    color='source_normalized:N'
)

scatter.save('visualizations/scatterplot.html')
scatter.save('visualizations/scatterplot.png', scale_factor=2)
print('Created: scatterplot')

# ============================================
# CHART 2: 2D Histogram Heatmap
# (Based on: altair-viz.github.io/gallery/histogram_heatmap.html)
# ============================================
heatmap = alt.Chart(df).mark_rect().encode(
    alt.X('period:O').bin(maxbins=5),
    alt.Y('source_normalized:N'),
    alt.Color('count():Q').scale(scheme='greenblue')
)

heatmap.save('visualizations/heatmap.html')
heatmap.save('visualizations/heatmap.png', scale_factor=2)
print('Created: heatmap')

print('\nDone!')
