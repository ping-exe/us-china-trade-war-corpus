#!/usr/bin/env python3
"""
Sentiment Analysis Pipeline for US-China Trade War Corpus
=========================================================

This script runs two sentiment analysis methods on the corpus:
1. Pysentimiento (RoBERTa-based transformer model)
2. VADER (Lexicon-based sentiment analyzer)

Requirements:
    pip install pandas pysentimiento vaderSentiment

Usage:
    python run_sentiment_analysis.py

Input:
    - ../data/corpus_with_sentiment.csv (or corpus without sentiment scores)

Output:
    - Prints detailed results to terminal
    - Updates CSV with sentiment scores if needed
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*70)
print("SENTIMENT ANALYSIS PIPELINE")
print("US-China Trade War Newspaper Corpus")
print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

# =============================================================================
# LOAD DATA
# =============================================================================
print("\n[1/4] LOADING CORPUS DATA")
print("-"*70)

df = pd.read_csv('../data/corpus_with_sentiment.csv')
print(f"Loaded {len(df)} articles")
print(f"Date range: {df['date_normalized'].min()} to {df['date_normalized'].max()}")
print(f"Columns: {list(df.columns)}")

# =============================================================================
# PYSENTIMIENTO ANALYSIS
# =============================================================================
print("\n" + "="*70)
print("[2/4] PYSENTIMIENTO SENTIMENT ANALYSIS")
print("="*70)
print("\nModel: pysentimiento RoBERTa-based sentiment classifier")
print("Language: English")
print("Task: Sentiment classification (POS/NEG/NEU)")
print("Input: First 512 tokens of article text")
print("-"*70)

# Check if pysentimiento scores already exist
if 'pysentimiento_label' in df.columns and df['pysentimiento_label'].notna().all():
    print("\nPysentimiento scores found in dataset. Displaying results...")
else:
    print("\nRunning pysentimiento analysis...")
    from pysentimiento import create_analyzer
    analyzer = create_analyzer(task="sentiment", lang="en")
    
    pysen_results = []
    for idx, row in df.iterrows():
        text = str(row.get('full_text', ''))[:512] if row.get('full_text') else str(row['headline'])
        if text.strip():
            result = analyzer.predict(text)
            pysen_results.append({
                'pysentimiento_label': result.output,
                'pysentimiento_pos': round(result.probas.get('POS', 0), 4),
                'pysentimiento_neg': round(result.probas.get('NEG', 0), 4),
                'pysentimiento_neu': round(result.probas.get('NEU', 0), 4)
            })
        else:
            pysen_results.append({
                'pysentimiento_label': 'NEU',
                'pysentimiento_pos': 0,
                'pysentimiento_neg': 0,
                'pysentimiento_neu': 1
            })
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{len(df)} articles...")
    
    pysen_df = pd.DataFrame(pysen_results)
    for col in pysen_df.columns:
        df[col] = pysen_df[col].values

# Display Pysentimiento Results
print("\n" + "="*70)
print("PYSENTIMIENTO RESULTS")
print("="*70)

pysen_counts = df['pysentimiento_label'].value_counts()
print("\nSentiment Classification Distribution:")
print("-"*40)
print(f"{'Label':<15} {'N':>8} {'Percentage':>12}")
print("-"*40)
for label in ['NEU', 'NEG', 'POS']:
    count = pysen_counts.get(label, 0)
    pct = count / len(df) * 100
    print(f"{label:<15} {count:>8} {pct:>11.1f}%")
print("-"*40)
print(f"{'TOTAL':<15} {len(df):>8} {'100.0%':>12}")

print("\nProbability Score Statistics:")
print("-"*40)
for col in ['pysentimiento_pos', 'pysentimiento_neg', 'pysentimiento_neu']:
    label = col.replace('pysentimiento_', '').upper()
    print(f"\n{label} Probability:")
    print(f"  Mean:   {df[col].mean():.4f}")
    print(f"  Std:    {df[col].std():.4f}")
    print(f"  Min:    {df[col].min():.4f}")
    print(f"  Max:    {df[col].max():.4f}")

# =============================================================================
# VADER ANALYSIS
# =============================================================================
print("\n" + "="*70)
print("[3/4] VADER SENTIMENT ANALYSIS")
print("="*70)
print("\nModel: VADER (Valence Aware Dictionary and sEntiment Reasoner)")
print("Type: Lexicon and rule-based sentiment analyzer")
print("Reference: Hutto & Gilbert (2014)")
print("Input: First 5000 characters of article text")
print("-"*70)

# Check if VADER scores already exist
if 'vader_compound' in df.columns and df['vader_compound'].notna().all():
    print("\nVADER scores found in dataset. Displaying results...")
else:
    print("\nRunning VADER analysis...")
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    vader = SentimentIntensityAnalyzer()
    
    vader_results = []
    for idx, row in df.iterrows():
        text = str(row.get('full_text', ''))[:5000] if row.get('full_text') else str(row['headline'])
        if text.strip():
            scores = vader.polarity_scores(text)
            vader_results.append({
                'vader_compound': round(scores['compound'], 4),
                'vader_pos': round(scores['pos'], 4),
                'vader_neg': round(scores['neg'], 4),
                'vader_neu': round(scores['neu'], 4)
            })
        else:
            vader_results.append({
                'vader_compound': 0,
                'vader_pos': 0,
                'vader_neg': 0,
                'vader_neu': 1
            })
    
    vader_df = pd.DataFrame(vader_results)
    for col in vader_df.columns:
        df[col] = vader_df[col].values

# Display VADER Results
print("\n" + "="*70)
print("VADER RESULTS")
print("="*70)

print("\nCompound Score Descriptive Statistics:")
print("-"*40)
vader = df['vader_compound']
print(f"{'Statistic':<20} {'Value':>15}")
print("-"*40)
print(f"{'Mean':<20} {vader.mean():>15.4f}")
print(f"{'Standard Deviation':<20} {vader.std():>15.4f}")
print(f"{'Median':<20} {vader.median():>15.4f}")
print(f"{'Minimum':<20} {vader.min():>15.4f}")
print(f"{'Maximum':<20} {vader.max():>15.4f}")
print(f"{'25th Percentile':<20} {vader.quantile(0.25):>15.4f}")
print(f"{'75th Percentile':<20} {vader.quantile(0.75):>15.4f}")

print("\nCategorical Classification (Standard Thresholds):")
print("-"*40)
print("Thresholds: Positive >= 0.05, Negative <= -0.05, Neutral otherwise")
print("-"*40)
positive = (vader >= 0.05).sum()
neutral = ((vader > -0.05) & (vader < 0.05)).sum()
negative = (vader <= -0.05).sum()

print(f"{'Category':<20} {'N':>8} {'Percentage':>12}")
print("-"*40)
print(f"{'Positive (>=0.05)':<20} {positive:>8} {positive/len(df)*100:>11.1f}%")
print(f"{'Neutral':<20} {neutral:>8} {neutral/len(df)*100:>11.1f}%")
print(f"{'Negative (<=-0.05)':<20} {negative:>8} {negative/len(df)*100:>11.1f}%")
print("-"*40)
print(f"{'TOTAL':<20} {len(df):>8} {'100.0%':>12}")

print("\nComponent Score Statistics:")
print("-"*40)
for col in ['vader_pos', 'vader_neg', 'vader_neu']:
    label = col.replace('vader_', '').upper()
    print(f"\n{label} Component:")
    print(f"  Mean:   {df[col].mean():.4f}")
    print(f"  Std:    {df[col].std():.4f}")

# =============================================================================
# CROSS-METHOD COMPARISON
# =============================================================================
print("\n" + "="*70)
print("[4/4] CROSS-METHOD COMPARISON")
print("="*70)

from scipy import stats

# Correlation between VADER compound and Pysentimiento negative probability
r, p = stats.pearsonr(df['vader_compound'], df['pysentimiento_neg'])
print(f"\nPearson Correlation (VADER compound vs Pysentimiento NEG probability):")
print(f"  r = {r:.4f}, p = {p:.6f}")

# Sentiment by period
print("\n" + "-"*70)
print("VADER Mean Sentiment by Policy Period:")
print("-"*70)
print(f"{'Period':<10} {'Mean':>10} {'Std':>10} {'N':>8}")
print("-"*40)
for period in ['P1', 'P2', 'P3', 'P4', 'P5']:
    period_df = df[df['period'] == period]
    if len(period_df) > 0:
        mean = period_df['vader_compound'].mean()
        std = period_df['vader_compound'].std()
        n = len(period_df)
        print(f"{period:<10} {mean:>10.4f} {std:>10.4f} {n:>8}")

# ANOVA
print("\n" + "-"*70)
print("One-Way ANOVA: Sentiment across Policy Periods")
print("-"*70)
groups = [df[df['period'] == p]['vader_compound'].values for p in ['P1', 'P2', 'P3', 'P4', 'P5']]
f_stat, p_val = stats.f_oneway(*groups)
print(f"F-statistic: {f_stat:.4f}")
print(f"p-value: {p_val:.6f}")
print(f"Result: {'Significant' if p_val < 0.05 else 'Not significant'} at α = 0.05")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print(f"\nTotal articles analyzed: {len(df)}")
print(f"Date range: {df['date_normalized'].min()} to {df['date_normalized'].max()}")
print("\nKey Findings:")
print(f"  - Pysentimiento classified {pysen_counts.get('NEU', 0)/len(df)*100:.1f}% as Neutral")
print(f"  - VADER mean compound score: {vader.mean():.4f}")
print(f"  - Cross-method correlation: r = {r:.4f}")
print(f"  - Significant period differences: {'Yes' if p_val < 0.05 else 'No'} (F = {f_stat:.3f}, p = {p_val:.4f})")
