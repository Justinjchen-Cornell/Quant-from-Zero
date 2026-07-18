import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).parent.parent
DATA = BASE / "交接文件/9-11研究/代码"
OUT = BASE / "output"; OUT.mkdir(exist_ok=True)
print("Lesson 6: Return Distributions — What Do Returns Actually Look Like?")
print()
# Load index.csv daily returns
raw = pd.read_csv(DATA / "index.csv", encoding="gbk")
codes = list(raw.columns[1:])
df = raw.iloc[3:-2].copy()
df.columns = ["date"] + codes
for c in codes: df[c] = pd.to_numeric(df[c], errors="coerce") / 100.0
df['date'] = pd.to_datetime(df['date'])
daily = df.set_index('date')
# Weekly returns: group by week, compound 5 days
weekly = daily.resample('W').apply(lambda x: (1+x).prod() - 1)
print(f"Daily: {len(daily)} days, Weekly: {len(weekly)} weeks")


# The core question: are returns normally distributed?
# If yes -> VaR from normal distribution is valid
# If no (fat tails) -> VaR underestimates real risk

# Pick 4 representative indices
targets = {"000300.SH": "CSI300", "000001.SH": "SH Comp", "399324.SZ": "SZ Dividend", "159915.SZ": "ChiNext"}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for idx, (code, name) in enumerate(targets.items()):
    ax = axes[idx // 2][idx % 2]
    rets = weekly[code].dropna()
    # Histogram + KDE
    sns.histplot(rets, bins=50, kde=True, ax=ax, color="#1971c2", alpha=0.6)
    # Overlay normal distribution with same mean/std
    x = np.linspace(rets.min(), rets.max(), 200)
    from scipy import stats
    normal_pdf = stats.norm.pdf(x, rets.mean(), rets.std())
    ax_twin = ax.twinx()
    ax_twin.plot(x, normal_pdf, "r-", linewidth=2, alpha=0.7, label="Normal fit")
    ax_twin.set_ylim(0, ax_twin.get_ylim()[1])
    ax.set_title(name + " Weekly Returns (histogram vs normal)")
    ax.set_xlabel("Return"); ax.set_ylabel("Count")

    # Key stats
    skew = rets.skew()
    kurt = rets.kurtosis()  # excess kurtosis
    ax.text(0.02, 0.95, f"Skew={skew:.2f} Kurt={kurt:.2f}", transform=ax.transAxes,
            fontsize=10, verticalalignment="top", bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

plt.tight_layout()
plt.savefig(OUT / "lesson6_distributions.png", dpi=150)
plt.close()

# Print insights
print()
print("THE INSIGHT:")
print("  Skewness < 0 = more negative outliers (crashes)")
print("  Kurtosis > 0 = fatter tails than normal (more extremes)")
print("  Most financial returns have NEGATIVE skew and POSITIVE kurtosis.")
print("  This means: crashes happen more often than normal distribution predicts.")
print("  This is why VaR from Lesson 1 is BETTER than assuming normality.")
print("Chart: output/lesson6_distributions.png")
