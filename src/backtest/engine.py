import numpy as np
import pandas as pd
from src.backtest.metrics import sharpe_ratio, max_drawdown

def run_backtest(series, entry_sig, exit_sig, max_loss_pct=None):
    """
    通用高精度回测引擎
    ----------------
    :param series: pd.Series
    :param entry_sig: pd.Series (bool), buy signal
    :param exit_sig: pd.Series (bool), sell signal
    :param max_loss_pct: float,
    :return: (outcome_dict, trades_df)
    """
    in_trade = False
    entry_idx = entry_px = None
    trade_log = []

    # simulate real trade day
    for t in range(len(series) - 1):
        if not in_trade:
            # always trade on the next bar
            if entry_sig.iat[t]:
                in_trade = True
                entry_idx = t + 1
                entry_px = series.iat[t + 1]
        else:
            # keep the stock
            nxt = t + 1
            reason = None
            
            # check the stop loss （N/A if not setting it)
            if max_loss_pct and series.iat[nxt] <= entry_px * (1 - max_loss_pct):
                reason = "STOP_LOSS"
            elif exit_sig.iat[t]:
                reason = "SIGNAL_EXIT"
            
            if reason:
                trade_log.append({
                    "entry_time": series.index[entry_idx],
                    "exit_time": series.index[nxt],
                    "entry_price": entry_px,
                    "exit_price": series.iat[nxt],
                    "ret": series.iat[nxt] / entry_px - 1,
                    "reason": reason
                })
                in_trade = False

    df_trades = pd.DataFrame(trade_log)
    
    if df_trades.empty:
        return None, df_trades

    trade_rets = df_trades['ret']
    
 
    outcome = {
        "cum_return": (1 + trade_rets).prod() - 1,
        "n_trades": len(df_trades),
        "win_rate": (trade_rets > 0).sum() / len(df_trades),
        "avg_trade_return": trade_rets.mean(),
        "max_drawdown": max_drawdown((1 + trade_rets).cumprod()),
        "sharpe": (trade_rets.mean() / trade_rets.std() * np.sqrt(252)) if len(trade_rets) > 1 else 0
    }

    return outcome, df_trades