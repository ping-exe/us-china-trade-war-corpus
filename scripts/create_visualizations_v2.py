# US-China Trade War Corpus Visualization Script v2
# Improved versions with refinements

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import os
from scipy import stats

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

# Color palette
period_colors = {
    'P1': '#1f77b4', 
    'P2': '#ff7f0e', 
    'P3': '#2ca02c', 
    'P4': '#d62728', 
    'P5': '#9467bd'
}

os.makedirs('github_release/figures', exist_ok=True)

# =============================================================================
# FIGURE 3 IMPROVED: Add correlation coefficient
# =============================================================================
print("Creating Figure 3 (improved): Method Comparison with correlation...")

fig, ax = plt.subplots(figsize=(10, 8))

# Calculate correlation
r, p = stats.pearsonr(df['vader_compound'], df['pysentimiento_neg'])

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

# Add correlation annotation
ax.annotate(f'r = {r:.3f} (p < .001)' if p < 0.001 else f'r = {r:.3f} (p = {p:.3f})',
            xy=(0.95, 0.95), xycoords='axes fraction',
            ha='right', va='top', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.set_xlabel('VADER Compound Score')
ax.set_ylabel('Pysentimiento Negative Probability')
ax.set_title('Comparison of Sentiment Analysis Methods')
ax.legend(title='Policy Period', loc='upper left', framealpha=0.9)

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig('github_release/figures/fig3_method_comparison_v2.png', dpi=300, bbox_inches='tight')
plt.close()
print("    Saved: fig3_method_comparison_v2.png")


# =============================================================================
# FIGURE 4 IMPROVED: Print sources only (exclude low-n broadcast)
# =============================================================================
print("Creating Figure 4 (improved): Print sources only...")

# Filter to print sources only
print_sources = ['The New York Times', 'The Washington Post', 'Financial Times', 'The Wall Street Journal']
df_print = df[df['source_normalized'].isin(print_sources)]

fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
axes = axes.flatten()

for i, source in enumerate(print_sources):
    ax = axes[i]
    source_df = df_print[df_print['source_normalized'] == source].copy()
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
                s=30,
                label=period if i == 0 else None
            )
    
    # Add rolling mean
    if len(source_df) >= 10:
        source_df_indexed = source_df.set_index('date_normalized')
        rolling = source_df_indexed['vader_compound'].rolling(window='90D', min_periods=3).mean()
        ax.plot(rolling.index, rolling.values, color='black', linewidth=1.5, alpha=0.7)
    
    # Add horizontal line at 0
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3, linewidth=1)
    
    # Title with article count
    n_articles = len(source_df)
    ax.set_title(f'{source}\n(n={n_articles})', fontsize=11)
    ax.set_ylim(-1.1, 1.1)

# Format x-axis
for ax in axes:
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Add legend
legend_labels = ['P1: Pre-Trade War', 'P2: Escalation', 'P3: Phase One', 
                 'P4: Biden Review', 'P5: Tech Decoupling']
legend_handles = [plt.scatter([], [], c=period_colors[p], s=60) for p in ['P1', 'P2', 'P3', 'P4', 'P5']]
fig.legend(legend_handles, legend_labels, loc='center right', 
           title='Policy Periods', bbox_to_anchor=(1.12, 0.5))

fig.text(0.5, 0.02, 'Date', ha='center', fontsize=11)
fig.text(0.02, 0.5, 'VADER Compound Score', va='center', rotation='vertical', fontsize=11)
fig.suptitle('Sentiment Trajectories by News Source (Print Media)', fontsize=13, y=0.98)

plt.tight_layout(rect=[0.03, 0.05, 0.88, 0.95])
plt.savefig('github_release/figures/fig4_small_multiples_print.png', dpi=300, bbox_inches='tight')
plt.close()
print("    Saved: fig4_small_multiples_print.png")


# =============================================================================
# NEW FIGURE 5: Sentiment Distribution by Period (Box Plot)
# =============================================================================
print("Creating Figure 5: Sentiment by Period Box Plot...")

fig, ax = plt.subplots(figsize=(10, 6))

period_order = ['P1', 'P2', 'P3', 'P4', 'P5']
period_labels = ['Pre-Trade War\n(P1)', 'Escalation\n(P2)', 'Phase One\n(P3)', 
                 'Biden Review\n(P4)', 'Tech Decoupling\n(P5)']

# Create box plot with period colors
bp = ax.boxplot([df[df['period'] == p]['vader_compound'] for p in period_order],
                labels=period_labels, patch_artist=True)

for patch, period in zip(bp['boxes'], period_order):
    patch.set_facecolor(period_colors[period])
    patch.set_alpha(0.7)

ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_ylabel('VADER Compound Score')
ax.set_xlabel('Policy Period')
ax.set_title('Sentiment Distribution Across Policy Periods')

# Add sample sizes
for i, period in enumerate(period_order):
    n = len(df[df['period'] == period])
    ax.annotate(f'n={n}', xy=(i+1, -1.15), ha='center', fontsize=9, color='gray')

ax.set_ylim(-1.2, 1.1)

plt.tight_layout()
plt.savefig('github_release/figures/fig5_sentiment_by_period_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("    Saved: fig5_sentiment_by_period_boxplot.png")


# =============================================================================
# Summary Statistics for Interpretation
# =============================================================================
print("\n" + "="*60)
print("KEY STATISTICS FOR INTERPRETATION")
print("="*60)

# Correlation between methods
r, p = stats.pearsonr(df['vader_compound'], df['pysentimiento_neg'])
print(f"\nVADER vs Pysentimiento correlation: r = {r:.3f}, p = {p:.4f}")

# Mean sentiment by period
print("\nMean VADER sentiment by period:")
for period in ['P1', 'P2', 'P3', 'P4', 'P5']:
    mean = df[df['period'] == period]['vader_compound'].mean()
    std = df[df['period'] == period]['vader_compound'].std()
    n = len(df[df['period'] == period])
    print(f"  {period}: M = {mean:.3f}, SD = {std:.3f}, n = {n}")

# ANOVA test
from scipy.stats import f_oneway
groups = [df[df['period'] == p]['vader_compound'] for p in ['P1', 'P2', 'P3', 'P4', 'P5']]
f_stat, p_val = f_oneway(*groups)
print(f"\nOne-way ANOVA (sentiment ~ period): F = {f_stat:.3f}, p = {p_val:.4f}")

print("\n" + "="*60)
print("VISUALIZATION UPDATE COMPLETE")
print("="*60)
