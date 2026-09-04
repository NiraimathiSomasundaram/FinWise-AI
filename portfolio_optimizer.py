import yfinance as yf
from pypfopt import expected_returns, risk_models, EfficientFrontier


# ==========================================
# FINWISE AI - RISK-AWARE PORTFOLIO OPTIMIZER
# ==========================================


# ------------------------------------------
# 1. DEFINE ASSET CLASSES
# ------------------------------------------

# Broad / diversified equity assets
CORE_EQUITIES = [
    "VTI",   # Total US Stock Market
    "SPY",   # S&P 500
    "VXUS"   # International Stocks
]

# Defensive / relatively stable equity sectors
DEFENSIVE_EQUITIES = [
    "XLV",   # Healthcare
    "VNQ"    # Real Estate
]

# Growth / sector-focused equities
GROWTH_EQUITIES = [
    "QQQ",   # Technology / Growth
    "XLF",   # Financials
    "XLE"    # Energy
]

# Fixed income
BOND_ASSETS = [
    "AGG",   # Aggregate Bonds
    "TLT"    # Long-Term Treasury Bonds
]

# Alternatives
ALTERNATIVE_ASSETS = [
    "GLD"    # Gold
]


# ------------------------------------------
# 2. COMPLETE MARKET DATA UNIVERSE
# ------------------------------------------

ALL_TICKERS = (
    CORE_EQUITIES
    + DEFENSIVE_EQUITIES
    + GROWTH_EQUITIES
    + BOND_ASSETS
    + ALTERNATIVE_ASSETS
)


# ==========================================
# MAIN PORTFOLIO FUNCTION
# ==========================================

def get_portfolio(profile):

    print("\nDownloading historical market data...")

    # --------------------------------------
    # Download historical prices
    # --------------------------------------

    prices = yf.download(
        ALL_TICKERS,
        start="2020-01-01",
        end="2025-01-01",
        auto_adjust=True
    )["Close"]

    prices = prices.dropna()

    # --------------------------------------
    # Calculate expected returns
    # --------------------------------------

    mu = expected_returns.mean_historical_return(prices)

    # --------------------------------------
    # Calculate covariance matrix
    # --------------------------------------

    S = risk_models.sample_cov(prices)

    # ======================================
    # CONSERVATIVE PROFILE
    # ======================================

    if "Conservative" in profile:

        print("\nInvestment Strategy: CONSERVATIVE 🟢")
        print("Focus: Capital preservation and lower volatility")

        # Conservative investors get safer,
        # broader investment choices.

        selected_assets = (
            ["SPY", "VTI", "XLV", "VNQ"]
            + BOND_ASSETS
            + ALTERNATIVE_ASSETS
        )

        equity_max = 0.40
        bond_min = 0.40
        gold_max = 0.15

        max_individual_weight = 0.30


    # ======================================
    # MODERATE PROFILE
    # ======================================

    elif "Moderate" in profile:

        print("\nInvestment Strategy: MODERATE 🟡")
        print("Focus: Balanced growth and risk")

        # Moderate investors get a mix of
        # diversified + growth assets.

        selected_assets = (
            CORE_EQUITIES
            + DEFENSIVE_EQUITIES
            + ["QQQ", "XLF"]
            + BOND_ASSETS
            + ALTERNATIVE_ASSETS
        )

        equity_max = 0.70
        bond_min = 0.15
        gold_max = 0.15

        max_individual_weight = 0.35


    # ======================================
    # AGGRESSIVE PROFILE
    # ======================================

    else:

        print("\nInvestment Strategy: AGGRESSIVE 🔴")
        print("Focus: Long-term growth and higher risk")

        # Aggressive investors can access
        # the complete equity universe.

        selected_assets = (
            CORE_EQUITIES
            + DEFENSIVE_EQUITIES
            + GROWTH_EQUITIES
            + BOND_ASSETS
            + ALTERNATIVE_ASSETS
        )

        equity_min = 0.70
        bond_max = 0.15
        gold_max = 0.10

        max_individual_weight = 0.40


    # --------------------------------------
    # Select relevant market data
    # --------------------------------------

    selected_prices = prices[selected_assets]

    selected_mu = mu[selected_assets]

    selected_S = S.loc[
        selected_assets,
        selected_assets
    ]


    # --------------------------------------
    # Create Efficient Frontier
    # --------------------------------------

    ef = EfficientFrontier(
        selected_mu,
        selected_S,
        weight_bounds=(0, max_individual_weight)
    )


    # --------------------------------------
    # Define asset classes for selected assets
    # --------------------------------------

    selected_equities = [
        asset for asset in selected_assets
        if asset not in BOND_ASSETS
        and asset not in ALTERNATIVE_ASSETS
    ]

    selected_bonds = [
        asset for asset in BOND_ASSETS
        if asset in selected_assets
    ]


    # ======================================
    # APPLY PROFILE CONSTRAINTS
    # ======================================

    # Conservative constraints
    if "Conservative" in profile:

        # Equity maximum
        ef.add_constraint(
            lambda w: sum(
                w[list(selected_mu.index).index(asset)]
                for asset in selected_equities
            ) <= equity_max
        )

        # Bonds minimum
        ef.add_constraint(
            lambda w: sum(
                w[list(selected_mu.index).index(asset)]
                for asset in selected_bonds
            ) >= bond_min
        )


    # Moderate constraints
    elif "Moderate" in profile:

        # Equity maximum
        ef.add_constraint(
            lambda w: sum(
                w[list(selected_mu.index).index(asset)]
                for asset in selected_equities
            ) <= equity_max
        )

        # Bonds minimum
        ef.add_constraint(
            lambda w: sum(
                w[list(selected_mu.index).index(asset)]
                for asset in selected_bonds
            ) >= bond_min
        )


    # Aggressive constraints
    else:

        # Equity minimum
        ef.add_constraint(
            lambda w: sum(
                w[list(selected_mu.index).index(asset)]
                for asset in selected_equities
            ) >= equity_min
        )

        # Bonds maximum
        ef.add_constraint(
            lambda w: sum(
                w[list(selected_mu.index).index(asset)]
                for asset in selected_bonds
            ) <= bond_max
        )


    # --------------------------------------
    # Gold maximum allocation
    # --------------------------------------

    if "GLD" in selected_mu.index:

        gold_index = list(selected_mu.index).index("GLD")

        ef.add_constraint(
            lambda w: w[gold_index] <= gold_max
        )


    # ======================================
    # OPTIMIZE PORTFOLIO
    # ======================================

    ef.max_sharpe()

    cleaned_weights = ef.clean_weights()


    # ======================================
    # DISPLAY RESULTS
    # ======================================

    print("\n" + "=" * 55)
    print("FINWISE AI - PERSONALIZED PORTFOLIO")
    print("=" * 55)

    print("\nRecommended Asset Allocation:\n")

    for ticker, weight in cleaned_weights.items():

        if weight > 0:
            print(f"{ticker}: {weight:.2%}")


    # --------------------------------------
    # Portfolio Performance
    # --------------------------------------

    expected_return, volatility, sharpe_ratio = (
        ef.portfolio_performance()
    )

    print("\nPortfolio Performance:")
    print("-" * 35)

    print(f"Expected Annual Return: {expected_return:.2%}")
    print(f"Annual Volatility: {volatility:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")


    # ======================================
    # ASSET CLASS ALLOCATION
    # ======================================

    equity_weight = sum(
        cleaned_weights.get(asset, 0)
        for asset in selected_equities
    )

    bond_weight = sum(
        cleaned_weights.get(asset, 0)
        for asset in selected_bonds
    )

    alternative_weight = sum(
        cleaned_weights.get(asset, 0)
        for asset in ALTERNATIVE_ASSETS
    )

    print("\nAsset Class Allocation:")
    print("-" * 35)

    print(f"Equities: {equity_weight:.2%}")
    print(f"Bonds: {bond_weight:.2%}")
    print(f"Alternatives: {alternative_weight:.2%}")


    # --------------------------------------
    # Disclaimer
    # --------------------------------------

    print("\nDisclaimer:")
    print(
        "Portfolio estimates are based on historical market data "
        "and do not guarantee future performance."
    )


    # --------------------------------------
    # Return results
    # --------------------------------------

    return (
        cleaned_weights,
        expected_return,
        volatility,
        sharpe_ratio
    )


# ==========================================
# TEST THE OPTIMIZER
# ==========================================

if __name__ == "__main__":

    profile = "Aggressive 🔴"

    get_portfolio(profile)