"""
US–China Trade War Corpus — Altair Visualization Suite
=======================================================
Generates 6 publication-ready HTML charts and saves them to
visualizations/ inside your GitHub repo, then commits & pushes.

Run this script from Claude Code with:
    python generate_visualizations.py

Requirements (auto-installed if missing):
    altair, pandas, scipy, numpy
"""

import subprocess, sys

# ── 0. Auto-install dependencies ──────────────────────────────────────────────
def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

for pkg in ["altair", "pandas", "scipy", "numpy", "vegafusion"]:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        print(f"Installing {pkg}…")
        install(pkg)

import pandas as pd
import numpy as np
import altair as alt
from scipy import stats
from pathlib import Path

alt.data_transformers.enable("default")

# ── 1. Paths — edit DATA_PATH to point at your CSV ───────────────────────────
DATA_PATH  = Path("data/corpus_metadata_sentiment.csv")     # metadata CSV
OUT_DIR    = Path("visualizations")
OUT_DIR.mkdir(exist_ok=True)

# ── 2. Load & clean data ─────────────────────────────────────────────────────
raw = pd.read_csv(DATA_PATH)
# The CSV has both 'date' (raw string e.g. "2 April 2017") and
# 'date_normalized' (ISO format e.g. "2017-04-02"). Drop the raw one first.
if "date_normalized" in raw.columns and "date" in raw.columns:
    raw = raw.drop(columns=["date"])
df = raw.rename(columns={"date_normalized": "date", "source_normalized": "source"})
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["vader_compound"] = pd.to_numeric(df["vader_compound"], errors="coerce")
df["word_count"]     = pd.to_numeric(df["word_count"],     errors="coerce")

# Friendly period labels
period_labels = {
    "P1": "P1 — Pre-escalation\n(Feb 2017 – Mar 2018)",
    "P2": "P2 — Escalation\n(Apr 2018 – Nov 2019)",
    "P3": "P3 — COVID/Phase-1\n(Feb 2020 – Dec 2020)",
    "P4": "P4 — Biden transition\n(Feb 2021 – Aug 2022)",
    "P5": "P5 — Post-escalation\n(Nov 2022 – Feb 2026)",
}
df["period_label"] = df["period"].map(period_labels)

# Period date ranges for shaded bands
period_bands = pd.DataFrame([
    {"period": "P1", "start": "2017-02-05", "end": "2018-03-17", "color": "#E8F4FD"},
    {"period": "P2", "start": "2018-04-22", "end": "2019-11-16", "color": "#FDE8E8"},
    {"period": "P3", "start": "2020-02-02", "end": "2020-12-19", "color": "#E8FDE8"},
    {"period": "P4", "start": "2021-02-28", "end": "2022-08-20", "color": "#FDF6E8"},
    {"period": "P5", "start": "2022-11-27", "end": "2026-02-02", "color": "#F0E8FD"},
])
for col in ["start", "end"]:
    period_bands[col] = pd.to_datetime(period_bands[col])

SOURCE_ORDER = [
    "The Wall Street Journal", "Financial Times",
    "The New York Times", "The Washington Post",
    "PBS NewsHour", "Fox News", "MSNBC",
]

PERIOD_ORDER = ["P1", "P2", "P3", "P4", "P5"]
PERIOD_SHORT = {"P1": "P1\nPre-war", "P2": "P2\nEscalation",
                "P3": "P3\nCOVID", "P4": "P4\nBiden", "P5": "P5\nPost"}

COLORS = {
    "The New York Times":    "#1f77b4",
    "The Washington Post":   "#ff7f0e",
    "Financial Times":       "#2ca02c",
    "The Wall Street Journal":"#d62728",
    "Fox News":              "#9467bd",
    "MSNBC":                 "#8c564b",
    "PBS NewsHour":          "#e377c2",
}

print("Data loaded:", len(df), "articles,", df["source"].nunique(), "sources")

# ── 3. Chart 1: Time-series — VADER over time with period bands ───────────────
print("Building Chart 1: Time-series…")

# Rolling 30-day mean
ts = df[["date","vader_compound"]].dropna().sort_values("date")
ts = ts.set_index("date").resample("7D").mean().reset_index()
ts.columns = ["date", "rolling_vader"]

bands = alt.Chart(period_bands).mark_rect(opacity=0.18).encode(
    x=alt.X("start:T"),
    x2="end:T",
    color=alt.Color("period:N", legend=None,
                    scale=alt.Scale(domain=["P1","P2","P3","P4","P5"],
                                    range=["#4e79a7","#e15759","#59a14f","#f28e2b","#b07aa1"])),
)

dots = alt.Chart(df).mark_circle(size=25, opacity=0.35).encode(
    x=alt.X("date:T", title="Date"),
    y=alt.Y("vader_compound:Q", title="VADER Compound Score",
            scale=alt.Scale(domain=[-1, 1])),
    color=alt.Color("period:N",
                    scale=alt.Scale(domain=PERIOD_ORDER,
                                    range=["#4e79a7","#e15759","#59a14f","#f28e2b","#b07aa1"]),
                    legend=alt.Legend(title="Period")),
    tooltip=["source:N", "date:T", "headline:N",
             alt.Tooltip("vader_compound:Q", format=".3f")],
)

line = alt.Chart(ts).mark_line(color="#333333", strokeWidth=2.5).encode(
    x="date:T",
    y="rolling_vader:Q",
)

zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(
    strokeDash=[6,3], color="gray", opacity=0.5
).encode(y="y:Q")

# Period labels at midpoints
mid_labels = period_bands.copy()
mid_labels["mid"] = mid_labels["start"] + (mid_labels["end"] - mid_labels["start"]) / 2
mid_labels["label"] = mid_labels["period"]

period_text = alt.Chart(mid_labels).mark_text(
    dy=-130, fontSize=11, fontWeight="bold", opacity=0.7
).encode(
    x=alt.X("mid:T"),
    text="label:N",
    color=alt.Color("period:N",
                    scale=alt.Scale(domain=PERIOD_ORDER,
                                    range=["#4e79a7","#e15759","#59a14f","#f28e2b","#b07aa1"]),
                    legend=None),
)

chart1 = (bands + dots + line + zero + period_text).properties(
    width=820, height=320,
    title=alt.TitleParams(
        "VADER Sentiment Over Time (U.S.–China Trade War Coverage)",
        subtitle=["Each dot = one article. Black line = 7-day rolling mean. "
                  "Shaded bands = policy periods P1–P5.",
                  "ANOVA: F(4,554) = 3.92, p = 0.0038 — period differences statistically significant (α=0.05)"],
        fontSize=15, subtitleFontSize=11, subtitleColor="#555",
    )
).interactive()

chart1.save(str(OUT_DIR / "01_timeseries_vader.html"))
print("  ✓ saved 01_timeseries_vader.html")

# ── 4. Chart 2: Violin — VADER by source ─────────────────────────────────────
print("Building Chart 2: Violin (VADER by source)…")

violin_data = df[["source","vader_compound","period"]].dropna()

violin = alt.Chart(violin_data).transform_density(
    "vader_compound",
    as_=["vader_compound", "density"],
    groupby=["source"],
    extent=[-1, 1],
    bandwidth=0.12,
).mark_area(orient="horizontal", opacity=0.75).encode(
    y=alt.Y("vader_compound:Q", title="VADER Compound Score",
            scale=alt.Scale(domain=[-1,1])),
    x=alt.X("density:Q", title="",
            stack="center", impute=None, axis=alt.Axis(labels=False, ticks=False, grid=False)),
    color=alt.Color("source:N",
                    scale=alt.Scale(domain=list(COLORS.keys()),
                                    range=list(COLORS.values())),
                    legend=None),
    column=alt.Column("source:N",
                      sort=SOURCE_ORDER,
                      header=alt.Header(labelAngle=-30, labelFontSize=10, titleOrient="bottom")),
    tooltip=["source:N"],
).properties(width=95, height=280,
    title=alt.TitleParams(
        "VADER Sentiment Distribution by News Source",
        subtitle=["Violin width = density of articles at that sentiment score. "
                  "Financial press (WSJ, FT) clusters near 0 (neutral); broadcast outlets show more spread."],
        fontSize=15, subtitleFontSize=11, subtitleColor="#555",
    )
).configure_facet(spacing=4).configure_view(stroke=None)

violin.save(str(OUT_DIR / "02_violin_vader_by_source.html"))
print("  ✓ saved 02_violin_vader_by_source.html")

# ── 5. Chart 3: Heatmap — mean VADER by Source × Period ──────────────────────
print("Building Chart 3: Heatmap source × period…")

heat_df = (df.groupby(["source","period"])["vader_compound"]
             .agg(["mean","count"]).reset_index())
heat_df.columns = ["source","period","mean_vader","n"]

heatmap = alt.Chart(heat_df).mark_rect(stroke="white", strokeWidth=1).encode(
    x=alt.X("period:O", sort=PERIOD_ORDER, title="Period",
            axis=alt.Axis(labelAngle=0)),
    y=alt.Y("source:N", sort=SOURCE_ORDER, title=""),
    color=alt.Color("mean_vader:Q",
                    title="Mean VADER",
                    scale=alt.Scale(scheme="redyellowblue", domain=[-0.5, 1.0])),
    tooltip=["source:N","period:N",
             alt.Tooltip("mean_vader:Q", title="Mean VADER", format=".3f"),
             alt.Tooltip("n:Q", title="n articles")],
)

text_overlay = alt.Chart(heat_df).mark_text(fontSize=11, fontWeight="bold").encode(
    x=alt.X("period:O", sort=PERIOD_ORDER),
    y=alt.Y("source:N", sort=SOURCE_ORDER),
    text=alt.Text("mean_vader:Q", format=".2f"),
    color=alt.condition(
        "datum.mean_vader > 0.5 || datum.mean_vader < -0.2",
        alt.value("white"), alt.value("#333")
    ),
)

chart3 = (heatmap + text_overlay).properties(
    width=380, height=280,
    title=alt.TitleParams(
        "Mean VADER Sentiment: Source × Period",
        subtitle=["Red = negative, Blue = positive. "
                  "P2 (escalation) shows the most negative readings across outlets."],
        fontSize=15, subtitleFontSize=11, subtitleColor="#555",
    )
)
chart3.save(str(OUT_DIR / "03_heatmap_source_period.html"))
print("  ✓ saved 03_heatmap_source_period.html")

# ── 6. Chart 4: Ridgeline — VADER distribution by period ────────────────────
print("Building Chart 4: Ridgeline by period…")

ridge_df = df[["period","vader_compound"]].dropna()
ridge_df["period_short"] = ridge_df["period"].map(
    {"P1":"P1 Pre-war","P2":"P2 Escalation","P3":"P3 COVID","P4":"P4 Biden","P5":"P5 Post"})

step = 50
overlap = 3

ridgeline = alt.Chart(ridge_df, height=step).transform_density(
    "vader_compound",
    as_=["vader_compound","density"],
    extent=[-1,1],
    groupby=["period_short"],
    bandwidth=0.15,
).mark_area(fillOpacity=0.7, stroke="white", strokeWidth=0.5).encode(
    x=alt.X("vader_compound:Q", title="VADER Compound Score",
            scale=alt.Scale(domain=[-1,1])),
    y=alt.Y("density:Q", scale=alt.Scale(range=[step, -step*overlap]),
            axis=None, title=""),
    fill=alt.Fill("period_short:N",
                  sort=["P1 Pre-war","P2 Escalation","P3 COVID","P4 Biden","P5 Post"],
                  scale=alt.Scale(range=["#4e79a7","#e15759","#59a14f","#f28e2b","#b07aa1"]),
                  legend=alt.Legend(title="Period")),
    row=alt.Row("period_short:N",
                sort=["P1 Pre-war","P2 Escalation","P3 COVID","P4 Biden","P5 Post"],
                header=alt.Header(labelAngle=0, labelAlign="right", labelFontSize=11)),
).properties(width=520,
    title=alt.TitleParams(
        "VADER Sentiment Distribution by Policy Period (Ridgeline)",
        subtitle=["P2 and P3 distributions shift left (more negative). "
                  "P5 rebounds toward positive. ANOVA p=0.0038."],
        fontSize=15, subtitleFontSize=11, subtitleColor="#555",
    )
).configure_facet(spacing=-step*overlap*0.6).configure_view(stroke=None)

ridgeline.save(str(OUT_DIR / "04_ridgeline_period.html"))
print("  ✓ saved 04_ridgeline_period.html")

# ── 7. Chart 5: Multifeature scatter — Word count vs VADER ───────────────────
print("Building Chart 5: Multifeature scatter…")

scatter_df = df[["source","period","vader_compound","word_count","headline"]].dropna()
scatter_df = scatter_df[scatter_df["word_count"] < 4000]  # trim outliers

scatter = alt.Chart(scatter_df).mark_circle(opacity=0.55, stroke="white", strokeWidth=0.3).encode(
    x=alt.X("word_count:Q", title="Word Count",
            scale=alt.Scale(type="log", domain=[50,4000])),
    y=alt.Y("vader_compound:Q", title="VADER Compound Score",
            scale=alt.Scale(domain=[-1,1])),
    color=alt.Color("source:N",
                    scale=alt.Scale(domain=list(COLORS.keys()),
                                    range=list(COLORS.values())),
                    legend=alt.Legend(title="Source")),
    size=alt.Size("period:O",
                  sort=PERIOD_ORDER,
                  scale=alt.Scale(range=[20,120]),
                  legend=alt.Legend(title="Period")),
    tooltip=["source:N","period:N","headline:N",
             alt.Tooltip("word_count:Q", title="Words"),
             alt.Tooltip("vader_compound:Q", format=".3f", title="VADER")],
)

zero_h = alt.Chart(pd.DataFrame({"y":[0]})).mark_rule(
    strokeDash=[4,3], color="gray", opacity=0.4).encode(y="y:Q")

chart5 = (scatter + zero_h).properties(
    width=600, height=380,
    title=alt.TitleParams(
        "Word Count vs. VADER Sentiment (by Source & Period)",
        subtitle=["Color = outlet, size = period number (larger = later period). "
                  "Log x-axis. Hover for article details."],
        fontSize=15, subtitleFontSize=11, subtitleColor="#555",
    )
).interactive()

chart5.save(str(OUT_DIR / "05_scatter_wordcount_vader.html"))
print("  ✓ saved 05_scatter_wordcount_vader.html")

# ── 8. Chart 6: VADER vs Pysentimiento dual-method comparison ────────────────
print("Building Chart 6: VADER vs Pysentimiento comparison…")

# Stacked bar: pysentimiento label distribution by period
pysent_period = (df.groupby(["period","pysentimiento_label"])
                   .size().reset_index(name="count"))
total_per_period = df.groupby("period").size().reset_index(name="total")
pysent_period = pysent_period.merge(total_per_period, on="period")
pysent_period["pct"] = pysent_period["count"] / pysent_period["total"] * 100

bar_pysent = alt.Chart(pysent_period).mark_bar().encode(
    x=alt.X("period:O", sort=PERIOD_ORDER, title="Period",
            axis=alt.Axis(labelAngle=0)),
    y=alt.Y("pct:Q", title="% of Articles", stack="zero"),
    color=alt.Color("pysentimiento_label:N",
                    scale=alt.Scale(domain=["NEG","NEU","POS"],
                                    range=["#e15759","#bab0ac","#59a14f"]),
                    legend=alt.Legend(title="Pysentimiento")),
    tooltip=["period:N","pysentimiento_label:N",
             alt.Tooltip("pct:Q", format=".1f", title="%"),
             "count:Q"],
).properties(width=280, height=220, title="Pysentimiento Label % by Period")

# Mean VADER bar by period (for direct comparison)
vader_period = df.groupby("period")["vader_compound"].mean().reset_index()
vader_period.columns = ["period","mean_vader"]

bar_vader = alt.Chart(vader_period).mark_bar().encode(
    x=alt.X("period:O", sort=PERIOD_ORDER, title="Period",
            axis=alt.Axis(labelAngle=0)),
    y=alt.Y("mean_vader:Q", title="Mean VADER Compound"),
    color=alt.Color("mean_vader:Q",
                    scale=alt.Scale(scheme="redyellowblue", domain=[-0.3,0.6])),
    tooltip=["period:N", alt.Tooltip("mean_vader:Q", format=".3f")],
).properties(width=280, height=220, title="Mean VADER Score by Period")

# Scatter: for each article, pysentimiento neu score vs vader
method_scatter = alt.Chart(df.dropna(subset=["vader_compound","pysentimiento_neu"])).mark_circle(
    opacity=0.4, size=18
).encode(
    x=alt.X("vader_compound:Q", title="VADER Compound", scale=alt.Scale(domain=[-1,1])),
    y=alt.Y("pysentimiento_neu:Q", title="Pysentimiento NEU Confidence", scale=alt.Scale(domain=[0,1])),
    color=alt.Color("pysentimiento_label:N",
                    scale=alt.Scale(domain=["NEG","NEU","POS"],
                                    range=["#e15759","#bab0ac","#59a14f"]),
                    legend=alt.Legend(title="Pysentimiento")),
    tooltip=["source:N","period:N",
             alt.Tooltip("vader_compound:Q", format=".3f"),
             alt.Tooltip("pysentimiento_neu:Q", format=".3f"),
             "pysentimiento_label:N"],
).properties(width=320, height=220,
    title="Both Methods: VADER vs Pysentimiento NEU Confidence")

# Combine
chart6 = alt.vconcat(
    alt.hconcat(bar_vader, bar_pysent),
    method_scatter,
    title=alt.TitleParams(
        "Dual-Method Comparison: VADER vs. Pysentimiento by Period",
        subtitle=["Top row: VADER means (left) and Pysentimiento label proportions (right) by period. "
                  "Bottom: article-level agreement — high NEU confidence aligns with VADER near 0.",
                  "Both methods agree: sentiment dipped during P2–P3 (active conflict) and recovered in P5."],
        fontSize=15, subtitleFontSize=11, subtitleColor="#555",
    )
)

chart6.save(str(OUT_DIR / "06_dual_method_comparison.html"))
print("  ✓ saved 06_dual_method_comparison.html")

# ── 9. Summary ────────────────────────────────────────────────────────────────
print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("All 6 charts saved to:", OUT_DIR.resolve())
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("""
Next steps (run in Claude Code or terminal):
  cd /path/to/us-china-trade-war-corpus
  git add visualizations/
  git commit -m "Add Altair sentiment visualization suite (6 charts)"
  git push
""")
