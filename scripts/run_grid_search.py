import pandas as pd
from pathlib import Path
from itertools import product
from tqdm import tqdm
from src.utils.data_loader import load_price_series, resample_to_tf, get_tf_table
from src.backtest.engine import run_backtest
import src.strategies.macd_strategy as macd_strat
import src.strategies.rsi_strategy as rsi_strat
import src.strategies.ema_strategy as ema_strat


# ================= Config =================
STRATEGY_TYPE = "MACD"  
DATA_PATH = Path("data/Sample.csv")  
BASE_TF = "1m"         
OUT_CSV = Path("results/grid_search_report.csv")


MACD_GRID = {
    "short": range(10, 30, 5),
    "long": range(30, 70, 10),
    "signal": [9, 12]
}

RSI_GRID = {
    "window": range(10, 21, 5),
    "low_th": [30, 35],
    "high_th": [70, 75]
}
# =========================================

def main():
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    

    base_series = load_price_series(DATA_PATH)
    tf_table = get_tf_table()
    target_tfs = tf_table.get(BASE_TF, [BASE_TF])
    
    all_results = []
    

    grid_config = MACD_GRID if STRATEGY_TYPE.upper() == "MACD" else RSI_GRID
    keys, values = zip(*grid_config.items())
    combinations = [dict(zip(keys, v)) for v in product(*values)]

    for tf in tqdm(target_tfs, desc="Timeframes"):

        series = resample_to_tf(base_series, tf)
        if len(series) < 100: continue 

        for params in tqdm(combinations, desc=f"Grid@{tf}", leave=False):
            if STRATEGY_TYPE.upper() == "MACD":
                if params['short'] >= params['long']: continue
                en, ex = macd_strat.get_signals(series, **params)
            else:
                en, ex = rsi_strat.get_signals(series, **params)
            
            outcome, _ = run_backtest(series, en, ex)
            
            # record
            if outcome:
                res_row = {
                    "strategy": STRATEGY_TYPE,
                    "tf": tf,
                    "params": str(params),
                    **outcome
                }
                all_results.append(res_row)

    # report
    if all_results:
        df = pd.DataFrame(all_results)
        df = df.sort_values("sharpe", ascending=False)
        df.to_csv(OUT_CSV, index=False)
        print(f"\nFinished! Grid search report saved to: {OUT_CSV}")
        print(df.head(10)) # top 10 
    else:
        print("\n No trades generated for any parameter combinations.")

if __name__ == "__main__":
    main()