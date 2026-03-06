import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv('data/corpus_metadata_sentiment.csv')

# ============================================
# CHART 1: Article Count by Period (Bar Chart)
# ============================================
period_counts = df['period'].value_counts().sort_index()
fig1 = px.bar(
    x=period_counts.index,
    y=period_counts.values,
    labels={'x': 'Period', 'y': 'Number of Articles'},
    title='Article Coverage by Period',
    color=period_counts.values,
    color_continuous_scale='Blues'
)
fig1.update_layout(showlegend=False, coloraxis_showscale=False)
fig1.write_html('visualizations/articles_by_period.html')
print('Created: articles_by_period.html')

# ============================================
# CHART 2: Article Count by Source (Bar Chart)
# ============================================
source_counts = df['source_normalized'].value_counts()
fig2 = px.bar(
    x=source_counts.values,
    y=source_counts.index,
    orientation='h',
    labels={'x': 'Number of Articles', 'y': 'Source'},
    title='Article Coverage by News Source',
    color=source_counts.values,
    color_continuous_scale='Greens'
)
fig2.update_layout(showlegend=False, coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
fig2.write_html('visualizations/articles_by_source.html')
print('Created: articles_by_source.html')

# ============================================
# CHART 3: VADER Sentiment by Period (Bar Chart)
# ============================================
sentiment_by_period = df.groupby('period')['vader_compound'].mean().reset_index()
fig3 = px.bar(
    sentiment_by_period,
    x='period',
    y='vader_compound',
    labels={'period': 'Period', 'vader_compound': 'Mean VADER Sentiment'},
    title='Average Sentiment by Period (VADER)',
    color='vader_compound',
    color_continuous_scale='RdYlGn',
    range_color=[-0.5, 0.5]
)
fig3.update_layout(coloraxis_showscale=True)
fig3.write_html('visualizations/sentiment_by_period.html')
print('Created: sentiment_by_period.html')

# ============================================
# CHART 4: VADER Sentiment by Source (Bar Chart)
# ============================================
sentiment_by_source = df.groupby('source_normalized')['vader_compound'].mean().reset_index()
sentiment_by_source = sentiment_by_source.sort_values('vader_compound')
fig4 = px.bar(
    sentiment_by_source,
    x='vader_compound',
    y='source_normalized',
    orientation='h',
    labels={'vader_compound': 'Mean VADER Sentiment', 'source_normalized': 'Source'},
    title='Average Sentiment by News Source (VADER)',
    color='vader_compound',
    color_continuous_scale='RdYlGn',
    range_color=[-0.5, 1.0]
)
fig4.write_html('visualizations/sentiment_by_source.html')
print('Created: sentiment_by_source.html')

# ============================================
# CHART 5: Pysentimiento Classification (Pie Chart)
# ============================================
label_counts = df['pysentimiento_label'].value_counts()
fig5 = px.pie(
    values=label_counts.values,
    names=label_counts.index,
    title='Sentiment Classification (Pysentimiento)',
    color=label_counts.index,
    color_discrete_map={'NEU': '#636EFA', 'NEG': '#EF553B', 'POS': '#00CC96'}
)
fig5.write_html('visualizations/sentiment_classification.html')
print('Created: sentiment_classification.html')

# ============================================
# CHART 6: Timeline - Articles Over Time (Line Chart)
# ============================================
df['date_normalized'] = pd.to_datetime(df['date_normalized'])
df['year_month'] = df['date_normalized'].dt.to_period('M').astype(str)
timeline = df.groupby('year_month').size().reset_index(name='count')
fig6 = px.line(
    timeline,
    x='year_month',
    y='count',
    labels={'year_month': 'Month', 'count': 'Number of Articles'},
    title='Article Publication Timeline'
)
fig6.update_xaxes(tickangle=45, dtick=6)
fig6.write_html('visualizations/timeline.html')
print('Created: timeline.html')

print('\nAll visualizations saved to visualizations/ folder!')
print('Open the .html files in your browser to view them.')
