# -----------------------------------
# FINWISE AI - RISK ASSESSMENT
# -----------------------------------

def ask_question(question, options):
    """
    Displays a question with options
    and returns the selected score.
    """

    print("\n" + question)

    for number, (option, score) in enumerate(options, start=1):
        print(f"{number}. {option}")

    while True:
        try:
            choice = int(input("\nEnter your choice: "))

            if 1 <= choice <= len(options):
                return options[choice - 1][1]

            else:
                print("Please enter a valid option.")

        except ValueError:
            print("Please enter a number.")


def assess_risk():
    """
    Calculates the user's investment risk profile.
    """

    print("\n" + "=" * 50)
    print("WELCOME TO FINWISE AI - RISK ASSESSMENT")
    print("=" * 50)

    total_score = 0

    # -----------------------------------
    # Question 1: Investment Horizon
    # -----------------------------------

    total_score += ask_question(
        "1. What is your investment time horizon?",
        [
            ("Less than 2 years", 1),
            ("2 to 5 years", 2),
            ("5 to 10 years", 3),
            ("More than 10 years", 4)
        ]
    )

    # -----------------------------------
    # Question 2: Market Loss Reaction
    # -----------------------------------

    total_score += ask_question(
        "2. If your portfolio drops by 20%, what would you do?",
        [
            ("Sell immediately to avoid further losses", 1),
            ("Wait and observe", 2),
            ("Hold my investments", 3),
            ("Invest more because prices are lower", 4)
        ]
    )

    # -----------------------------------
    # Question 3: Primary Goal
    # -----------------------------------

    total_score += ask_question(
        "3. What is your primary investment goal?",
        [
            ("Protect my money", 1),
            ("Generate stable returns", 2),
            ("Balance growth and safety", 3),
            ("Maximize long-term growth", 4)
        ]
    )

    # -----------------------------------
    # Question 4: Risk Comfort
    # -----------------------------------

    total_score += ask_question(
        "4. How comfortable are you with investment risk?",
        [
            ("Not comfortable", 1),
            ("Slightly comfortable", 2),
            ("Comfortable", 3),
            ("Very comfortable", 4)
        ]
    )

    # -----------------------------------
    # Question 5: Investment Experience
    # -----------------------------------

    total_score += ask_question(
        "5. What is your investment experience level?",
        [
            ("Beginner", 1),
            ("Some experience", 2),
            ("Experienced", 3),
            ("Highly experienced", 4)
        ]
    )

    # -----------------------------------
    # Determine Risk Profile
    # -----------------------------------

    if total_score <= 8:
        profile = "Conservative 🟢"

    elif total_score <= 14:
        profile = "Moderate 🟡"

    else:
        profile = "Aggressive 🔴"

    # -----------------------------------
    # Display Results
    # -----------------------------------

    print("\n" + "=" * 50)
    print("RISK ASSESSMENT RESULT")
    print("=" * 50)

    print(f"\nYour Risk Score: {total_score}/20")
    print(f"Your Investor Profile: {profile}")

    return total_score, profile


# -----------------------------------
# Run the assessment
# -----------------------------------

if __name__ == "__main__":
    assess_risk()