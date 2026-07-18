#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lesson 1: Descriptive Statistics - Understanding Risk
=====================================================
Reads: index.csv (16 A-share indices, 2000-2018 daily returns)
Output: output/descriptive_stats.csv (risk ranking table)
Every line is commented. Read top to bottom.
"""

import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent.parent
DATA = BASE / '交接文件/9-11研究/代码'
OUT = BASE / 'output'
OUT.mkdir(exist_ok=True)

# ===== STEP 1: Load the master data file =====
# index.csv: GBK-encoded, 3 header rows, 16 columns of daily return %
raw = pd.read_csv(DATA / 'index.csv', encoding='gbk')
codes = list(raw.columns[1:])
# Row 0 = Chinese names (garbled in terminal, fine in Excel)
# Row 2 = all labels are '涨跌幅' (daily change %)
df = raw.iloc[3:-2].copy()  # Skip 3 header rows + 2 footer rows (empty + Choice data source)
df.columns = ['date'] + codes
df['date'] = pd.to_datetime(df['date'])
for c in codes:
    df[c] = pd.to_numeric(df[c], errors='coerce') / 100.0

total_days = len(df)
print(f'Data: {total_days} trading days, {len(codes)} indices')
print(f'Range: {df.date.min().date()} to {df.date.max().date()}')

# ===== STEP 2: Build results table =====
results = pd.DataFrame(index=pd.Index(codes, name='code'))

# Metric A: Annualized return (compound 245 days, then average)
# Metric B: Annualized return (average daily first, then compound)
for code in codes:
    d = df[code].dropna()
    # Annual return: compound 245 trading-day windows
    c245 = (d + 1).rolling(245).apply(np.prod, raw=True) - 1
    results.loc[code, 'ann_return'] = c245.mean()
    results.loc[code, 'ann_return_alt'] = (d.mean() + 1)**245 - 1
    # Monthly return
    c20 = (d + 1).rolling(20).apply(np.prod, raw=True) - 1
    results.loc[code, 'mon_return'] = c20.mean()

# Annualized volatility = daily_std * sqrt(245)
for code in codes:
    d = df[code].dropna()
    results.loc[code, 'ann_vol'] = d.std() * np.sqrt(245)

# Max Drawdown: worst peak-to-trough loss
for code in codes:
    d = df[code].dropna()
    cum = (d + 1).cumprod()
    peak = cum.expanding().max()
    drawdown = (cum - peak) / peak
    results.loc[code, 'max_dd'] = drawdown.min()

# VaR: sort returns, pick the Nth percentile worst
for code in codes:
    d = df[code].dropna()
    sd = sorted(d, reverse=True)
    n = len(sd)
    results.loc[code, 'VaR_95'] = sd[round(n*0.95)]
    results.loc[code, 'VaR_99'] = sd[round(n*0.99)]

# Average net value
for code in codes:
    d = df[code].dropna()
    results.loc[code, 'avg_nv'] = (d + 1).cumprod().mean()

# ===== STEP 3: Compute return/risk ratio =====
results['ret_per_vol'] = results['ann_return'] / results['ann_vol']

# ===== STEP 4: Display =====
disp = results[['ann_return','ann_vol','max_dd','VaR_95','VaR_99','ret_per_vol']].copy()
disp.columns = ['Ann.Return','Ann.Vol','MaxDD','VaR95','VaR99','Ret/Vol']
print()
print(disp.to_string(float_format=lambda x: f'{x:.4f}'))

print()
top = results.nlargest(5, 'ret_per_vol')
print('Top 5 by Return/Volatility:')
for idx, row in top.iterrows():
    print(f'  {idx:12s}  ret={row["ann_return"]:.4f}  vol={row["ann_vol"]:.4f}  ratio={row["ret_per_vol"]:.4f}')

print()
print('HOW TO READ:')
print('  Ann.Return = average annual return (higher = better)')
print('  Ann.Vol    = how much it bounces (higher = rougher ride)')
print('  MaxDD      = worst peak-to-trough loss ever')
print('  VaR99      = on 99% of days, loss is LESS than this')
print('  Ret/Vol    = return per unit of risk (>0.5 good, >1.0 excellent)')

results.to_csv(OUT / 'descriptive_stats.csv', encoding='utf-8-sig')
print('')
print('Saved: ' + str(OUT / 'descriptive_stats.csv'))
