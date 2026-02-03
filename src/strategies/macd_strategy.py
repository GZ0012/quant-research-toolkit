import pandas as pd
from src.indicators.macd import macd

def get_signals(series: pd.Series, short: int, long: int, signal: int):
    """
    MACD Golden cross
    """
    macd_line, sig_line = macd(series, short, long, signal)
    
    # Entry: MACD line cross Signal line
    entry = (macd_line > sig_line) & (macd_line.shift(1) <= sig_line.shift(1))
    # Exit: MACD cross under Signal line
    exit = (macd_line < sig_line) & (macd_line.shift(1) >= sig_line.shift(1))
    
    return entry, exit