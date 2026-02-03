import numpy as np
import pandas as pd


def rsi(series: pd.Series, window: int) -> pd.Series:

    d = series.diff()
    up = d.clip(lower=0).ewm(alpha=1/window, min_periods=window, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/window, min_periods=window, adjust=False).mean()

    rs = up / dn.replace(0, np.nan)
    
    return 100 - 100 / (1 + rs)