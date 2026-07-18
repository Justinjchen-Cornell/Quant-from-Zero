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
print("Lesson 10: Sharpe Ratio — Return per Unit of Risk")
print("=" * 60)
raw = pd.read_csv(DATA / "index.csv", encoding="gbk")
codes = list(raw.columns[1:])
df = raw.iloc[3:-2].copy()
df.columns = ["date"] + codes
for c in codes: df[c] = pd.to_numeric(df[c], errors="coerce") / 100.0
cn = ["SH180","SZ Value","SZ Growth","SZ100","SZ Div","ChiNext","SME","Fund50","CSI800","CSI500","CSI100","CSI300","SH180","SH50","SZ Comp","SH Comp"]
# Compute Sharpe = (annual_return - risk_free) / annual_volatility
rf = 0.035
results = []
for i, code in enumerate(codes):
    d = df[code].dropna().values
    ann_r = (np.prod(1+d))**(252/len(d)) - 1
    ann_v = np.std(d) * np.sqrt(252)
    sharpe = (ann_r - rf) / ann_v if ann_v > 0 else 0
    results.append({"Code":code, "Name":cn[i], "AnnRet":ann_r, "AnnVol":ann_v, "Sharpe":sharpe})
df_r = pd.DataFrame(results).sort_values("Sharpe", ascending=False)
print(); print(df_r.to_string(float_format=lambda x: f"{x*100:+.1f}%" if abs(x)<10 else f"{x:.3f}", index=False))


# ===== Rolling Sharpe: does ranking persist over time? =====
code = "000300.SH"
daily = df[code].dropna().values
window = 252*3  # 3-year rolling
rolling_sharpe = []
for i in range(window, len(daily)):
    w = daily[i-window:i]
    ann_r = (np.prod(1+w))**(252/len(w)) - 1
    ann_v = np.std(w) * np.sqrt(252)
    rolling_sharpe.append((ann_r - rf) / ann_v)

# Rolling Sharpe for CSI300
print(f'Rolling Sharpe (3yr): min={min(rolling_sharpe):.2f} max={max(rolling_sharpe):.2f}')

# Chart: just the ranking bar chart
fig, ax = plt.subplots(figsize=(14, 5))
colors = ["#2b8a3e" if s>0.5 else "#f08c00" if s>0 else "#c92a2a" for s in df_r["Sharpe"]]
ax.bar(range(len(df_r)), df_r["Sharpe"].values, color=colors)
ax.axhline(y=0.5, color="#868e96", linestyle="--", label="Good (>0.5)")
ax.set_xticks(range(len(df_r))); ax.set_xticklabels(df_r["Name"], rotation=45, ha="right")
ax.set_title("16-Index Sharpe Ranking"); ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout(); plt.savefig(OUT / "lesson10_sharpe.png", dpi=150); plt.close()
print("Chart: output/lesson10_sharpe.png")
print()
print("THE INSIGHT:")
print("  Sharpe ratio is the single best metric for comparing assets.")
print("  But it has a fatal flaw: it penalizes upside volatility.")
print("  An asset that goes UP 50%% then DOWN 10%% looks worse than")
print("  one that goes up 10%% steadily. Sortino ratio fixes this.")
