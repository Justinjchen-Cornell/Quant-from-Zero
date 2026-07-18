import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
OUT = Path(__file__).parent.parent / "output"; OUT.mkdir(exist_ok=True)
np.random.seed(42)

# ===== LESSON 4: MONTE CARLO SIMULATION =====
print("=" * 60)
print("Monte Carlo = ask what if 1,000,000 times, then look at the distribution")
print("=" * 60)

print()
print("THE PROBLEM:")
print("  Invest in CSI300 today at 3800. What happens in 1 year?")
print("  History = ONE answer. Monte Carlo = 100,000 possible futures.")
print()

s0 = 3779.522; r = 0.1375; sigma = 0.2863
T = 1.0; M = 52; I = 100000; dt = T / M

S = np.zeros((M+1, I))
S[0] = s0
for t in range(1, M+1):
    Z = np.random.standard_normal(I)
    S[t] = S[t-1] * np.exp((r - 0.5*sigma**2) * dt + sigma * np.sqrt(dt) * Z)

print('Simulation done:', S.shape)
print('Week 52: min=' + str(int(S[-1].min())) + ' max=' + str(int(S[-1].max())) + ' mean=' + str(int(S[-1].mean())))


# ===== PART 3: Extract quantile paths =====
# Sort ALL 100,000 final prices, pick the one at each percentile rank
sorted_idx = S[-1].argsort()
pcts = [5, 10, 50, 90, 95]
paths = {}
for p in pcts:
    idx = sorted_idx[int(I * p / 100) - 1]
    paths[p] = S[:, idx]

# Build results table
results = pd.DataFrame()
for p in pcts:
    results[str(p) + '%'] = paths[p]
print()
print('Quantile paths (what the index looks like at each percentile):')
print(results.tail(5).to_string())

# ===== PART 4: Real-world interpretation =====
print()
print('=' * 50)
print('WHAT THIS MEANS FOR YOUR MONEY')
print('=' * 50)
final = S[-1]
for p in [5, 10, 50, 90, 95]:
    val = np.percentile(final, p)
    chg = (val - s0) / s0 * 100
    arrow = 'UP' if chg > 0 else 'DOWN'
    print(f'  {p:2d}% percentile: {val:7.0f}  ({chg:+5.0f}%)  {arrow}')

print()
print('HOW TO READ:')
print('  5% worst case: only 5% of scenarios are worse than this')
print('  95% best case: only 5% of scenarios are better than this')
print('  50% median: half above, half below')

# VaR: how much you lose in the worst 5% of scenarios
var_95 = (np.percentile(final, 5) - s0) / s0 * 100
print(f'  VaR 95% = {var_95:.0f}% = worst 5% loss')


# ===== PART 5: Visualize =====
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: 20 sample paths + quantile bands
for i in range(20):
    axes[0].plot(S[:, i*5000], linewidth=0.3, color='#868e96', alpha=0.4)
axes[0].plot(paths[50], linewidth=2, color='#1971c2', label='Median')
axes[0].fill_between(range(M+1), paths[5], paths[95], alpha=0.15, color='#1971c2', label='90% range')
axes[0].set_title('CSI300: 20 Sample Paths + 90% Confidence Band')
axes[0].set_ylabel('Price'); axes[0].legend(); axes[0].grid(True, alpha=0.3)

# Right: final price distribution
axes[1].hist(final, bins=100, color='#1971c2', alpha=0.7, edgecolor='white')
for p in pcts:
    val = np.percentile(final, p)
    axes[1].axvline(x=val, color='#c92a2a', linestyle='--', linewidth=1, alpha=0.7)
    axes[1].text(val, axes[1].get_ylim()[1]*0.9, str(p)+'%', ha='center', fontsize=9, color='#c92a2a')
axes[1].axvline(x=s0, color='#2b8a3e', linewidth=2, label='Today')
axes[1].set_title('Distribution of 100,000 Final Prices'); axes[1].legend()
axes[1].set_xlabel('Price'); axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUT / 'lesson4_monte_carlo.png', dpi=150)
plt.close()
print('Chart saved to output/lesson4_monte_carlo.png')

# ===== PART 6: The BIG IDEA =====
print()
print('THE BIG IDEA:')
print('  Monte Carlo does not predict. It maps the RANGE of possibilities.')
print('  No one can tell you CSI300 will be at 4500 next year.')
print('  But you CAN say: there is a 90% chance it will be between')
print('  X and Y. That is a decision-making input, not a forecast.')
print()
print('Next: apply this to Cannes Bay cash flow stress testing.')
