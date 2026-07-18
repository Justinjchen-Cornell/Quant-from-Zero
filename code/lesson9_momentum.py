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
print("Lesson 9: Momentum Strategy — Follow the Trend")
print("=" * 60)
print()
print("THE IDEA:")
print("  Do not predict. Just detect when something is accelerating.")
print("  When acceleration is detected -> hold for 3 periods -> exit.")
print("  This is the simplest trend-following system.")
print()
# We simulate a momentum signal from CSI300 returns
raw = pd.read_csv(DATA / "index.csv", encoding="gbk")
codes = list(raw.columns[1:])
df = raw.iloc[3:-2].copy()
df.columns = ["date"] + codes
for c in codes: df[c] = pd.to_numeric(df[c], errors="coerce") / 100.0
CODE = "000300.SH"
daily = df[CODE].dropna().values
# Step 1: Compute a simple momentum signal
# momentum = 5-day return / 20-day return (rate of change)
mom5 = np.array([np.prod(1+daily[max(0,i-5):i])-1 for i in range(5, len(daily))])
mom5 = mom5[15:]  # align
# Jump level: classify momentum into 5 levels
pcts = np.percentile(mom5, [20, 40, 60, 80])
levels = np.digitize(mom5, pcts)  # 0=weakest, 4=strongest
print(f"Momentum range: {mom5.min()*100:.1f}% to {mom5.max()*100:.1f}%")
print(f"Level thresholds: {[f"{p*100:.1f}%" for p in pcts]}")
# Signal: buy when level >= 4 (top 20% momentum)
HOLD = 3
signal = np.zeros(len(levels))
for i in range(len(levels)-HOLD):
    if levels[i] >= 4:
        signal[i:i+HOLD] = 1  # hold for 3 periods
# Step 2: Compute returns only during signal periods
rets_aligned = daily[5+15:5+15+len(signal)]  # align with signal
signal_returns = rets_aligned * signal
bh_returns = rets_aligned
# Net value
nv_sig = np.cumprod(1 + signal_returns)
nv_bh = np.cumprod(1 + bh_returns)
sa = (nv_sig[-1])**(252/len(signal_returns))-1
ba = (nv_bh[-1])**(252/len(bh_returns))-1
print(f"Signal ann: {sa*100:.1f}%  Buy-hold ann: {ba*100:.1f}%")
print(f"Final: {nv_sig[-1]:.4f}x vs {nv_bh[-1]:.4f}x")
print(f"Signal active: {signal.sum()/len(signal)*100:.1f}% of the time")


fig, axes = plt.subplots(2, 1, figsize=(14, 8))
axes[0].plot(nv_sig, label="Momentum Signal", linewidth=2, color="#1971c2")
axes[0].plot(nv_bh, label="Buy Hold", linewidth=1.5, color="#868e96", alpha=0.7)
axes[0].set_title("Momentum Strategy vs Buy Hold (CSI300)"); axes[0].legend(); axes[0].grid(True, alpha=0.3)
axes[1].fill_between(range(len(signal)), 0, signal, color="#2b8a3e", alpha=0.3, label="Signal ON")
axes[1].plot(mom5, linewidth=0.5, color="#1971c2", alpha=0.5, label="Momentum")
axes[1].axhline(y=pcts[3], color="#c92a2a", linewidth=1, linestyle="--", label="Buy threshold")
axes[1].set_title("Momentum Signal & Buy Threshold"); axes[1].legend(); axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "lesson9_momentum.png", dpi=150)
plt.close()

print()
print("COMPARED TO PE STRATEGY:")
print("  PE strategy: value-based (is it cheap?)")
print("  Momentum: trend-based (is it moving up?)")
print("  PE works when markets mean-revert. Momentum works when they trend.")
print("  They are COMPLEMENTARY: use PE for long-term, momentum for timing.")
print("Chart: output/lesson9_momentum.png")
