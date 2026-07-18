#!/usr/bin/env python3
"""Lesson 2: PE Quantile Strategy — with REAL PE data from 深证红利"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

BASE = Path(__file__).parent.parent
DATA = BASE / "交接文件/9-11研究/代码/PE"
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

# Load REAL PE data (output from original notebook, contains actual PE column)
raw = pd.read_csv(DATA / "深证红利PE策略.csv", encoding="gbk")
print(f"Columns: {list(raw.columns)}")

# Extract: date, close price, PE, return
dates = raw.iloc[:, 0]  # first col = date
cp = pd.to_numeric(raw["cp"], errors="coerce")  # close price
pe = pd.to_numeric(raw["PE"], errors="coerce")  # real PE from Wind
ret = pd.to_numeric(raw["re"], errors="coerce")  # weekly return

print(f"Real PE range: {pe.min():.1f} to {pe.max():.1f}")
print(f"Data: {len(pe)} weeks, {dates.iloc[0]} to {dates.iloc[-1]}")

# ==== CORE ALGORITHM ====
pe_vals = pe.values
n = len(pe_vals)
WARMUP = 96

pos = [0]
states = []

for i in range(WARMUP, n):
    cur = np.mean(pe_vals[i-5:i])          # 5-week smooth
    hist = sorted(pe_vals[0:(i-1)])        # all past PE
    q20 = hist[min(int(i*0.20), len(hist)-1)]
    q30 = hist[min(int(i*0.30), len(hist)-1)]
    q60 = hist[min(int(i*0.60), len(hist)-1)]
    q80 = hist[min(int(i*0.80), len(hist)-1)]

    if cur <= q20:
        pos.append(1); states.append("CHEAP")
    elif cur <= q30:
        if pos[-1] >= 0.5: pos.append(1)
        else: pos.append(0.5)
        states.append("VALUE")
    elif cur < q60:
        pos.append(pos[-1]); states.append("NORMAL")
    elif cur < q80:
        if pos[-1] == 1: pos.append(0.5)
        elif pos[-1] == 0.5: pos.append(0)
        else: pos.append(0)
        states.append("EXPENSIVE")
    else:
        pos.append(0); states.append("BUBBLE")

pos = pos[1:]

# ==== Performance ====
r = ret.values[WARMUP:]
nv = [1.0]
for i in range(len(pos)):
    rr = 0.035/52 if pos[i]==0 else pos[i]*r[i]
    nv.append(nv[-1]*(1+rr))
nv = np.array(nv)

bh = [1.0]
for rr in r: bh.append(bh[-1]*(1+rr))
bh = np.array(bh)

# ==== Results ====
w = len(pos)
full = sum(1 for p in pos if p==1)
half = sum(1 for p in pos if p==0.5)
empty = sum(1 for p in pos if p==0)
print(f"Weeks: {w}  (warmup={WARMUP})")
print(f"Position: full={full}({full/w*100:.1f}%) half={half} empty={empty}({empty/w*100:.1f}%)")
print(f"Strategy annualized: {((nv[-1])**(52/w)-1)*100:.1f}%")
print(f"Buy-hold annualized: {((bh[-1])**(52/w)-1)*100:.1f}%")
print(f"Strategy final: {nv[-1]:.4f}x   Buy-hold: {bh[-1]:.4f}x")
diff = (nv[-1]-bh[-1])/bh[-1]*100
print(f"Alpha: {diff:+.1f}%")

# ==== Chart ====
fig, axes = plt.subplots(3, 1, figsize=(14, 10))

# Panel 1: Net value
axes[0].plot(nv, label="PE Strategy", linewidth=2, color="#1971c2")
axes[0].plot(bh, label="Buy Hold", linewidth=1.5, color="#868e96", alpha=0.7)
axes[0].set_title("PE Quantile Strategy — SSE Dividend Index (REAL PE Data)", fontsize=14)
axes[0].set_ylabel("Net Value"); axes[0].legend(); axes[0].grid(True, alpha=0.3)

# Panel 2: Position
colors = ["#2b8a3e" if p==1 else "#f08c00" if p==0.5 else "#c92a2a" for p in pos]
axes[1].scatter(range(len(pos)), pos, c=colors, s=3, alpha=0.6)
axes[1].set_title("Position Signal (green=full, orange=half, red=empty)")
axes[1].set_ylim(-0.1, 1.1); axes[1].grid(True, alpha=0.3)

# Panel 3: PE with thresholds over time
axes[2].plot(range(len(pe_vals)), pe_vals, linewidth=1, color="#1971c2", alpha=0.5, label="PE")
axes[2].axhline(y=np.mean(pe_vals), color="#868e96", linestyle="--", alpha=0.5, label="Mean PE")
axes[2].set_title("PE Value Over Time")
axes[2].set_ylabel("PE"); axes[2].legend(); axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUT / "lesson2_real_pe.png", dpi=150)
plt.close()
print(f"Chart saved to output/lesson2_real_pe.png")
print("Next: Lesson 3")