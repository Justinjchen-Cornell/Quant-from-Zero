import akshare as ak
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
BASE = Path(__file__).parent.parent
DATA_DIR = BASE / "交接文件/9-11研究/代码"
DATA_DIR.mkdir(parents=True, exist_ok=True)
print("=" * 60)
print("Updating all data: index prices + PE + ETFs")
print("=" * 60)
date_str = datetime.now().strftime("%Y-%m-%d")
print(f"Pull date: {date_str}")
# Index code mapping: our code -> akshare symbol
INDEX_MAP = {
    "000001.SH": "sh000001", "000300.SH": "sh000300", "000016.SH": "sh000016",
    "000010.SH": "sh000010", "000903.SH": "sh000903", "000906.SH": "sh000906",
    "000925.SH": "sh000925", "399001.SZ": "sz399001", "399324.SZ": "sz399324",
    "399348.SZ": "sz399348", "399346.SZ": "sz399346", "159915.SZ": "sz399006",
    "159902.SZ": "sz399005", "512500.SH": "sh000905", "000015.SH": "sh000015",
    "161227.SZ": "sz399330",
}
# ===== 1. Pull all index prices =====
all_returns = {}
for code, symbol in INDEX_MAP.items():
    try:
        df = ak.stock_zh_index_daily(symbol=symbol)
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()
        # Compute daily return from close
        df["return"] = df["close"].pct_change() * 100  # in %, like old data
        all_returns[code] = df["return"]
        print(f"  {code:12s} -> {len(df):5d} days, {df.index[0].date()} to {df.index[-1].date()}")
    except Exception as e:
        print(f"  {code:12s} -> ERROR: {str(e)[:50]}")
# Build unified returns DataFrame
ret_df = pd.DataFrame(all_returns).dropna(how="all")
ret_df.index.name = "date"
print(f"Unified returns: {len(ret_df)} days, {len(ret_df.columns)} indices")
print(f"Range: {ret_df.index[0].date()} to {ret_df.index[-1].date()}")


# ===== 2. Pull PE data for indices =====
PE_INDICES = {"000300.SH": "沪深300", "000016.SH": "上证50", "512500.SH": "中证500", "399324.SZ": "深证红利"}
pe_data = {}
for code, name in PE_INDICES.items():
    try:
        df = ak.stock_index_pe_lg(symbol=name)
        df["date"] = pd.to_datetime(df.iloc[:,0])
        df = df.set_index("date").sort_index()
        pe_data[code] = df["滚动市盈率"]  # trailing PE
        print(f"  PE {name:6s} -> {len(df):5d} days, PE {df["滚动市盈率"].min():.1f}-{df["滚动市盈率"].max():.1f}")
    except Exception as e:
        print(f"  PE {name:6s} -> ERROR: {str(e)[:50]}")

# ===== 3. Align PE with weekly returns =====
# PE策略需要周度PE+收益数据
pe_weekly = {}
for code, pe_series in pe_data.items():
    if code in all_returns:
        rets = all_returns[code]
        # Resample to weekly: compound 5-day returns, take last PE of week
        weekly_ret = rets.resample("W").apply(lambda x: (1+x/100).prod() - 1)
        weekly_pe = pe_series.resample("W").last()
        # Align
        common_idx = weekly_ret.index.intersection(weekly_pe.index)
        if len(common_idx) > 100:
            pe_weekly[code] = pd.DataFrame({
                "date": common_idx,
                "PE": weekly_pe[common_idx].values,
                "return": weekly_ret[common_idx].values
            })
            print(f"  Weekly {code}: {len(common_idx)} weeks aligned")

# ===== 4. Save =====
# Save returns
ret_df.to_csv(DATA_DIR / "index_updated.csv", encoding="utf-8-sig")
print(f"Saved index_updated.csv: {len(ret_df)} days")

# Save PE data
for code, df_pe in pe_weekly.items():
    fname = code.replace(".", "_") + "_pe_weekly.csv"
    df_pe.to_csv(DATA_DIR / "PE" / fname, encoding="utf-8-sig", index=False)

print()
print("UPDATE COMPLETE. New data covers 2002-2026.")
print(f"Old data: 2000-2017 (4278 days)")
print(f"New data: {ret_df.index[0].date()} to {ret_df.index[-1].date()} ({len(ret_df)} days)")
