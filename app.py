import streamlit as st
from itertools import product

# Number mapping
NUMBER_MAP = {
    "0": ["3", "9"],
    "1": ["8", "4"],
    "2": ["3", "6"],
    "3": ["4", "8"],
    "4": ["6", "3"],
    "5": ["0", "7"],
    "6": ["2", "1"],
    "7": ["4", "5"],
    "8": ["6", "2"],
    "9": ["2", "0"],
}

# Page Configuration
st.set_page_config(
    page_title="Number Generator",
    page_icon="🔢",
    layout="centered"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    /* Main container padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 680px;
    }
    
    /* Input box styling */
    div[data-baseweb="input"] {
        border-radius: 10px;
    }
    
    /* Custom Card Design for Results */
    .result-card {
        background: linear-gradient(135deg, #2b2c36 0%, #1e1e24 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px 10px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(0,0,0,0.25);
    }

    .result-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #94a3b8;
        margin-bottom: 6px;
        font-weight: 600;
    }

    .result-value {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 2px;
        color: #38bdf8;
        font-family: 'Source Code Pro', monospace;
    }
    </style>
""", unsafe_allow_html=True)

# Title & Header
st.title("🔢 Number Generator")
st.caption("Generate unique digit permutations from standard mapped pairs.")
st.divider()

# Session State Initialization
if "results" not in st.session_state:
    st.session_state.results = []
if "third_index" not in st.session_state:
    st.session_state.third_index = 0
if "last_number" not in st.session_state:
    st.session_state.last_number = ""

# Input Form Area
with st.container():
    number = st.text_input(
        "Enter Number",
        placeholder="e.g. 156",
        max_chars=4,
        help="Enter any 2, 3, or 4 digit sequence."
    ).strip()

    generate_btn = st.button("✨ GENERATE", use_container_width=True, type="primary")

# Generation Logic
if generate_btn:
    if not number.isdigit():
        st.error("⚠️ Invalid input: Please enter numbers only.", icon="🚨")
    elif len(number) not in [2, 3, 4]:
        st.warning("⚠️ Length error: Input must be exactly 2, 3, or 4 digits.", icon="📏")
    else:
        # Get possible values for each digit
        possibilities = [NUMBER_MAP[digit] for digit in number]

        # Generate all combinations
        combinations = ["".join(c) for c in product(*possibilities)]

        # Remove duplicates while preserving order
        combinations = list(dict.fromkeys(combinations))

        if len(combinations) < 3:
            st.error("Not enough combinations generated to build a 3-result set.")
        else:
            first = combinations[0]
            second = combinations[1]
            remaining = combinations[2:]

            # Reset index if the input changed
            if st.session_state.last_number != number:
                st.session_state.third_index = 0
                st.session_state.last_number = number
            else:
                st.session_state.third_index = (st.session_state.third_index + 1) % len(remaining)

            third = remaining[st.session_state.third_index]

            st.session_state.results = [first, second, third]
            st.session_state.total_remaining = len(remaining)

# Results Display Section
if st.session_state.results:
    st.write("")
    
    # Rotation counter indicator
    if "total_remaining" in st.session_state:
        current_step = st.session_state.third_index + 1
        total_steps = st.session_state.total_remaining
        st.caption(f"🔄 Rotating combination **{current_step} of {total_steps}** for item #3")

    # Column Grid Display
    cols = st.columns(3)
    labels = ["Fixed #1", "Fixed #2", "Rotated #3"]

    for idx, (col, res, label) in enumerate(zip(cols, st.session_state.results, labels)):
        with col:
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-label">{label}</div>
                    <div class="result-value">{res}</div>
                </div>
                """,
                unsafe_allow_html=True
            )