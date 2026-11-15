
import streamlit as st
import streamlit.components.v1 as components
import random

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Number Generator",
    page_icon="🔢",
    layout="centered"
)

# ==========================================
# SOURCE PATTERNS
# ==========================================

SOURCE_NUMBERS = [
    "139", "267",
    "2046", "0958",
    "578", "143"
]

AVAILABLE_DIGITS = sorted(set("".join(SOURCE_NUMBERS)))


# ==========================================
# FIXED COLOUR FOR EACH DIGIT
# ==========================================

DIGIT_COLORS = {
    "0": "#A855F7",  # Purple
    "1": "#3B82F6",  # Blue
    "2": "#EF4444",  # Red
    "3": "#22C55E",  # Green
    "4": "#F59E0B",  # Orange
    "5": "#EC4899",  # Pink
    "6": "#06B6D4",  # Cyan
    "7": "#F97316",  # Orange
    "8": "#A3E635",  # Lime
    "9": "#E879F9"   # Violet
}


# ==========================================
# GENERATION FUNCTION
# ==========================================

def generate_random_number(input_number):

    length = len(input_number)

    selected = random.sample(
        AVAILABLE_DIGITS,
        length
    )

    return "".join(selected)


# ==========================================
# GENERATE ONLY TWO UNIQUE POSSIBILITIES
# ==========================================

def generate_two_possibilities(input_number):

    possibilities = []

    while len(possibilities) < 2:

        result = generate_random_number(input_number)

        if result not in possibilities:
            possibilities.append(result)

    return possibilities


# ==========================================
# CUSTOM UI / STYLES
# ==========================================

st.markdown("""
<style>

/* Main Container */
.block-container {
    max-width: 680px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Header */
.header-box {
    text-align: center;
    padding: 1.5rem 0 1rem 0;
}

.heading {
    font-size: 36px;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}

.subtitle {
    font-size: 14px;
    color: #94a3b8;
    font-weight: 400;
}

/* Input */
div[data-baseweb="input"] {
    border-radius: 12px !important;
}

/* Generate Button */
button[kind="primary"] {
    border-radius: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    background: linear-gradient(
        135deg, #0284c7, #6366f1
    ) !important;
    border: none !important;
    transition: all 0.2s ease !important;
}

button[kind="primary"]:hover {
    opacity: 0.95;
    transform: scale(1.01);
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="header-box">
    <div class="heading">🔢 Number Generator</div>
    <div class="subtitle">
        Randomized Combination Generator
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# SESSION STATE
# ==========================================

if "possibilities" not in st.session_state:
    st.session_state.possibilities = []

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

if "result" not in st.session_state:
    st.session_state.result = None


# ==========================================
# INPUT SECTION
# ==========================================

number = st.text_input(
    "Enter Your Input Number",
    placeholder="e.g. 156",
    max_chars=10
).strip()

generate = st.button(
    "✨ GENERATE NUMBER",
    use_container_width=True,
    type="primary"
)


# ==========================================
# GENERATION LOGIC
# ==========================================

if generate:

    if not number.isdigit():

        st.session_state.result = None
        st.error("Please enter numbers only.")

    elif not 2 <= len(number) <= len(AVAILABLE_DIGITS):

        st.session_state.result = None

        st.warning(
            f"Enter between 2 and {len(AVAILABLE_DIGITS)} digits."
        )

    else:

        # Generate a new pair only when input changes
        if (
            number != st.session_state.last_input
            or not st.session_state.possibilities
        ):

            st.session_state.possibilities = (
                generate_two_possibilities(number)
            )

            st.session_state.current_index = 0
            st.session_state.last_input = number

        else:

            # Alternate between the same two possibilities
            st.session_state.current_index = (
                1 - st.session_state.current_index
            )

        # Display only one possibility
        st.session_state.result = (
            st.session_state.possibilities[
                st.session_state.current_index
            ]
        )


# ==========================================
# OUTPUT DISPLAY
# ==========================================

if st.session_state.result:

    st.divider()

    st.markdown("### 🎯 Generated Output")

    st.caption(
        f"Based on input: **{st.session_state.last_input}**"
    )

    result = st.session_state.result

    # Apply fixed colour to every digit
    colored_digits = "".join(
        f'<span style="color:{DIGIT_COLORS[digit]};">'
        f'{digit}</span>'
        for digit in result
    )

    # Single rectangular output card
    html = f"""
<!DOCTYPE html>
<html>
<head>
<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: Arial, sans-serif;
}}

.result-card {{
    width: 100%;
    background: rgba(30, 41, 59, 0.95);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 32px 15px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.20);
}}

.result-label {{
    color: #94a3b8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 18px;
}}

.result-number {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
    font-family: monospace;
    font-size: 48px;
    font-weight: 800;
    letter-spacing: 4px;
}}

</style>
</head>

<body>

<div class="result-card">

    <div class="result-label">
        GENERATED NUMBER
    </div>

    <div class="result-number">
        {colored_digits}
    </div>

</div>

</body>
</html>
"""

    components.html(
        html,
        height=155,
        scrolling=False
    )

    st.caption(
        "✨ Alternating between your 2 fixed possibilities."
    )


# ==========================================
# DIGIT COLOUR MAPPING
# ==========================================

with st.expander("🎨 View Digit Colour Mapping"):

    st.markdown("### Fixed Colours for Each Digit")

    columns = st.columns(5)

    for index, (digit, color) in enumerate(DIGIT_COLORS.items()):

        with columns[index % 5]:

            st.markdown(
                f"""
                <div style="
                    background:#1e293b;
                    border:1px solid {color};
                    border-radius:12px;
                    padding:12px 5px;
                    text-align:center;
                    margin-bottom:10px;
                ">
                    <div style="
                        font-size:27px;
                        font-weight:800;
                        color:{color};
                    ">{digit}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ==========================================
# SOURCE INFORMATION
# ==========================================

with st.expander("View Source Patterns & Digits"):

    st.write("**Patterns:**")

    st.code(
        "139 → 267\n2046 → 0958\n578 → 143",
        language="text"
    )

    st.write("**Available Digits Set:**")

    st.info(", ".join(AVAILABLE_DIGITS))
