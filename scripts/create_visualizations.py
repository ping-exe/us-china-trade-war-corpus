# US-China Trade War Corpus Visualization Script
# Generates 4 figures for the analysis

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import os

# Load data
df = pd.read_csv('github_release/data/corpus_with_sentiment.csv')
df['date_normalized'] = pd.to_datetime(df['date_normalized'])
df = df.sort_values('date_normalized')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Define period boundaries for annotations
period_boundaries = [
    ('2018-03-22', 'Section 301'),
    ('2020-01-15', 'Phase One'),
    ('2021-01-20', 'Biden Inaug.'),
    ('2022-10-07', 'Chip Controls')
]

# Color palette
period_colors = {
    'P1': '#1f77b4', 
    'P2': '#ff7f0e', 
    'P3': '#2ca02c', 
    'P4': '#d62728', 
    'P5': '#9467bd'
}

# Create figures directory
os.makedirs('github_release/figures', exist_ok=True)

# =============================================================================
# FIGURE 1: Sentiment Time Series with Policy Period Annotations
# =============================================================================
print("Creating Figure 1: Sentiment Time Series...")

fig, ax = plt.subplots(figsize=(12, 5))

# Calculate 60-day rolling mean
df_sorted = df.sort_values('date_normalized').copy()
df_sorted = df_sorted.set_index('date_normalized')
rolling = df_sorted['vader_compound'].rolling(window='60D', min_periods=5).mean()

# Plot rolling average
ax.plot(rolling.index, rolling.values, color='#2c3e50', linewidth=2, label='60-day rolling mean')

# Add individual points with low alpha
ax.scatter(df['date_normalized'], df['vader_compound'], alpha=0.15, s=15, color='#3498db', label='Individual articles')

# Add period boundary lines and annotations
for date_str, label in period_boundaries:
    date = pd.to_datetime(date_str)
    ax.axvline(x=date, color='#e74c3c', linestyle='--', alpha=0.7, linewidth=1)
    ax.annotate(label, xy=(date, 1.0), xytext=(5, -5),
                textcoords='offset points', fontsize=8, color='#e74c3c',
                rotation=90, va='top', ha='left')

# Add horizontal line at 0
ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3, linewidth=1)

# Add period background shading
period_ranges = [
    ('2017-01-20', '2018-03-22', 'P1'),
    ('2018-03-23', '2020-01-15', 'P2'),
    ('2020-01-16', '2021-01-20', 'P3'),
    ('2021-01-21', '2022-10-06', 'P4'),
    ('2022-10-07', '2025-12-31', 'P5')
]

for start, end, period in period_ranges:
    ax.axvspan(pd.to_datetime(start), pd.to_datetime(end), 
               alpha=0.1, color=period_colors[period])

ax.set_xlabel('Date')
ax.set_ylabel('VADER Compound Score')
ax.set_title('Media Sentiment Toward US-China Trade Relations (2017-2025)')
ax.set_ylim(-1.1, 1.1)
ax.legend(loc='lower right', framealpha=0.9)

# Format x-axis
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.tight_layout()
plt.savefig('github_release/figures/fig1_sentiment_timeseries.png', dpi=300, bbox_inches='tight')
plt.savefig('github_release/figures/fig1_sentiment_timeseries.pdf', bbox_inches='tight')
plt.close()
print("    Saved: fig1_sentiment_timeseries.png/pdf")


# =============================================================================
# FIGURE 2: Source x Period Heatmap
# =============================================================================
print("Creating Figure 2: Source x Period Heatmap...")

# Calculate mean sentiment and counts
pivot_sentiment = df.pivot_table(
    values='vader_compound', 
    index='source_normalized', 
    columns='period', 
    aggfunc='mean'
)

pivot_counts = df.pivot_table(
    values='vader_compound', 
    index='source_normalized', 
    columns='period', 
    aggfunc='count'
)

# Order sources by total coverage
source_order = df['source_normalized'].value_counts().index.tolist()
pivot_sentiment = pivot_sentiment.reindex(source_order)
pivot_counts = pivot_counts.reindex(source_order)

# Create annotation labels with mean and n
annot_labels = pivot_sentiment.copy().astype(str)
for idx in pivot_sentiment.index:
    for col in pivot_sentiment.columns:
        mean_val = pivot_sentiment.loc[idx, col]
        count_val = pivot_counts.loc[idx, col]
        if pd.isna(mean_val):
            annot_labels.loc[idx, col] = ''
        else:
            annot_labels.loc[idx, col] = f'{mean_val:.2f}\n(n={int(count_val)})'

fig, ax = plt.subplots(figsize=(10, 7))

# Create heatmap
sns.heatmap(
    pivot_sentiment, 
    annot=annot_labels, 
    fmt='', 
    cmap='RdBu', 
    center=0, 
    ax=ax,
    cbar_kws={'label': 'Mean VADER Compound Score'},
    linewidths=0.5,
    linecolor='white',
    vmin=-0.5,
    vmax=0.5
)

ax.set_xlabel('Policy Period')
ax.set_ylabel('News Source')
ax.set_title('Mean Sentiment by Source and Policy Period')

# Add period labels
period_labels = ['Pre-Trade War\n(P1)', 'Escalation\n(P2)', 'Phase One\n(P3)', 
                 'Biden Review\n(P4)', 'Tech Decoupling\n(P5)']
ax.set_xticklabels(period_labels, rotation=0, ha='center')

plt.tight_layout()
plt.savefig('github_release/figures/fig2_source_period_heatmap.png', dpi=300, bbox_inches='tight')
plt.savefig('github_release/figures/fig2_source_period_heatmap.pdf', bbox_inches='tight')
plt.close()
print("    Saved: fig2_source_period_heatmap.png/pdf")


# =============================================================================
# FIGURE 3: VADER vs Pysentimiento Scatter Plot
# =============================================================================
print("Creating Figure 3: Dual-Method Sentiment Comparison...")

fig, ax = plt.subplots(figsize=(10, 8))

# Create scatter plot colored by period
for period in ['P1', 'P2', 'P3', 'P4', 'P5']:
    mask = df['period'] == period
    ax.scatter(
        df.loc[mask, 'vader_compound'], 
        df.loc[mask, 'pysentimiento_neg'],
        c=period_colors[period],
        label=period,
        alpha=0.6,
        s=40,
        edgecolors='white',
        linewidth=0.5
    )

# Add quadrant lines
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5, linewidth=1)

# Add quadrant labels
ax.annotate('VADER Negative\nPysentimiento Negative', 
            xy=(-0.7, 0.75), fontsize=9, color='gray', ha='center')
ax.annotate('VADER Positive\nPysentimiento Negative', 
            xy=(0.7, 0.75), fontsize=9, color='gray', ha='center')
ax.annotate('VADER Negative\nPysentimiento Neutral/Positive', 
            xy=(-0.7, 0.25), fontsize=9, color='gray', ha='center')
ax.annotate('VADER Positive\nPysentimiento Neutral/Positive', 
            xy=(0.7, 0.25), fontsize=9, color='gray', ha='center')

ax.set_xlabel('VADER Compound Score')
ax.set_ylabel('Pysentimiento Negative Probability')
ax.set_title('Comparison of Sentiment Analysis Methods')
ax.legend(title='Policy Period', loc='upper left', framealpha=0.9)

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig('github_release/figures/fig3_method_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('github_release/figures/fig3_method_comparison.pdf', bbox_inches='tight')
plt.close()
print("    Saved: fig3_method_comparison.png/pdf")


# =============================================================================
# FIGURE 4: Small Multiples - Sentiment by Source Over Time
# =============================================================================
print("Creating Figure 4: Small Multiples by Source...")

# Get sources ordered by article count
sources = df['source_normalized'].value_counts().index.tolist()

# Create 2x4 grid (7 sources + 1 for legend)
fig, axes = plt.subplots(2, 4, figsize=(14, 7), sharex=True, sharey=True)
axes = axes.flatten()

for i, source in enumerate(sources):
    ax = axes[i]
    source_df = df[df['source_normalized'] == source].copy()
    source_df = source_df.sort_values('date_normalized')
    
    # Plot individual points
    for period in ['P1', 'P2', 'P3', 'P4', 'P5']:
        mask = source_df['period'] == period
        if mask.sum() > 0:
            ax.scatter(
                source_df.loc[mask, 'date_normalized'], 
                source_df.loc[mask, 'vader_compound'],
                c=period_colors[period],
                alpha=0.6,
                s=20
            )
    
    # Add rolling mean if enough data
    if len(source_df) >= 10:
        source_df_indexed = source_df.set_index('date_normalized')
        rolling = source_df_indexed['vader_compound'].rolling(window='90D', min_periods=3).mean()
        ax.plot(rolling.index, rolling.values, color='black', linewidth=1.5, alpha=0.7)
    
    # Add horizontal line at 0
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3, linewidth=1)
    
    # Title with article count
    n_articles = len(source_df)
    ax.set_title(f'{source}\n(n={n_articles})', fontsize=10)
    
    ax.set_ylim(-1.1, 1.1)

# Use the last subplot for legend
ax_legend = axes[7]
ax_legend.axis('off')

# Create legend
legend_labels = [
    'P1: Pre-Trade War', 
    'P2: Escalation', 
    'P3: Phase One',
    'P4: Biden Review', 
    'P5: Tech Decoupling'
]

for period, label in zip(['P1', 'P2', 'P3', 'P4', 'P5'], legend_labels):
    ax_legend.scatter([], [], c=period_colors[period], label=label, s=60)

ax_legend.legend(loc='center', fontsize=10, frameon=True, title='Policy Periods')

# Format x-axis for all subplots
for ax in axes[:7]:
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Add common labels
fig.text(0.5, 0.02, 'Date', ha='center', fontsize=11)
fig.text(0.02, 0.5, 'VADER Compound Score', va='center', rotation='vertical', fontsize=11)
fig.suptitle('Sentiment Trajectories by News Source', fontsize=13, y=0.98)

plt.tight_layout(rect=[0.03, 0.05, 1, 0.95])
plt.savefig('github_release/figures/fig4_small_multiples.png', dpi=300, bbox_inches='tight')
plt.savefig('github_release/figures/fig4_small_multiples.pdf', bbox_inches='tight')
plt.close()
print("    Saved: fig4_small_multiples.png/pdf")


# =============================================================================
# Summary
# =============================================================================
print("\n" + "="*60)
print("VISUALIZATION COMPLETE")
print("="*60)
print("\nGenerated figures:")
print("  1. fig1_sentiment_timeseries - Temporal evolution with policy annotations")
print("  2. fig2_source_period_heatmap - Cross-source sentiment comparison")
print("  3. fig3_method_comparison - VADER vs Pysentimiento validation")
print("  4. fig4_small_multiples - Source-level sentiment trajectories")
print("\nAll figures saved to: github_release/figures/")
print("Formats: PNG (300 dpi) and PDF")
