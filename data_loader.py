import yfinance as yf

# Stock/ETF ticker symbols
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "SPY"]

# Download historical market data
data = yf.download(
    tickers,
    start="2020-01-01",
    end="2025-01-01",
    auto_adjust=True
)

# Extract only closing prices
close_prices = data["Close"]

print("\nClosing Prices:")
print(close_prices.head())

print("\nShape of Closing Price Data:")
print(close_prices.shape)

# Calculate daily percentage returns
daily_returns = close_prices.pct_change()

# Remove the first row containing missing values
daily_returns = daily_returns.dropna()

print("\nDaily Returns:")
print(daily_returns.head())

print("\nShape of Daily Returns:")
print(daily_returns.shape)
# Calculate average daily returns
average_daily_returns = daily_returns.mean()

print("\nAverage Daily Returns:")
print(average_daily_returns)

# Calculate daily volatility
daily_volatility = daily_returns.std()

print("\nDaily Volatility:")
print(daily_volatility)

import numpy as np

# Annualize returns and volatility
annual_returns = average_daily_returns * 252
annual_volatility = daily_volatility * np.sqrt(252)

print("\nAnnualized Returns:")
print(annual_returns)

print("\nAnnualized Volatility:")
print(annual_volatility)

# Calculate correlation between asset returns
correlation_matrix = daily_returns.corr()

print("\nCorrelation Matrix:")
print(correlation_matrix)
# Calculate covariance matrix of daily returns
covariance_matrix = daily_returns.cov()

print("\nCovariance Matrix:")
print(covariance_matrix)

# -------------------------------
# Equal-Weight Portfolio Analysis
# -------------------------------

# Create equal weights for all assets
num_assets = len(tickers)
weights = np.array([1 / num_assets] * num_assets)

# Calculate annualized portfolio return
portfolio_return = np.dot(weights, annual_returns)

# Annualize the covariance matrix
annual_covariance_matrix = covariance_matrix * 252

# Calculate portfolio variance
portfolio_variance = np.dot(
    weights.T,
    np.dot(annual_covariance_matrix, weights)
)

# Calculate portfolio volatility
portfolio_volatility = np.sqrt(portfolio_variance)

print("\nPortfolio Weights:")
for ticker, weight in zip(tickers, weights):
    print(f"{ticker}: {weight:.2%}")

print("\nEqual-Weight Portfolio Performance:")
print(f"Expected Annual Return: {portfolio_return:.2%}")
print(f"Annual Volatility: {portfolio_volatility:.2%}")