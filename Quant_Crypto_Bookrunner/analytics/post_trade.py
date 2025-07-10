import pandas as pd


def summary(perf: pd.DataFrame) -> pd.DataFrame:
    """Return common performance metrics from a trade log DataFrame.

    Expected columns: ['timestamp', 'pnl']
    """
    cumulative = perf["pnl"].cumsum()
    out = {
        "total_pnl": cumulative.iloc[-1],
        "max_drawdown": (cumulative.cummax() - cumulative).max(),
        "sharpe": perf["pnl"].mean() / (perf["pnl"].std(ddof=0) + 1e-9) * (252 ** 0.5),
    }
    return pd.Series(out)