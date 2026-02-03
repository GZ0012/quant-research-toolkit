import pandas as pd
from src.indicators.rsi import rsi

def get_signals(series: pd.Series, window: int, low_th: float, high_th: float):
    r = rsi(series, window)
    

    # Entry: RSI crosses above the low threshold
    entry = (r >= low_th) & (r.shift(1) < low_th)
    # Exit: RSI crosses below the high threshold
    exit = (r <= high_th) & (r.shift(1) > high_th)
    

    return entry, exit