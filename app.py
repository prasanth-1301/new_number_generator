
import streamlit as st
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
# GENERATION FUNCTION
# ==========================================

def generate_random_number(input_number, previous=None):

    length = len(input_number)

    if length > len(AVAILABLE_DIGITS):
        return None

    # Generate a new random combination
    # different from the previous output
    while True:

        selected = random.sample(
            AVAILABLE_DIGITS,
            length
        )

        output = "".join(selected)

        if output != previous:
            return output


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

/* Header Styling */
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

/* Result Card */
.result-card {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 24px 16px;
    text-align: center;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    margin-bottom: 12px;
}

.result-card:hover {
    border-color: #38bdf8;
    transform: translateY(-4px);
    box-shadow: 0 20px 30px -10px rgba(56, 189, 248, 0.2);
}

.result-label {
    color: #64748b;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.result-number {
    color: #f8fafc;
    font-size: 36px;
    font-weight: 800;
    font-family: 'SF Mono', 'Fira Code', 'Courier New', monospace;
    letter-spacing: 4px;
    text-shadow: 0 2px 10px rgba(56, 189, 248, 0.3);
}

/* Input Fields */
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

st.markdown(
    """
    <div class="header-box">
        <div class="heading">🔢 Number Generator</div>
        <div class="subtitle">
            Randomized Combination Generator
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


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
# SESSION STATE
# ==========================================

if "result" not in st.session_state:
    st.session_state.result = None

if "last_input" not in st.session_state:
    st.session_state.last_input = ""


# ==========================================
# GENERATION LOGIC
# ==========================================

if generate:

    if not number.isdigit():

        st.session_state.result = None
        st.session_state.last_input = ""

        st.error("Please enter numbers only.")

    elif not 2 <= len(number) <= len(AVAILABLE_DIGITS):

        st.session_state.result = None
        st.session_state.last_input = ""

        st.warning(
            f"Enter between 2 and {len(AVAILABLE_DIGITS)} digits."
        )

    else:

        # Avoid repeating the previous result
        previous = st.session_state.result

        new_result = generate_random_number(
            number,
            previous
        )

        st.session_state.result = new_result
        st.session_state.last_input = number


# ==========================================
# OUTPUT DISPLAY
# ==========================================

if st.session_state.result:

    st.divider()

    st.markdown("### 🎯 Generated Output")

    st.caption(
        f"Based on pattern length for input: "
        f"**{st.session_state.last_input}**"
    )

    result = st.session_state.result

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">
                GENERATED NUMBER
            </div>
            <div class="result-number">
                {result}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "✨ One new random combination on every click."
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
