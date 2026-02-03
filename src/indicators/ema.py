import pandas as pd

def calculate_ema(series: pd.Series, window: int) -> pd.Series:
    """
    calculate the average move of ema
    """
    avg = series.ewm(span=window, adjust=False).mean()
    return avg