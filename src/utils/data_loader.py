import pandas as pd
import numpy as np
from pathlib import Path

#time stamp
DATE_CANDIDATES = ["datetime", "timestamp", "date", "time", "Date", "DateTime", "Timestamp"]

def get_tf_table():
    """
    all the possible time stamp that will
    """
    return {
        "1m":  ["1m", "3m", "5m", "10m", "15m", "30m", "45m", "1h", "1d", "2d", "1w"],
        "5m":  ["5m", "10m", "15m", "30m", "45m", "1h", "1d", "2d", "1w"],
        "10m": ["10m", "20m", "30m", "40m", "50m", "1h", "1d", "2d", "1w"],
        "15m": ["15m", "30m", "45m", "1h", "1d", "2d", "1w"],
        "30m": ["30m", "45m", "1h", "1d", "2d", "1w"],
    }

def get_resample_alias(tf: str) -> str:
    """
    Make sure the tf can be identify by pandas
    """
    tf = tf.lower()
    if tf.endswith("m"): return tf.replace("m", "min")
    if tf.endswith("h"): return tf
    if tf.endswith("d"): return tf.upper()
    if tf.endswith("w"): return tf.upper()
    return tf

def load_price_series(
    csv: Path, 
    price_col: str = "close", 
    tz: str = "America/New_York" # mostly used New York
) -> pd.Series:
    """
    find the time stamp on the csv
    """
    df = pd.read_csv(csv)

    # auto finding time stemp
    dt_col = next((c for c in DATE_CANDIDATES if c in df.columns), None)
    if dt_col is None:
        raise ValueError(f"Error, no time stamp")

    # remove time stemp
    if np.issubdtype(df[dt_col].dtype, np.number):
        unit = "ms" if df[dt_col].iloc[0] > 1e12 else "s"
        df[dt_col] = pd.to_datetime(df[dt_col], unit=unit, utc=True)
    else:
        df[dt_col] = pd.to_datetime(df[dt_col], utc=True, errors="coerce")

    # remove the time period 
    df[dt_col] = df[dt_col].dt.tz_convert(tz).dt.tz_localize(None)
    
    # clean up the data
    df = df.dropna(subset=[dt_col, price_col]).sort_values(dt_col)
    
    return df.set_index(dt_col)[price_col]

def resample_to_tf(series: pd.Series, target_tf: str) -> pd.Series:
    """
    Resample the price sequence to the target period.
    """
    rule = get_resample_alias(target_tf)
    # make sure using the mostly right information to prevent forward-looking bias.
    return series.resample(rule, label="right", closed="right").last().dropna()