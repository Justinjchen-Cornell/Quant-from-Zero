import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
DATA = Path(__file__).parent.parent / "交接文件/9-11研究/代码/交易策略1"
OUT = Path(__file__).parent.parent / "output"; OUT.mkdir(exist_ok=True)
print("=" * 60)
print("Lesson 5: Signal-Based Trading — Buy When Told, Sell When Told")
print("=" * 60)


# ===== THE IDEA =====
# Lessons 2-3: you decide position based on valuation (PE).
# Lesson 5: someone else gives you buy/sell signals. You just follow them.
# Question: are these signals any good?

# Load data
stock = pd.read_csv(DATA / "stock.csv", encoding="utf-8-sig")
signal = pd.read_csv(DATA / "signal.csv", encoding="utf-8-sig")

# Merge: align stock prices with buy/sell signals
df = pd.merge(stock, signal, on="日期", how="left")
# Filter: keep only rows where signal column is not NaN
df2 = df[(df["sell"] == 0.0) | (df["sell"] == 1.0)].copy()
df2.index = range(len(df2))

print(f"Total trading days with signals: {len(df2)}")
print(f"Columns: {list(df2.columns)}")
print(f"Signal pattern: even rows = BUY, odd rows = SELL")

# Pick one index for demonstration
CODE = "000300.SH"  # CSI300
print(f"Testing on: {CODE}")

# Extract buy and sell prices
# Even indices (0,2,4...) = buy, Odd indices (1,3,5...) = sell
buy_idx = list(range(0, len(df2), 2))
sell_idx = list(range(1, len(df2), 2))

buy_prices = df2.iloc[buy_idx][CODE].values
sell_prices = df2.iloc[sell_idx][CODE].values

# Compute log return per trade: ln(sell_price / buy_price)
trades = len(buy_prices)
log_returns = np.log(sell_prices / buy_prices)

print(f"Trades: {trades}")
print(f"Avg log return per trade: {np.mean(log_returns):.4f}")
print(f"Win rate: {sum(1 for r in log_returns if r>0)/trades*100:.1f}%")


# ===== Performance Metrics =====
cum_return = np.sum(log_returns)
# Time span: first buy to last sell
first_date = df2.iloc[buy_idx[0]]["日期"]
last_date = df2.iloc[sell_idx[-1]]["日期"]
years = (last_date - first_date) / 365
ann_return = (1 + cum_return)**(1/years) - 1 if years > 0 else 0

# Volatility of trade returns
trade_vol = np.std(log_returns)

# Max drawdown on cumulative returns
cum_series = np.cumsum(log_returns)
peak = np.maximum.accumulate(cum_series)
dd = cum_series - peak
max_dd = np.min(dd)

# VaR
sorted_rets = sorted(log_returns, reverse=True)
var_99 = sorted_rets[round(len(sorted_rets)*0.99)]

print(f"Time span: {years:.1f} years")
print(f"Cumulative return: {cum_return:.4f}  ({np.exp(cum_return)-1:.1%})")
print(f"Annualized return: {ann_return:.1%}")
print(f"Avg return per trade: {np.mean(log_returns):.4f}")
print(f"Trade volatility: {trade_vol:.4f}")
print(f"Max drawdown: {max_dd:.4f}")
print(f"VaR 99%: {var_99:.4f}")
print(f"Sharpe-like: {np.mean(log_returns)/trade_vol:.4f}" if trade_vol>0 else "")

# ===== Visualize =====
fig, axes = plt.subplots(2, 1, figsize=(14, 8))

# Trade returns
colors = ["#2b8a3e" if r>0 else "#c92a2a" for r in log_returns]
axes[0].bar(range(trades), log_returns, color=colors, alpha=0.7)
axes[0].axhline(y=0, color="#868e96", linewidth=0.5)
axes[0].axhline(y=np.mean(log_returns), color="#1971c2", linewidth=1.5, linestyle="--", label="Mean")
axes[0].set_title(f"CSI300: {trades} Trade Returns (Signal-Based)")
axes[0].set_ylabel("Log Return"); axes[0].legend(); axes[0].grid(True, alpha=0.3)

# Cumulative return
axes[1].plot(np.exp(np.cumsum(log_returns)), linewidth=2, color="#1971c2")
axes[1].axhline(y=1, color="#868e96", linewidth=0.5, linestyle="--")
axes[1].fill_between(range(trades), 1, np.exp(np.cumsum(log_returns)), alpha=0.15, color="#1971c2")
axes[1].set_title("Cumulative Net Value from Signals"); axes[1].set_ylabel("Net Value")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUT / "lesson5_signals.png", dpi=150)
plt.close()
print("Chart: output/lesson5_signals.png")

print()
print("THE LESSON:")
print("  This strategy does not decide WHEN to trade.")
print("  It only evaluates: if someone ELSE gives you signals,")
print("  are those signals profitable?")
print("  This is the framework for testing ANY external signal source.")
