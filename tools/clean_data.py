"""
clean_data.py
Reads the raw complaints CSV, keeps selected columns, and saves a balanced
random sample of ~500 rows (split evenly across the three companies) to
data/complaints_clean.csv. The original file is never modified.
"""

import pandas as pd
import pathlib

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR   = pathlib.Path(__file__).resolve().parent.parent
INPUT_CSV  = BASE_DIR / "data" / "complaints-2026-11-07_22_17.csv"
OUTPUT_CSV = BASE_DIR / "data" / "complaints_clean.csv"

# ── Columns to keep ────────────────────────────────────────────────────────
KEEP_COLS = [
    "Date received",
    "Company",
    "Sub-product",
    "Issue",
    "Sub-issue",
    "State",
    "Company response to consumer",
    "Timely response?",
]

# ── Load ───────────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT_CSV, low_memory=False)

# ── Select columns ─────────────────────────────────────────────────────────
df = df[KEEP_COLS]

# ── Balanced sample: ~500 rows split evenly across companies ───────────────
TOTAL_ROWS     = 500
companies      = df["Company"].unique()
rows_per_group = TOTAL_ROWS // len(companies)   # floor-divide; ~166 each

pieces = [
    group.sample(n=min(rows_per_group, len(group)), random_state=42)
    for _, group in df.groupby("Company")
]
sampled = pd.concat(pieces).reset_index(drop=True)

# ── Save ───────────────────────────────────────────────────────────────────
sampled.to_csv(OUTPUT_CSV, index=False)

print(f"Saved {len(sampled)} rows to {OUTPUT_CSV}")
print(sampled["Company"].value_counts().to_string())
