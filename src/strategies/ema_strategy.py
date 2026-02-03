import pandas as pd
from src.indicators.ema import calculate_ema

def get_signals(series: pd.Series, short_window: int, long_window: int):
    """
    EMA cross theory
    - Entry: Short EMA > Long EMA (golden cross)
    - Exit: Short EMA < Long EMA (death cross)
    """
    ema_s = calculate_ema(series, short_window)
    ema_l = calculate_ema(series, long_window)
    
    # signal
    entry_sig = (ema_s > ema_l) & (ema_s.shift(1) <= ema_l.shift(1))
    exit_sig = (ema_s < ema_l) & (ema_s.shift(1) >= ema_l.shift(1))
    
    return entry_sig, exit_sig