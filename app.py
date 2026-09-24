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
# ===================  1. THEME / CSS  =======================
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: #05060a;
        color: #e6e6f0;
        position: relative;
        overflow-x: hidden;
    }

    /* ---- Animated glowing rays (layer 1) ---- */
    .stApp::before {
        content: "";
        position: fixed;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(
            from 0deg at 50% 50%,
            transparent 0deg,
            rgba(139, 92, 246, 0.18) 40deg,
            transparent 90deg,
            rgba(236, 72, 153, 0.18) 150deg,
            transparent 200deg,
            rgba(56, 189, 248, 0.18) 260deg,
            transparent 320deg,
            transparent 360deg
        );
        animation: rotateRays 25s linear infinite;
        z-index: 0;
        pointer-events: none;
        filter: blur(60px);
    }

    /* ---- Animated glowing rays (layer 2) ---- */
    .stApp::after {
        content: "";
        position: fixed;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(
            from 180deg at 50% 50%,
            transparent 0deg,
            rgba(99, 102, 241, 0.15) 60deg,
            transparent 120deg,
            rgba(217, 70, 239, 0.15) 200deg,
            transparent 280deg,
            transparent 360deg
        );
        animation: rotateRaysReverse 35s linear infinite;
        z-index: 0;
        pointer-events: none;
        filter: blur(80px);
    }

    @keyframes rotateRays        { from { transform: rotate(0deg);   } to { transform: rotate(360deg); } }
    @keyframes rotateRaysReverse { from { transform: rotate(360deg); } to { transform: rotate(0deg);   } }

    /* ---- Glass content card ---- */
    .block-container {
        position: relative;
        z-index: 2;
        background: rgba(15, 15, 25, 0.55);
        backdrop-filter: blur(20px) saturate(140%);
        -webkit-backdrop-filter: blur(20px) saturate(140%);
        border-radius: 24px;
        padding: 2.5rem 2.5rem 3rem 2.5rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        max-width: 820px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow:
            0 0 0 1px rgba(255,255,255,0.03),
            0 20px 60px rgba(0, 0, 0, 0.6),
            0 0 100px rgba(139, 92, 246, 0.15);
    }

    h1 {
        font-weight: 800 !important;
        text-align: center;
        font-size: 2.6rem !important;
        letter-spacing: -0.02em;
        background: linear-gradient(120deg, #a78bfa, #f472b6, #38bdf8);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shine 6s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }

    h2, h3 { color: #ffffff !important; font-weight: 700 !important; }

    p, label, .stMarkdown, .stCaption, [data-testid="stCaptionContainer"] {
        color: #c9c9d6 !important;
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #8b5cf6, #ec4899, #38bdf8);
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.6);
    }
    .stProgress > div > div > div { background: rgba(255,255,255,0.06); }

    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        color: #fff;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 1.5rem;
        font-weight: 600;
        transition: all 0.25s ease;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.35);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(236, 72, 153, 0.55);
        color: #fff;
    }
    .stButton > button:focus { color: #fff !important; border: none !important; }

    .stRadio > div {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
        transition: all 0.2s ease;
    }
    .stRadio > div:hover {
        border: 1px solid rgba(139, 92, 246, 0.6);
        box-shadow: 0 0 24px rgba(139, 92, 246, 0.25);
        background: rgba(139, 92, 246, 0.06);
    }

    [data-testid="stCameraInput"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }

    .stTable, table {
        border-radius: 14px !important;
        overflow: hidden;
        background: rgba(20, 20, 32, 0.9) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }
    thead tr th {
        background: linear-gradient(135deg, #8b5cf6, #ec4899) !important;
        color: #fff !important;
        font-weight: 600 !important;
        text-align: center !important;
        border: none !important;
    }
    tbody tr td {
        text-align: center !important;
        color: #e6e6f0 !important;
        border-color: rgba(255,255,255,0.05) !important;
    }
    tbody tr:nth-child(even) { background: rgba(255,255,255,0.02) !important; }

    .stAlert {
        border-radius: 14px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.08);
    }

    img { border-radius: 14px; }

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }

    .stMarkdown strong { color: #f472b6; font-weight: 700; }

    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0a0b12; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(#8b5cf6, #ec4899); border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# ===================  2. ACTUAL APP CONTENT  ================
# ============================================================

# ---------- Hero ----------
st.title("🧴 Glow")
st.markdown(
    "<p style='text-align:center;color:#a1a1b5;font-size:1.05rem;margin-top:-0.6rem;'>"
    "Discover your perfect skincare routine in 3 simple steps.</p>",
    unsafe_allow_html=True,
)

# -------- Load dataset safely --------
@st.cache_data
def load_data():
    df = pd.read_excel("skin_products.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

try:
    df = load_data()
except Exception:
    st.error("❌ skin_products.xlsx not found or cannot be read")
    st.stop()

# -------- Functions --------
def get_brightness(img):
    img = img.convert("L")
    return ImageStat.Stat(img).mean[0]

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

# -------- Progress bar --------
progress = {1: 33, 2: 66, 3: 100}[st.session_state.step]
st.progress(progress, text=f"Step {st.session_state.step} of 3")
st.write("")

# -------- Step 1: Webcam --------
if st.session_state.step == 1:
    st.subheader("📸 Step 1 — Capture your face")
    st.caption("Optional. We'll estimate your skin type from image brightness.")
    img_file = st.camera_input("📷 Capture Image")

    if img_file is not None:
        image = Image.open(img_file)
        st.image(image, caption="Captured Image", use_container_width=True)
        brightness = get_brightness(image)
        st.write(f"🌞 Estimated brightness: **{brightness:.2f}**")
        st.session_state.brightness_skin_type = brightness_to_skin_type(brightness)
        st.success(f"🧴 Predicted skin type: **{st.session_state.brightness_skin_type}**")

    st.write("")
    if st.button("Next → Skin Quiz"):
        st.session_state.step = 2
        st.rerun()

# -------- Step 2: Quiz --------
elif st.session_state.step == 2:
    st.subheader("📝 Step 2 — Skin Quiz")
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
    for ans in [q1, q2, q3, q4, q5, q6, q7, q8]:
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
        if st.button("← Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next → Recommendations"):
            st.session_state.step = 3
            st.rerun()

# -------- Step 3: Recommendation --------
elif st.session_state.step == 3:
    st.subheader("💎 Step 3 — Your Recommendations")

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

    st.success(f"✅ Final skin type: **{final_skin_type}**")

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
            st.markdown("### 🌟 Top Picks For You")
            st.table(products.head(5))
        else:
            st.warning("No products found for this skin type.")

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("🔄 Restart"):
            st.session_state.step = 1
            st.session_state.brightness_skin_type = None
            st.session_state.quiz_skin_type = None
            st.rerun()
