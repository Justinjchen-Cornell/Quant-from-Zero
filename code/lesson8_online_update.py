import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).parent.parent
OUT = BASE / "output"; OUT.mkdir(exist_ok=True)
DATA = BASE / "交接文件/9-11研究/代码"
print("Lesson 8: Online Statistics — No Peeking at the Future")
print()
# The sin of backtesting: using ALL historical data to compute mean/std
# Real investing: you only know data UP TO TODAY
# This lesson shows the difference.
raw = pd.read_csv(DATA / "index.csv", encoding="gbk")
codes = list(raw.columns[1:])
df = raw.iloc[3:-2].copy()
df.columns = ["date"] + codes
for c in codes: df[c] = pd.to_numeric(df[c], errors="coerce") / 100.0
CODE = "000300.SH"
daily = df[CODE].dropna().values
# Compute TWO versions of the moving average:
# V1: expanding (correct - only past data)
# V2: centered (cheating - uses future data)
n = len(daily)
expanding_mean = [np.mean(daily[:i+1]) for i in range(n)]
centered_mean = [np.mean(daily[max(0,i-10):min(n,i+11)]) for i in range(n)]
print(f"Final expanding mean: {expanding_mean[-1]*100:.2f}%")
print(f"Final centered mean: {centered_mean[-1]*100:.2f}%")
print(f"Difference at end: {(centered_mean[-1]-expanding_mean[-1])*100:.2f}%")
print()
print("THE INSIGHT:")
print("  Every strategy in Lessons 1-5 uses EXPANDING windows.")
print("  This is correct: no future data leaks into past decisions.")
print("  But parameters were tuned on the FULL dataset.")
print("  That IS a form of peeking: you chose m=2.0,n=1.0 BECAUSE")
print("  you already saw it worked. Walk-forward testing fixes this.")
