import yfinance as yf
from pypfopt import expected_returns, risk_models, EfficientFrontier

# -----------------------------------
# 1. Define the assets
# -----------------------------------

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "SPY"]

# -----------------------------------
# 2. Download historical price data
# -----------------------------------

prices = yf.download(
    tickers,
    start="2020-01-01",
    end="2025-01-01",
    auto_adjust=True
)["Close"]

# -----------------------------------
# 3. Calculate expected annual returns
# -----------------------------------

mu = expected_returns.mean_historical_return(prices)

# -----------------------------------
# 4. Calculate annualized covariance matrix
# -----------------------------------

S = risk_models.sample_cov(prices)

# -----------------------------------
# 5. Create Efficient Frontier
#    Maximum 30% allocation per asset
# -----------------------------------

ef = EfficientFrontier(
    mu,
    S,
    weight_bounds=(0, 0.30)
)

# -----------------------------------
# 6. Find Maximum Sharpe Ratio Portfolio
# -----------------------------------

ef.max_sharpe()

# Clean very small weights
cleaned_weights = ef.clean_weights()

# -----------------------------------
# 7. Display Portfolio Allocation
# -----------------------------------

print("\nOptimized Portfolio Allocation:\n")

for ticker, weight in cleaned_weights.items():
    print(f"{ticker}: {weight:.2%}")

# -----------------------------------
# 8. Display Portfolio Performance
# -----------------------------------

print("\nPortfolio Performance:")

expected_return, volatility, sharpe_ratio = ef.portfolio_performance()

print(f"Expected Annual Return: {expected_return:.2%}")
print(f"Annual Volatility: {volatility:.2%}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")