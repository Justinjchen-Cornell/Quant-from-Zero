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
print("Lesson 7: Consecutive Up/Down Days — Calendar Patterns")
raw = pd.read_csv(DATA / "index.csv", encoding="gbk")
codes = list(raw.columns[1:])
df = raw.iloc[3:-2].copy()
df.columns = ["date"] + codes
for c in codes: df[c] = pd.to_numeric(df[c], errors="coerce") / 100.0
CODE = "000300.SH"
rets = df[CODE].dropna().values
# Find all consecutive up-day streaks
up_streaks = []
current = 0
for r in rets:
    if r > 0: current += 1
    else:
        if current > 0: up_streaks.append(current)
        current = 0
if current > 0: up_streaks.append(current)
down_streaks = []
current = 0
for r in rets:
    if r < 0: current += 1
    else:
        if current > 0: down_streaks.append(current)
        current = 0
if current > 0: down_streaks.append(current)
print(f"Up streaks: {len(up_streaks)}, max={max(up_streaks)}, mean={np.mean(up_streaks):.1f}")
print(f"Down streaks: {len(down_streaks)}, max={max(down_streaks)}, mean={np.mean(down_streaks):.1f}")


fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].bar(range(len(up_streaks)), sorted(up_streaks, reverse=True), color="#2b8a3e", alpha=0.7)
axes[0].set_title("Consecutive UP Days (CSI300)"); axes[0].set_xlabel("Streak #"); axes[0].set_ylabel("Days")
axes[1].bar(range(len(down_streaks)), sorted(down_streaks, reverse=True), color="#c92a2a", alpha=0.7)
axes[1].set_title("Consecutive DOWN Days (CSI300)"); axes[1].set_xlabel("Streak #"); axes[1].set_ylabel("Days")
plt.tight_layout()
plt.savefig(OUT / "lesson7_calendar.png", dpi=150)
plt.close()

# What does a 5-day streak predict?
print()
print("After a 5-day up streak, next day:")
idx_5up = [i for i in range(5, len(rets)) if all(r>0 for r in rets[i-5:i])]
if idx_5up:
    next_day = [rets[i] for i in idx_5up if i < len(rets)]
    print(f"  Count: {len(next_day)}, Pos: {sum(1 for r in next_day if r>0)}, Neg: {sum(1 for r in next_day if r<0)}")
    print(f"  Avg next-day return: {np.mean(next_day)*100:.2f}%")

print()
print("THE INSIGHT:")
print("  If streaks were random, they would follow a geometric distribution.")
print("  If real streaks are LONGER than random -> there IS momentum.")
print("  If real streaks match random -> no momentum, pure noise.")
print("  This is the simplest possible momentum detector.")
print("Chart: output/lesson7_calendar.png")
