import streamlit as st
import pandas as pd
from PIL import Image, ImageStat

st.set_page_config(
    page_title="Glow • Skin Care Recommender",
    page_icon="🧴",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# ----------  CUSTOM THEME (Glassmorphism + Gradient)  -------
# ============================================================
st.markdown("""
<style>
    /* ---------- Import a nice font ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* ---------- Animated gradient background ---------- */
    .stApp {
        background: linear-gradient(-45deg, #fce4ec, #e1bee7, #b3e5fc, #c8e6c9);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ---------- Glass card effect for main block ---------- */
    .block-container {
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 24px;
        padding: 2.5rem 2.5rem 3rem 2.5rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.5);
        max-width: 800px;
    }

    /* ---------- Title styling ---------- */
    h1 {
        background: linear-gradient(90deg, #ec407a, #ab47bc, #42a5f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
        text-align: center;
        font-size: 2.4rem !important;
    }

    h2, h3 {
        color: #6a1b9a;
        font-weight: 600 !important;
    }

    /* ---------- Subheader ---------- */
    .stMarkdown p {
        color: #444;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        background: linear-gradient(90deg, #ec407a, #ab47bc);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.6rem 1.6rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(236, 64, 122, 0.35);
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(171, 71, 188, 0.5);
        background: linear-gradient(90deg, #ab47bc, #ec407a);
        color: white;
    }

    /* ---------- Radio buttons ---------- */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        border: 1px solid rgba(171, 71, 188, 0.15);
        transition: all 0.2s ease;
    }

    .stRadio > div:hover {
        border: 1px solid rgba(171, 71, 188, 0.4);
        box-shadow: 0 2px 10px rgba(171, 71, 188, 0.15);
    }

    /* ---------- Table ---------- */
    .stTable, table {
        border-radius: 14px !important;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.85) !important;
    }

    thead tr th {
        background: linear-gradient(90deg, #ec407a, #ab47bc) !important;
        color: white !important;
        font-weight: 600 !important;
        text-align: center !important;
    }

    tbody tr td {
        text-align: center !important;
        color: #333 !important;
    }

    /* ---------- Camera input ---------- */
    [data-testid="stCameraInput"] {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }

    /* ---------- Alerts (success / warning / error) ---------- */
    .stAlert {
        border-radius: 14px;
        backdrop-filter: blur(6px);
    }

    /* ---------- Metric text ---------- */
    .stMarkdown strong {
        color: #ad1457;
    }
</style>
""", unsafe_allow_html=True)
# ============================================================


# ---------- Hero title ----------
st.title("🧴 Glow — Skin Care Recommender")
st.write("✨ *Discover your perfect skincare routine in 3 simple steps.*")

# -------- Load dataset safely --------
@st.cache_data
def load_data():
    df = pd.read_excel("skin_products.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

try:
    df = load_data()
except Exception as e:
    st.error("❌ skin_products.xlsx not found or cannot be read")
    st.stop()

# -------- Functions --------
def get_brightness(img):
    img = img.convert("L")
    stat = ImageStat.Stat(img)
    return stat.mean[0]

def brightness_to_skin_type(brightness):
    if brightness < 90:
        return "dry"
    elif brightness < 160:
        return "normal"
    else:
        return "oily"

# -------- Session State --------
if "step" not in st.session_state:
    st.session_state.step = 1
if "brightness_skin_type" not in st.session_state:
    st.session_state.brightness_skin_type = None
if "quiz_skin_type" not in st.session_state:
    st.session_state.quiz_skin_type = None

# -------- Progress bar ----------
progress = {1: 33, 2: 66, 3: 100}[st.session_state.step]
st.progress(progress, text=f"Step {st.session_state.step} of 3")

# -------- Step 1: Webcam --------
if st.session_state.step == 1:
    st.subheader("📸 Step 1: Capture your face (Optional)")
    st.caption("We'll estimate your skin type from image brightness. You can skip this.")
    img_file = st.camera_input("📷 Capture Image")

    if img_file is not None:
        image = Image.open(img_file)
        st.image(image, caption="Captured Image", use_container_width=True)
        brightness = get_brightness(image)
        st.write(f"🌞 Estimated brightness: **{brightness:.2f}**")
        st.session_state.brightness_skin_type = brightness_to_skin_type(brightness)
        st.success(f"🧴 Predicted skin type: **{st.session_state.brightness_skin_type}**")

    st.write("")
    if st.button("Next: Skin Quiz ➡️"):
        st.session_state.step = 2
        st.rerun()

# -------- Step 2: Quiz --------
elif st.session_state.step == 2:
    st.subheader("📝 Step 2: Take a detailed skin quiz (Optional)")
    st.caption("Answer 8 quick questions for a more accurate result.")

    q1 = st.radio("How does your skin feel after washing your face?",
                  ["Tight or dry", "Comfortable", "Oily/shiny"])
    q2 = st.radio("How often does your skin get oily during the day?",
                  ["Rarely", "Sometimes", "Often"])
    q3 = st.radio("Do you have visible pores?",
                  ["Small/Invisible", "Medium", "Large"])
    q4 = st.radio("How often do you get dry patches?",
                  ["Rarely", "Sometimes", "Often"])
    q5 = st.radio("Does your skin feel greasy by midday?",
                  ["Never", "Sometimes", "Always"])
    q6 = st.radio("How sensitive is your skin?",
                  ["Very sensitive", "Slightly sensitive", "Not sensitive"])
    q7 = st.radio("How prone is your skin to acne or breakouts?",
                  ["Rarely", "Sometimes", "Often"])
    q8 = st.radio("How visible are fine lines or wrinkles?",
                  ["Very visible", "Slightly visible", "Not visible"])

    score = 0
    answers = [q1, q2, q3, q4, q5, q6, q7, q8]

    for ans in answers:
        if ans in ["Tight or dry", "Rarely", "Small/Invisible",
                   "Never", "Very sensitive", "Very visible"]:
            score += 1
        elif ans in ["Comfortable", "Sometimes", "Medium",
                     "Slightly sensitive", "Slightly visible"]:
            score += 2
        else:
            score += 3

    if score <= 10:
        st.session_state.quiz_skin_type = "dry"
    elif score <= 16:
        st.session_state.quiz_skin_type = "normal"
    else:
        st.session_state.quiz_skin_type = "oily"

    st.success(f"🧴 Quiz-based predicted skin type: **{st.session_state.quiz_skin_type}**")

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next: Recommendations ➡️"):
            st.session_state.step = 3
            st.rerun()

# -------- Step 3: Recommendation --------
elif st.session_state.step == 3:
    st.subheader("💎 Step 3: Your Recommended Products")

    manual_skin_type = st.radio(
        "Or select your skin type manually",
        ["dry", "normal", "oily"],
        horizontal=True,
    )

    final_skin_type = (
        st.session_state.brightness_skin_type
        or st.session_state.quiz_skin_type
        or manual_skin_type
    )

    st.success(f"✅ Final skin type used for recommendations: **{final_skin_type}**")

    skin_col = None
    for col in df.columns:
        if "skin" in col and "type" in col:
            skin_col = col
            break

    if skin_col is None:
        st.error("❌ Skin type column not found in dataset")
    else:
        products = df[df[skin_col].astype(str).str.lower() == final_skin_type]
        if not products.empty:
            st.write("### 🌟 Top Picks For You")
            st.table(products.head(5))
        else:
            st.warning("No products found for this skin type.")

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("🔄 Restart"):
            st.session_state.step = 1
            st.session_state.brightness_skin_type = None
            st.session_state.quiz_skin_type = None
            st.rerun()
