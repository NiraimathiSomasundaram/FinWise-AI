# ==========================================
# FINWISE AI - MAIN APPLICATION
# ==========================================

from risk_assessment import assess_risk
from portfolio_optimizer import get_portfolio


def main():

    print("\n" + "=" * 60)
    print("WELCOME TO FINWISE AI")
    print("AI-POWERED PERSONALIZED PORTFOLIO ADVISOR")
    print("=" * 60)

    # --------------------------------------
    # STEP 1: Risk Assessment
    # --------------------------------------

    score, profile = assess_risk()

    # --------------------------------------
    # STEP 2: Generate Portfolio
    # --------------------------------------

    print("\n" + "=" * 60)
    print("GENERATING YOUR PERSONALIZED PORTFOLIO...")
    print("=" * 60)

    weights, expected_return, volatility, sharpe_ratio = (
        get_portfolio(profile)
    )

    # --------------------------------------
    # Final Summary
    # --------------------------------------

    print("\n" + "=" * 60)
    print("FINWISE AI - FINAL INVESTMENT SUMMARY")
    print("=" * 60)

    print(f"\nRisk Score: {score}/20")
    print(f"Investor Profile: {profile}")

    print("\nYour optimized portfolio has been generated successfully.")

    print("\nKey Portfolio Metrics:")

    print(f"Expected Annual Return: {expected_return:.2%}")
    print(f"Annual Volatility: {volatility:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

    print("\nThank you for using FinWise AI!")

    print("\nIMPORTANT:")
    print(
        "This project is for educational and demonstration purposes only "
        "and does not constitute financial advice."
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    main()