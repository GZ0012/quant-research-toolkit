
# quant-research-toolkit

This is a quant research toolkit designed for stock digging and financial data storage. It is an entry-level framework built for high-precision strategy backtesting.

## Project Overview
This toolkit allows users to backtest fundamental quantitative strategies against historical price data. It is designed to be modular, making it easy to swap indicators, strategies, and datasets for rapid research and parameter optimization.

## Data Specification
The project includes a sample dataset located in the `data/` directory:
* **Asset**: NQ (Nasdaq 100 Index Futures)
* **Time Range**: March 2025 – June 2025
* **Interval**: 1-minute (1min) OHLCV data
* **Purpose**: This high-frequency data is used to validate the accuracy of signal generation and execution lag.

## Integrated Strategies
The toolkit currently supports three core technical analysis strategies:
1. **EMA (Exponential Moving Average)**: A trend-following strategy using dual-moving average crossovers.
2. **MACD (Moving Average Convergence Divergence)**: A momentum strategy based on the relationship between two moving averages of prices.
3. **RSI (Relative Strength Index)**: A mean-reversion strategy that identifies overbought or oversold conditions.

---

## Script Explanations

The toolkit is operated via three core scripts located in the `scripts/` directory. Each serves a specific stage of the research workflow:

### 1. `Single_result_test.py` (Performance Summary)
* **Purpose**: Quickly validates the final performance of a strategy using a **specific set of parameters**.
* **Output**: Prints a summary of performance metrics (Outcome), including Cumulative Return, Win Rate, Sharpe Ratio, and Maximum Drawdown.
* **Use Case**: Use this when you have a specific hypothesis (e.g., EMA 20/50) and want to see the "bottom line" results on the NQ dataset.

### 2. `run_details.py` (Trade Log Audit)
* **Purpose**: Provides a deep dive into the backtest by printing **every individual trade** executed.
* **Output**: A detailed table containing entry/exit timestamps, entry/exit prices, individual trade returns (ret), and the reason for closing the position (Signal Exit or Stop Loss).
* **Use Case**: Essential for debugging strategy logic and understanding how the strategy behaves during specific market events or volatility.

### 3. `run_grid_search.py` (Parameter Optimization)
* **Purpose**: **Automatically discovers the optimal parameters** for a given strategy.
* **Functionality**: The script iterates through a defined grid of parameters and multiple timeframes (resampling the 1min NQ data to 5m, 15m, 1h, etc.).
* **Output**: Generates a comprehensive CSV report (`grid_search_report.csv`) sorted by Sharpe Ratio to highlight the most robust parameter combinations.
* **Use Case**: Use this when you are unsure which moving average lengths or RSI thresholds perform best across different market cycles.

---

## How to Run
Ensure you are in the project root directory and execute the following commands:

```bash
# To run a single performance test
python -m scripts.Single_result_test

# To view detailed trade logs
python -m scripts.run_details

# To start a full parameter grid search
python -m scripts.run_grid_search 

# To setup all the requirement
pip install -r requirements.txt

