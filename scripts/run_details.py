import pandas as pd
from pathlib import Path
from src.utils.data_loader import load_price_series
from src.backtest.engine import run_backtest
import src.strategies.macd_strategy as macd_strat
import src.strategies.rsi_strategy as rsi_strat
import src.strategies.ema_strategy as ema_strat

# ================= Config =================
STRATEGY_TYPE = "MACD"  
DATA_PATH = Path("data/Sample.csv")

# MACD setup
MACD_PARAMS = {"short": 12, "long": 26, "signal": 9}
RSI_PARAMS = {"window": 14, "low_th": 30, "high_th": 70}
EMA_PARAMS = {"short_window": 20, "long_window": 50}
# =========================================

def main():

    series = load_price_series(DATA_PATH)
    
    if STRATEGY_TYPE.upper() == "MACD":
        en, ex = macd_strat.get_signals(series, **MACD_PARAMS)
    elif STRATEGY_TYPE.upper() == "RSI":
        en, ex = rsi_strat.get_signals(series, **RSI_PARAMS)
    elif STRATEGY_TYPE.upper() == "EMA": # 新增分支
        en, ex = ema_strat.get_signals(series, **EMA_PARAMS)
    else:
        print("Incorrect strategy type")
        return

    # detail trade
    _, trades = run_backtest(series, en, ex)
    
    # report
    print(f"\n>>> {STRATEGY_TYPE} Trade Details Report | Data: {DATA_PATH.name}")
    print("=" * 80)
    
    if trades is not None and not trades.empty:

        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_rows', 100)
        
        # trade 
        print(trades[['entry_time', 'exit_time', 'entry_price', 'exit_price', 'ret', 'reason']])
        
        print("-" * 80)
        print(f"Total trades: {len(trades)}")
    else:
        print("No trades were generated under this configuration.")

if __name__ == "__main__":
    main()