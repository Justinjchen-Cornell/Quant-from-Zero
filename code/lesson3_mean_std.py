import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).parent.parent
DATA = BASE / "交接文件/9-11研究/代码/PE"
OUT = BASE / "output"; OUT.mkdir(exist_ok=True)
# Try CSI300 — has a more moderate PE range
raw = pd.read_csv(DATA / "沪深300PE策略.csv", encoding="gbk")
pe = pd.to_numeric(raw["PE"], errors="coerce")
ret = pd.to_numeric(raw["re"], errors="coerce")
pe_vals = pe.values; r_vals = ret.values; N = len(pe_vals)
WARMUP, m, n = 202, 2.0, 1.5
print(f"PE range: {pe.min():.1f} to {pe.max():.1f}, N={N}")
print(f"Params: m={m}(sell), n={n}(buy) -> 5 zones")

pos = [0]
for i in range(WARMUP, N):
    cur = np.mean(pe_vals[i-5:i])
    avg = np.mean(pe_vals[0:(i-1)])
    std = np.std(pe_vals[0:(i-1)])
    if cur <= avg - m*std: pos.append(1)
    elif cur <= avg - n*std:
        pos.append(1 if pos[-1]==1 else (0.5 if pos[-1]==0 else 0.5))
    elif cur < avg + n*std: pos.append(pos[-1])
    elif cur < avg + m*std:
        pos.append(0.5 if pos[-1]==1 else pos[-1])
    else: pos.append(0)
pos = pos[1:]

r = r_vals[WARMUP:]
nv = [1.0]
for i in range(len(pos)):
    rr = 0.035/52 if pos[i]==0 else pos[i]*r[i]
    nv.append(nv[-1]*(1+rr))
nv = np.array(nv)
bh = [1.0]
for rr in r: bh.append(bh[-1]*(1+rr))
bh = np.array(bh)

w = len(pos)
full = sum(1 for p in pos if p==1)
half = sum(1 for p in pos if p==0.5)
empty = sum(1 for p in pos if p==0)
sa = (nv[-1])**(52/w)-1
ba = (bh[-1])**(52/w)-1
alpha = (nv[-1]-bh[-1])/bh[-1]*100

print(f"Mean-StdDev Strategy ({w} weeks)")
print(f"Position: full={full} half={half} empty={empty}")
print(f"Ann: strategy={sa*100:.1f}%  buy-hold={ba*100:.1f}%  alpha={alpha:+.1f}%")
print(f"Final: strategy={nv[-1]:.4f}x  buy-hold={bh[-1]:.4f}x")


fig, axes = plt.subplots(3, 1, figsize=(14, 10))
axes[0].plot(nv, label="Mean-StdDev", linewidth=2, color="#2b8a3e")
axes[0].plot(bh, label="Buy Hold", linewidth=1.5, color="#868e96", alpha=0.7)
axes[0].set_title("Mean-StdDev Strategy — SSE Dividend"); axes[0].legend(); axes[0].grid(True, alpha=0.3)

colors = ["#2b8a3e" if p==1 else "#f08c00" if p==0.5 else "#c92a2a" for p in pos]
axes[1].scatter(range(len(pos)), pos, c=colors, s=3, alpha=0.6)
axes[1].set_title("Position (green=full, orange=half, red=empty)")
axes[1].set_ylim(-0.1, 1.1); axes[1].grid(True, alpha=0.3)

x = range(WARMUP, N)
ra = [np.mean(pe_vals[0:i]) for i in range(WARMUP, N)]
rs = [np.std(pe_vals[0:i]) for i in range(WARMUP, N)]
upper = [a + m*s for a,s in zip(ra, rs)]
lower = [a - m*s for a,s in zip(ra, rs)]
axes[2].fill_between(x, lower, upper, alpha=0.15, color="#2b8a3e", label=f"+/-{m} std")
axes[2].plot(x, pe_vals[WARMUP:], linewidth=1, color="#1971c2", label="PE")
axes[2].plot(x, ra, linewidth=1.5, color="#868e96", linestyle="--", label="Running Mean")
axes[2].set_title("PE with Dynamic +/-2 Std Bands"); axes[2].legend(); axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUT / "lesson3_mean_std.png", dpi=150)
plt.close()
print("Chart: output/lesson3_mean_std.png")

print()
print("Quantile = WHERE in ranking (relative)")
print("StdDev   = HOW FAR from normal (absolute)")
print("StdDev better when index has stable personality.")
