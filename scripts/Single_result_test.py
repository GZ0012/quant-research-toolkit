import pandas as pd
from pathlib import Path
from src.utils.data_loader import load_price_series
from src.backtest.engine import run_backtest
import src.strategies.macd_strategy as macd_strat
import src.strategies.rsi_strategy as rsi_strat
import src.strategies.ema_strategy as ema_strat

# ================= Config =================
STRATEGY_TYPE = "EMA"  
DATA_PATH = Path("data/Sample.csv")

# MACD setup
MACD_PARAMS = {"short": 12, "long": 26, "signal": 9}
# RSI setup
RSI_PARAMS = {"window": 14, "low_th": 30, "high_th": 70}
# EMA setup
EMA_PARAMS = {"short_window": 20, "long_window": 50}
# =========================================

def main():
    series = load_price_series(DATA_PATH)
    
    if STRATEGY_TYPE.upper() == "MACD":
        en, ex = macd_strat.get_signals(series, **MACD_PARAMS)
    elif STRATEGY_TYPE.upper() == "RSI":
        en, ex = rsi_strat.get_signals(series, **RSI_PARAMS)
    elif STRATEGY_TYPE.upper() == "EMA": 
        en, ex = ema_strat.get_signals(series, **EMA_PARAMS)
    else:
        print("incorrect strategy type")
        return

    outcome, _ = run_backtest(series, en, ex)
    
    print(f"\n>>> Strategy: {STRATEGY_TYPE} | Data using: {DATA_PATH.name}")
    print("-" * 30)
    for k, v in outcome.items():
        print(f"{k:15}: {v:.4f}" if isinstance(v, float) else f"{k:15}: {v}")

if __name__ == "__main__":
    main()