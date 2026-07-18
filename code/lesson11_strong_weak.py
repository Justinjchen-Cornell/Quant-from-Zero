import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).parent.parent
DATA = BASE / "交接文件/9-11研究/代码"
OUT = BASE / "output"; OUT.mkdir(exist_ok=True)
print("=" * 60)
print("Lesson 11: Old vs New Strong-Weak Strategy")
print("=" * 60)
print()
print("THE CONCEPT:")
print("  Strong-Weak = momentum with JUMP LEVELS.")
print("  Not just is it going up? but HOW STRONG is the up move?")
print("  Jump levels range from -8 to +8. Extreme values = strong signals.")
print()
print("OLD STRATEGY (Notebooks 7-10):")
print("  Single index. Buy when jump level in {-7,-6,-5,4,7}.")
print("  Hold for 3 periods. Only long signals (no shorting).")
print()
print("NEW STRATEGY (Notebooks 13-16):")
print("  Added: IF/IC futures, COMBINED strong+weak signals,")
print("  portfolio-level net value, deep jump level statistics.")
print("  Key innovation: use BOTH strong AND weak jump levels.")
print()
# We simulate jump levels from real index return data
raw = pd.read_csv(DATA / "index.csv", encoding="gbk")
codes = list(raw.columns[1:])
df = raw.iloc[3:-2].copy()
df.columns = ["date"] + codes
for c in codes: df[c] = pd.to_numeric(df[c], errors="coerce") / 100.0
CODE = "000300.SH"
daily = df[CODE].dropna().values
# Step 1: compute 5-day momentum
mom5 = np.array([np.prod(1+daily[max(0,i-5):i])-1 for i in range(5, len(daily))])
# Step 2: classify into jump levels (-4 to +4)
pcts = np.percentile(mom5, [5,15,30,50,70,85,95])
levels = np.digitize(mom5, pcts) - 4  # center around 0, range -4 to +4
print(f"Momentum range: {mom5.min()*100:.1f}% to {mom5.max()*100:.1f}%")
print(f"Level distribution: {dict(zip(*np.unique(levels, return_counts=True)))}")
print()
# Step 3: OLD strategy - only strong long signals
old_signal_levels = {-4, -3, 3, 4}  # extreme levels
old_signal = np.zeros(len(levels))
for i in range(len(levels)-3):
    if levels[i] in old_signal_levels:
        old_signal[i:i+3] = 1
# Step 4: NEW strategy - BOTH strong AND weak
new_signal_levels = {-4, -3, -2, 2, 3, 4}  # wider capture
new_signal = np.zeros(len(levels))
for i in range(len(levels)-3):
    if levels[i] in new_signal_levels:
        new_signal[i:i+3] = 1
# Performance
rets = daily[5:5+len(levels)]
old_nv = np.prod(1 + old_signal * rets)
new_nv = np.prod(1 + new_signal * rets)
bh_nv = np.prod(1 + rets)
old_ann = old_nv**(252/len(rets))-1
new_ann = new_nv**(252/len(rets))-1
bh_ann = bh_nv**(252/len(rets))-1
old_active = old_signal.sum()/len(old_signal)*100
new_active = new_signal.sum()/len(new_signal)*100
print(f"Old Strategy: {old_ann*100:.1f}% ann, active {old_active:.0f}%, nv={old_nv:.3f}x")
print(f"New Strategy: {new_ann*100:.1f}% ann, active {new_active:.0f}%, nv={new_nv:.3f}x")
print(f"Buy-Hold:     {bh_ann*100:.1f}% ann, nv={bh_nv:.3f}x")
print(f"New vs Old:  {(new_ann-old_ann)*100:+.1f}% annual difference")


# ===== KEY INNOVATION: Jump Level Persistence =====
# Does a level 4 signal today predict the NEXT signal?
transitions = {}
for i in range(len(levels)-1):
    k = (levels[i], levels[i+1])
    transitions[k] = transitions.get(k, 0) + 1
top_transitions = sorted(transitions.items(), key=lambda x: -x[1])[:5]
print()
print("Top 5 level transitions (persistence check):")
for (a, b), count in top_transitions:
    print(f"  Level {a:+d} -> Level {b:+d}: {count} times")

# ===== OLD vs NEW: Why NEW wins =====
print()
print("OLD vs NEW — KEY DIFFERENCES:")
print("  OLD: waits for EXTREME signals (-4,-3,3,4). Misses medium moves.")
print("  NEW: captures medium signals too (-2,2). More trades, less missed.")
print("  OLD: single index only. NEW: can trade futures (IF/IC).")
print("  OLD: only long. NEW: weak levels -> short signals on futures.")
print()

# Chart
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
# Panel 1: Net value comparison
axes[0,0].plot(np.cumprod(1+old_signal*rets), label="Old (extreme only)", linewidth=2, color="#c92a2a")
axes[0,0].plot(np.cumprod(1+new_signal*rets), label="New (wider capture)", linewidth=2, color="#1971c2")
axes[0,0].plot(np.cumprod(1+rets), label="Buy Hold", linewidth=1.5, color="#868e96", alpha=0.7)
axes[0,0].set_title("Old vs New Strategy Net Value"); axes[0,0].legend(); axes[0,0].grid(True, alpha=0.3)

# Panel 2: Jump level distribution
from collections import Counter
lc = Counter(levels)
axes[0,1].bar(lc.keys(), lc.values(), color="#1971c2", alpha=0.7)
axes[0,1].set_title("Jump Level Distribution (CSI300)"); axes[0,1].set_xlabel("Level"); axes[0,1].grid(True, alpha=0.3)

# Panel 3: Old signal
axes[1,0].fill_between(range(len(old_signal)), 0, old_signal, color="#c92a2a", alpha=0.3)
axes[1,0].plot(levels, linewidth=0.5, color="#1971c2", alpha=0.5)
axes[1,0].set_title("Old Strategy Signal (extreme only)"); axes[1,0].set_ylim(-5, 5)

# Panel 4: New signal
axes[1,1].fill_between(range(len(new_signal)), 0, new_signal, color="#1971c2", alpha=0.3)
axes[1,1].plot(levels, linewidth=0.5, color="#1971c2", alpha=0.5)
axes[1,1].set_title("New Strategy Signal (wider capture)"); axes[1,1].set_ylim(-5, 5)

plt.tight_layout(); plt.savefig(OUT / "lesson11_strong_weak.png", dpi=150); plt.close()
print("Chart: output/lesson11_strong_weak.png")
