import pandas as pd
def macd(series: pd.Series, short: int, long: int, signal: int):
    fast = series.ewm(span=short, adjust=False).mean()
    slow = series.ewm(span=long, adjust=False).mean()
    macd_line = fast - slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line