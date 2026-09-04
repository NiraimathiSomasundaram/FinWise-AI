import streamlit as st
import pandas as pd

# IMPORTANT:
# Your portfolio_optimizer.py contains:
# def get_portfolio(profile):
from portfolio_optimizer import get_portfolio


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FinWise AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0E1117;
    color: #FFFFFF;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* Main container */
.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}


/* Titles */
.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #AAB2C8;
    margin-bottom: 40px;
}


/* Metric cards */
.metric-card {
    background: #1B2230;
    border: 1px solid #2E3A50;
    border-radius: 16px;
    padding: 25px;
    text-align: center;
}

.metric-title {
    font-size: 14px;
    color: #9AA4B2;
    font-weight: 600;
    letter-spacing: 1px;
}

.metric-value {
    font-size: 34px;
    font-weight: 800;
    margin-top: 10px;
}


/* Question card */
.question-card {
    background: #161B25;
    border: 1px solid #293244;
    border-radius: 18px;
    padding: 30px;
    margin-top: 25px;
}


/* Profile card */
.profile-card {
    background: #1B2230;
    border: 1px solid #2E3A50;
    border-radius: 18px;
    padding: 30px;
    margin-top: 30px;
}


/* Portfolio card */
.portfolio-card {
    background: #161B25;
    border: 1px solid #293244;
    border-radius: 16px;
    padding: 20px;
}


/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-size: 16px;
    font-weight: 600;
}


/* Divider */
hr {
    border-color: #293244;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "login"

if "name" not in st.session_state:
    st.session_state.name = ""

if "email" not in st.session_state:
    st.session_state.email = ""

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "risk_score" not in st.session_state:
    st.session_state.risk_score = 0

if "profile" not in st.session_state:
    st.session_state.profile = ""

if "portfolio_generated" not in st.session_state:
    st.session_state.portfolio_generated = False


# ============================================================
# RISK ASSESSMENT QUESTIONS
# ============================================================

questions = [

    {
        "icon": "⏳",
        "question": "What is your investment time horizon?",
        "options": [
            "Less than 2 years",
            "2 to 5 years",
            "5 to 10 years",
            "More than 10 years"
        ]
    },

    {
        "icon": "📉",
        "question": "If your portfolio drops by 20%, what would you do?",
        "options": [
            "Sell immediately to avoid further losses",
            "Wait and observe",
            "Hold my investments",
            "Invest more because prices are lower"
        ]
    },

    {
        "icon": "🎯",
        "question": "What is your primary investment goal?",
        "options": [
            "Protect my money",
            "Generate stable returns",
            "Balance growth and safety",
            "Maximize long-term growth"
        ]
    },

    {
        "icon": "⚡",
        "question": "How comfortable are you with investment risk?",
        "options": [
            "Not comfortable",
            "Slightly comfortable",
            "Comfortable",
            "Very comfortable"
        ]
    },

    {
        "icon": "📊",
        "question": "What is your investment experience level?",
        "options": [
            "Beginner",
            "Some experience",
            "Experienced",
            "Highly experienced"
        ]
    }

]


# ============================================================
# FUNCTION: DETERMINE INVESTOR PROFILE
# ============================================================

def determine_profile(score):

    if score <= 8:
        return "Conservative 🟢"

    elif score <= 14:
        return "Moderate 🟡"

    else:
        return "Aggressive 🔴"


# ============================================================
# FUNCTION: PROFILE DESCRIPTION
# ============================================================

def get_profile_description(profile):

    if "Conservative" in profile:

        return (
            "You prefer capital preservation and lower volatility. "
            "Your portfolio will focus more on bonds and stable investments."
        )

    elif "Moderate" in profile:

        return (
            "You are looking for a balance between growth and stability. "
            "Your portfolio will combine equities, bonds, and alternative assets."
        )

    else:

        return (
            "You are comfortable with higher market risk in pursuit of long-term growth. "
            "Your portfolio will have a stronger focus on growth-oriented equities."
        )


# ============================================================
# LOGIN PAGE
# ============================================================

if st.session_state.page == "login":

    st.markdown(
        '<div class="main-title">📈 FinWise AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-Powered Personalized Portfolio Advisor</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("👋 Welcome")

        st.write(
            "Let's understand your investment preferences and create "
            "a personalized portfolio recommendation."
        )

        st.write("")

        name = st.text_input(
            "Your Name",
            placeholder="Enter your name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        st.write("")

        if st.button("🚀 Start Risk Assessment"):

            if name.strip() == "":
                st.warning("⚠️ Please enter your name.")

            elif email.strip() == "":
                st.warning("⚠️ Please enter your email address.")

            else:

                st.session_state.name = name
                st.session_state.email = email
                st.session_state.page = "assessment"

                st.rerun()


# ============================================================
# RISK ASSESSMENT PAGE
# ============================================================

elif st.session_state.page == "assessment":

    current = st.session_state.current_question
    total_questions = len(questions)

    question_data = questions[current]

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="main-title">🧠 Risk Assessment</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Let us understand your investment preferences</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # PROGRESS BAR
    # --------------------------------------------------------

    progress = current / total_questions

    st.progress(progress)

    st.markdown(
        f"""
        <div style="
            text-align:center;
            color:#8B5CF6;
            font-weight:700;
            margin-top:10px;
        ">
            QUESTION {current + 1} OF {total_questions}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="question-card">
            <h2>{question_data["icon"]} {question_data["question"]}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # RADIO BUTTON
    # --------------------------------------------------------

    selected_option = st.radio(
        "Select your answer:",
        question_data["options"],
        index=None,
        key=f"question_{current}"
    )

    st.write("")

    # --------------------------------------------------------
    # BUTTONS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if current > 0:

            if st.button("← Previous"):

                st.session_state.current_question -= 1

                # Remove the previous answer
                if len(st.session_state.answers) > st.session_state.current_question:
                    st.session_state.answers.pop()

                st.rerun()

    with col2:

        button_text = (
            "Generate My Investor Profile →"
            if current == total_questions - 1
            else
            "Next Question →"
        )

        if st.button(button_text):

            # IMPORTANT FIX
            # Do NOT use .index() when selected_option is None

            if selected_option is None:

                st.warning(
                    "⚠️ Please select an answer before continuing."
                )

            else:

                # Get score from option position
                score = question_data["options"].index(
                    selected_option
                ) + 1

                # Save answer
                st.session_state.answers.append(score)

                # ------------------------------------------------
                # LAST QUESTION
                # ------------------------------------------------

                if current == total_questions - 1:

                    total_score = sum(
                        st.session_state.answers
                    )

                    profile = determine_profile(
                        total_score
                    )

                    st.session_state.risk_score = total_score
                    st.session_state.profile = profile
                    st.session_state.page = "profile"

                    st.rerun()

                # ------------------------------------------------
                # NEXT QUESTION
                # ------------------------------------------------

                else:

                    st.session_state.current_question += 1

                    st.rerun()


# ============================================================
# INVESTOR PROFILE PAGE
# ============================================================

elif st.session_state.page == "profile":

    risk_score = st.session_state.risk_score
    profile = st.session_state.profile

    description = get_profile_description(profile)

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    st.markdown(
        '<div class="main-title">🎯 Your Investor Profile</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            label="RISK SCORE",
            value=f"{risk_score}/20"
        )

    with col2:

        st.metric(
            label="INVESTOR PROFILE",
            value=profile
        )

    st.write("")
    st.divider()

    # --------------------------------------------------------
    # PROFILE DESCRIPTION
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="profile-card">
            <h2>{profile}</h2>
            <p style="font-size:18px; color:#D1D5DB;">
                {description}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    # --------------------------------------------------------
    # GENERATE BUTTON
    # --------------------------------------------------------

    if st.button(
        "📈 Generate My Personalized Portfolio"
    ):

        st.session_state.page = "portfolio"

        st.rerun()


# ============================================================
# PORTFOLIO PAGE
# ============================================================

elif st.session_state.page == "portfolio":

    st.markdown(
        '<div class="main-title">📈 Your Personalized Portfolio</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="subtitle">
            Personalized recommendation for {st.session_state.name}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # LOAD PORTFOLIO
    # --------------------------------------------------------

    if not st.session_state.portfolio_generated:

        with st.spinner(
            "🤖 FinWise AI is analyzing market data and optimizing your portfolio..."
        ):

            # IMPORTANT:
            # Your function is get_portfolio()
            result = get_portfolio(
                st.session_state.profile
            )

            # Your get_portfolio() returns FOUR values:
            #
            # cleaned_weights
            # expected_return
            # volatility
            # sharpe_ratio

            (
                weights,
                expected_return,
                volatility,
                sharpe_ratio
            ) = result

            st.session_state.weights = weights
            st.session_state.expected_return = expected_return
            st.session_state.volatility = volatility
            st.session_state.sharpe_ratio = sharpe_ratio

            st.session_state.portfolio_generated = True

    # --------------------------------------------------------
    # GET SAVED RESULTS
    # --------------------------------------------------------

    weights = st.session_state.weights
    expected_return = st.session_state.expected_return
    volatility = st.session_state.volatility
    sharpe_ratio = st.session_state.sharpe_ratio

    # --------------------------------------------------------
    # FILTER ZERO WEIGHTS
    # --------------------------------------------------------

    active_weights = {
        ticker: weight
        for ticker, weight in weights.items()
        if weight > 0
    }

    # --------------------------------------------------------
    # PORTFOLIO METRICS
    # --------------------------------------------------------

    st.subheader("📊 Portfolio Performance")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Expected Annual Return",
            f"{expected_return:.2%}"
        )

    with col2:

        st.metric(
            "Annual Volatility",
            f"{volatility:.2%}"
        )

    with col3:

        st.metric(
            "Sharpe Ratio",
            f"{sharpe_ratio:.2f}"
        )

    st.write("")
    st.divider()

    # --------------------------------------------------------
    # ASSET ALLOCATION
    # --------------------------------------------------------

    st.subheader("💼 Recommended Asset Allocation")

    allocation_data = pd.DataFrame(
        {
            "Asset": list(active_weights.keys()),
            "Allocation": list(active_weights.values())
        }
    )

    allocation_data["Percentage"] = (
        allocation_data["Allocation"] * 100
    )

    allocation_data = allocation_data.sort_values(
        by="Allocation",
        ascending=False
    )

    col1, col2 = st.columns([1, 1])

    with col1:

        st.dataframe(
            allocation_data[
                ["Asset", "Percentage"]
            ],
            use_container_width=True,
            hide_index=True
        )

    with col2:

        chart_data = allocation_data.set_index(
            "Asset"
        )["Percentage"]

        st.bar_chart(chart_data)

    st.write("")
    st.divider()

    # --------------------------------------------------------
    # ASSET CLASS ALLOCATION
    # --------------------------------------------------------

    st.subheader("🏦 Asset Class Allocation")

    equity_assets = [
        "VTI",
        "SPY",
        "VXUS",
        "XLV",
        "VNQ",
        "QQQ",
        "XLF",
        "XLE"
    ]

    bond_assets = [
        "AGG",
        "TLT"
    ]

    alternative_assets = [
        "GLD"
    ]

    equity_weight = sum(
        active_weights.get(asset, 0)
        for asset in equity_assets
    )

    bond_weight = sum(
        active_weights.get(asset, 0)
        for asset in bond_assets
    )

    alternative_weight = sum(
        active_weights.get(asset, 0)
        for asset in alternative_assets
    )

    asset_class_data = pd.DataFrame(
        {
            "Asset Class": [
                "Equities",
                "Bonds",
                "Alternatives"
            ],
            "Allocation": [
                equity_weight * 100,
                bond_weight * 100,
                alternative_weight * 100
            ]
        }
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Equities",
            f"{equity_weight:.2%}"
        )

    with col2:

        st.metric(
            "Bonds",
            f"{bond_weight:.2%}"
        )

    with col3:

        st.metric(
            "Alternatives",
            f"{alternative_weight:.2%}"
        )

    st.write("")
    st.divider()

    # --------------------------------------------------------
    # INVESTOR SUMMARY
    # --------------------------------------------------------

    st.subheader("🧠 Investor Summary")

    st.info(
        f"""
**Investor:** {st.session_state.name}

**Risk Score:** {st.session_state.risk_score}/20

**Investor Profile:** {st.session_state.profile}

This portfolio has been generated based on your risk profile
and historical market data.
        """
    )

    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    st.warning(
        """
⚠️ **Disclaimer**

This project is for educational and demonstration purposes only.
Portfolio estimates are based on historical market data and
do not guarantee future performance. This does not constitute
financial advice.
        """
    )

    st.write("")

    # --------------------------------------------------------
    # START AGAIN
    # --------------------------------------------------------

    if st.button("🔄 Start New Assessment"):

        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.risk_score = 0
        st.session_state.profile = ""
        st.session_state.portfolio_generated = False

        # Remove previous portfolio data
        for key in [
            "weights",
            "expected_return",
            "volatility",
            "sharpe_ratio"
        ]:

            if key in st.session_state:
                del st.session_state[key]

        st.session_state.page = "assessment"

        st.rerun()