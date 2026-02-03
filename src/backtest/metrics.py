import numpy as np
import pandas as pd


def sharpe_ratio(returns: pd.Series, ann_factor: float):

    return ann_factor * returns.mean() / returns.std(ddof=0)

def max_drawdown(wealth: pd.Series):

    peak = wealth.cummax()
    return ((wealth - peak) / peak).min()
