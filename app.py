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
# ====================  1. GLOBAL THEME  =====================
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ================= DARK BASE + RAYS ================= */
.stApp {
    background: #05060a;
    color: #e6e6f0;
}

/* Rays behind everything */
.stApp::before {
    content: "";
    position: fixed;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(
        from 0deg at 50% 50%,
        transparent 0deg,
        rgba(139, 92, 246, 0.22) 40deg,
        transparent 90deg,
        rgba(236, 72, 153, 0.22) 150deg,
        transparent 200deg,
        rgba(56, 189, 248, 0.22) 260deg,
        transparent 320deg,
        transparent 360deg
    );
    animation: rotateRays 28s linear infinite;
    z-index: -2;
    pointer-events: none;
    filter: blur(80px);
}
.stApp::after {
    content: "";
    position: fixed;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(
        from 180deg at 50% 50%,
        transparent 0deg,
        rgba(99, 102, 241, 0.18) 60deg,
        transparent 120deg,
        rgba(217, 70, 239, 0.18) 200deg,
        transparent 280deg,
        transparent 360deg
    );
    animation: rotateRaysReverse 40s linear infinite;
    z-index: -2;
    pointer-events: none;
    filter: blur(100px);
}
@keyframes rotateRays        { from { transform: rotate(0deg);   } to { transform: rotate(360deg); } }
@keyframes rotateRaysReverse { from { transform: rotate(360deg); } to { transform: rotate(0deg);   } }

/* Content above rays */
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
section.main {
    z-index: 1;
    position: relative;
    background: transparent !important;
}

.block-container {
    position: relative;
    z-index: 1;
    background: rgba(15, 15, 25, 0.55);
    backdrop-filter: blur(22px) saturate(150%);
    -webkit-backdrop-filter: blur(22px) saturate(150%);
    border-radius: 26px;
    padding: 2.8rem 2.6rem 3.2rem 2.6rem;
    margin-top: 2rem;
    margin-bottom: 2rem;
    max-width: 860px;
    border: 1px solid rgba(255, 255, 255, 0.09);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.03),
        0 30px 80px rgba(0, 0, 0, 0.7),
        0 0 120px rgba(139, 92, 246, 0.18);
}

/* ================= HERO ================= */
h1 {
    font-weight: 900 !important;
    text-align: center;
    font-size: 2.9rem !important;
    letter-spacing: -0.03em;
    background: linear-gradient(120deg, #a78bfa, #f472b6, #38bdf8, #a78bfa);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 8s linear infinite;
    margin-bottom: 0.2rem !important;
}
@keyframes shine { to { background-position: 300% center; } }

h2, h3 {
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
}

/* Hero subtitle (custom class) */
.hero-sub {
    text-align: center;
    color: #a1a1b5;
    font-size: 1.05rem;
    margin: -0.4rem 0 1.6rem 0;
    letter-spacing: 0.01em;
}
.hero-badge {
    display: inline-block;
    margin: 0 auto 1rem auto;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #d8b4fe;
    background: rgba(139, 92, 246, 0.12);
    border: 1px solid rgba(139, 92, 246, 0.35);
    box-shadow: 0 0 24px rgba(139, 92, 246, 0.25);
}
.badge-wrap { text-align: center; }

/* ================= INPUTS ================= */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    color: #fff !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    padding: 0.7rem 0.9rem !important;
    transition: all 0.2s ease;
}
.stTextInput > div > div > input:focus {
    border: 1px solid rgba(139, 92, 246, 0.9) !important;
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.22) !important;
}

/* ================= PROGRESS ================= */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #8b5cf6, #ec4899, #38bdf8);
    box-shadow: 0 0 22px rgba(139, 92, 246, 0.7);
    border-radius: 999px;
}
.stProgress > div > div > div {
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
}

/* ================= BUTTONS ================= */
.stButton > button {
    background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
    color: #fff !important;
    border: none;
    border-radius: 14px;
    padding: 0.7rem 1.6rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    transition: all 0.25s ease;
    box-shadow:
        0 4px 20px rgba(139, 92, 246, 0.4),
        inset 0 1px 0 rgba(255,255,255,0.2);
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 10px 34px rgba(236, 72, 153, 0.55),
        inset 0 1px 0 rgba(255,255,255,0.3);
    color: #fff !important;
}
.stButton > button:active { transform: translateY(0); }

/* ================= RADIO CHIPS ================= */
.stRadio > div {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    transition: all 0.2s ease;
}
.stRadio > div:hover {
    border: 1px solid rgba(139, 92, 246, 0.6);
    box-shadow: 0 0 26px rgba(139, 92, 246, 0.28);
    background: rgba(139, 92, 246, 0.06);
}

/* ================= CAMERA — GLOWING BORDER ================= */
[data-testid="stCameraInput"] {
    border-radius: 20px;
    overflow: hidden;
    padding: 6px;
    background: linear-gradient(135deg, #8b5cf6, #ec4899, #38bdf8);
    box-shadow:
        0 0 40px rgba(139, 92, 246, 0.45),
        0 0 80px rgba(236, 72, 153, 0.25);
    animation: pulseGlow 4s ease-in-out infinite;
}
[data-testid="stCameraInput"] > div {
    border-radius: 16px !important;
    overflow: hidden;
    background: #0a0b12;
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 40px rgba(139,92,246,0.45), 0 0 80px rgba(236,72,153,0.25); }
    50%      { box-shadow: 0 0 60px rgba(236,72,153,0.6), 0 0 110px rgba(56,189,248,0.35); }
}

/* Make the camera's "Take Photo" button beautiful */
[data-testid="stCameraInput"] button {
    background: linear-gradient(135deg, #8b5cf6, #ec4899) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.2rem !important;
    box-shadow: 0 4px 18px rgba(139, 92, 246, 0.5) !important;
}

/* ================= IMAGES ================= */
img { border-radius: 16px; }
[data-testid="stImage"] img {
    border-radius: 18px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.08);
}

/* ================= TABLE ================= */
.stTable, table {
    border-radius: 16px !important;
    overflow: hidden;
    background: rgba(20, 20, 32, 0.92) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}
thead tr th {
    background: linear-gradient(135deg, #8b5cf6, #ec4899) !important;
    color: #fff !important;
    font-weight: 700 !important;
    text-align: center !important;
    border: none !important;
    padding: 0.9rem !important;
}
tbody tr td {
    text-align: center !important;
    color: #e6e6f0 !important;
    padding: 0.8rem !important;
    border-color: rgba(255,255,255,0.05) !important;
}
tbody tr:nth-child(even) { background: rgba(255,255,255,0.02) !important; }

/* ================= ALERTS ================= */
.stAlert {
    border-radius: 14px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
}

/* ================= MISC ================= */
p, label, .stMarkdown, .stCaption,
[data-testid="stCaptionContainer"] { color: #c9c9d6 !important; }

.stMarkdown strong { color: #f472b6; font-weight: 700; }

#MainMenu, footer { visibility: hidden; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #0a0b12; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(#8b5cf6, #ec4899);
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# ====================  2. HERO RENDER  ======================
# ============================================================
def render_hero(subtitle: str, badge: str = "✨ AI-POWERED SKINCARE"):
    st.markdown(
        f"<div class='badge-wrap'><span class='hero-badge'>{badge}</span></div>",
        unsafe_allow_html=True,
    )
    st.title("🧴 Glow")
    st.markdown(f"<p class='hero-sub'>{subtitle}</p>", unsafe_allow_html=True)


# ============================================================
# ====================  3. LOGIN GATE  =======================
# ============================================================
VALID_USERS = {
    "admin": "glow123",
    "user":  "1234",
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


def login_page():
    render_hero("Sign in to unlock your personalized routine.", badge="🔐 MEMBERS ONLY")
    st.write("")

    with st.form("login_form", clear_on_submit=False):
        st.markdown("##### 👤 Username")
        username = st.text_input(
            "username", label_visibility="collapsed", placeholder="admin"
        )
        st.markdown("##### 🔒 Password")
        password = st.text_input(
            "password", type="password", label_visibility="collapsed", placeholder="••••••••"
        )
        st.write("")
        submitted = st.form_submit_button("Sign In →")

    if submitted:
        if username in VALID_USERS and VALID_USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

    st.caption("Demo →  `admin` / `glow123`   •   `user` / `1234`")


# ============================================================
# ====================  4. MAIN APP  =========================
# ============================================================
def main_app():

    # -------- Top bar --------
    top_l, top_r = st.columns([3, 1])
    with top_l:
        st.markdown(
            f"<p style='margin:0.4rem 0 0 0;color:#a1a1b5;font-size:0.9rem;'>"
            f"Signed in as <strong>{st.session_state.username}</strong></p>",
            unsafe_allow_html=True,
        )
    with top_r:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.step = 1
            st.session_state.brightness_skin_type = None
            st.session_state.quiz_skin_type = None
            st.rerun()

    render_hero("Three quick steps. One perfect routine.", badge="✨ AI-POWERED SKINCARE")

    # -------- Data --------
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

    def get_brightness(img):
        return ImageStat.Stat(img.convert("L")).mean[0]

    def brightness_to_skin_type(b):
        return "dry" if b < 90 else ("normal" if b < 160 else "oily")

    # -------- State --------
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "brightness_skin_type" not in st.session_state:
        st.session_state.brightness_skin_type = None
    if "quiz_skin_type" not in st.session_state:
        st.session_state.quiz_skin_type = None

    # -------- Progress --------
    progress = {1: 33, 2: 66, 3: 100}[st.session_state.step]
    st.progress(progress, text=f"Step {st.session_state.step} of 3")
    st.write("")

    # ================= STEP 1 =================
    if st.session_state.step == 1:
        st.markdown("### 📸 Step 1 — Face Capture")
        st.caption("Optional. Our AI estimates skin type from image brightness.")

        # Nice tip chip
        st.markdown(
            "<div style='padding:0.7rem 1rem;border-radius:14px;"
            "background:rgba(139,92,246,0.08);border:1px solid rgba(139,92,246,0.25);"
            "color:#c9c9d6;font-size:0.9rem;margin-bottom:1rem;'>"
            "💡 <strong>Tip:</strong> Face a soft light source for the best result."
            "</div>",
            unsafe_allow_html=True,
        )

        img_file = st.camera_input("📷 Take a photo")

        if img_file is not None:
            image = Image.open(img_file)
            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(image, caption="Captured", use_container_width=True)
            with col2:
                brightness = get_brightness(image)
                st.metric("🌞 Brightness", f"{brightness:.1f}")
                st.session_state.brightness_skin_type = brightness_to_skin_type(brightness)
                st.metric("🧴 Predicted Type", st.session_state.brightness_skin_type.upper())

        st.write("")
        if st.button("Next → Skin Quiz"):
            st.session_state.step = 2
            st.rerun()

    # ================= STEP 2 =================
    elif st.session_state.step == 2:
        st.markdown("### 📝 Step 2 — Skin Quiz")
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

        st.session_state.quiz_skin_type = (
            "dry" if score <= 10 else ("normal" if score <= 16 else "oily")
        )

        st.success(f"🧴 Quiz-based skin type: **{st.session_state.quiz_skin_type.upper()}**")

        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Back"):
                st.session_state.step = 1
                st.rerun()
        with c2:
            if st.button("Next → Recommendations"):
                st.session_state.step = 3
                st.rerun()

    # ================= STEP 3 =================
    elif st.session_state.step == 3:
        st.markdown("### 💎 Step 3 — Your Recommendations")

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

        st.success(f"✅ Final skin type: **{final_skin_type.upper()}**")

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
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Back"):
                st.session_state.step = 2
                st.rerun()
        with c2:
            if st.button("🔄 Restart"):
                st.session_state.step = 1
                st.session_state.brightness_skin_type = None
                st.session_state.quiz_skin_type = None
                st.rerun()


# ============================================================
# ====================  5. ROUTER  ===========================
# ============================================================
if st.session_state.logged_in:
    main_app()
else:
    login_page()
