
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
# FIXED COLOUR FOR EACH DIGIT
# ==========================================

DIGIT_COLORS = {
    "0": "#A855F7",
    "1": "#3B82F6",
    "2": "#EF4444",
    "3": "#22C55E",
    "4": "#F59E0B",
    "5": "#EC4899",
    "6": "#06B6D4",
    "7": "#F97316",
    "8": "#A3E635",
    "9": "#E879F9"
}


# ==========================================
# RANDOM NUMBER GENERATION
# EXACTLY ONE DIGIT REPEATS TWICE
# ==========================================

def generate_random_number(input_number):

    length = len(input_number)

    while True:

        # Select length - 1 unique digits
        unique_digits = random.sample(
            "0123456789",
            length - 1
        )

        # Select exactly one digit to repeat
        repeated_digit = random.choice(unique_digits)

        # Create the number with exactly one pair
        digits = unique_digits.copy()
        digits.append(repeated_digit)

        # Randomly mix all digits
        random.shuffle(digits)

        result = "".join(digits)

        # Validate exactly one repeated digit
        if sum(
            result.count(digit) == 2
            for digit in set(result)
        ) != 1:
            continue

        # All other digits must appear once
        if any(result.count(digit) > 2 for digit in set(result)):
            continue

        # No consecutive identical digits
        if any(
            result[i] == result[i + 1]
            for i in range(length - 1)
        ):
            continue

        # First and last digits must be different
        if result[0] == result[-1]:
            continue

        return result


# ==========================================
# GENERATE POSSIBILITIES
# ==========================================

def generate_possibilities(input_number):

    length = len(input_number)

    if length == 8:
        count = 3

    elif length in (5, 6):
        count = 2

    else:
        count = 2

    possibilities = set()

    while len(possibilities) < count:

        result = generate_random_number(input_number)

        possibilities.add(result)

    return list(possibilities)


# ==========================================
# CUSTOM UI / STYLES
# ==========================================

st.markdown("""
<style>

.block-container {
    max-width: 680px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

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
}

div[data-baseweb="input"] {
    border-radius: 12px !important;
}

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
    placeholder="e.g. 15634",
    max_chars=20
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

    elif len(number) < 3 or len(number) > 10:

        st.session_state.result = None

        st.warning(
            "Please enter between 3 and 10 digits."
        )

    else:

        # Generate a fresh set when input changes
        if (
            number != st.session_state.last_input
            or not st.session_state.possibilities
        ):

            st.session_state.possibilities = (
                generate_possibilities(number)
            )

            st.session_state.current_index = 0
            st.session_state.last_input = number

        else:

            # Alternate through the same possibilities
            st.session_state.current_index = (
                (st.session_state.current_index + 1)
                % len(st.session_state.possibilities)
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

    # Fixed colour for every digit
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
    gap: 8px;
    flex-wrap: wrap;
    font-family: monospace;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 2px;
}}

@media (max-width: 400px) {{
    .result-number {{
        font-size: 30px;
        gap: 5px;
    }}
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
        "✨ One repeated digit. All other digits unique."
    )


# ==========================================
# DIGIT COLOUR MAPPING
# ==========================================

with st.expander("🎨 View Digit Colour Mapping"):

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
# GENERATION INFORMATION
# ==========================================

with st.expander("View Generation Rules"):

    st.write("""
    - Exactly one digit repeats twice.
    - All remaining digits are unique.
    - No digit repeats more than twice.
    - No consecutive identical digits.
    - First and last digits must differ.
    - Digits are randomly mixed.
    - Only one output appears at a time.
    - Possibilities alternate on every click.
    """)

    st.write("**Available digits:**")

    st.info("0, 1, 2, 3, 4, 5, 6, 7, 8, 9")
