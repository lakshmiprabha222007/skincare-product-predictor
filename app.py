import streamlit as st
import pandas as pd
from PIL import Image, ImageStat
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Skin Care Product Recommender",
    page_icon="💛",
    layout="wide"
)

# --- Colorful Theme Styling ---
st.markdown("""
<style>
body {
    background-color: #fffaf0;
}
.stButton>button {
    background: linear-gradient(90deg, #FFD700, #FFB347);
    color: black;
    font-size: 16px;
    font-weight: bold;
    border-radius: 12px;
    padding: 8px 20px;
    margin-top: 10px;
}
div[data-baseweb="card"] {
    background-color: #fff5e1;
    border: 2px solid #FFD700;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
    transition: transform 0.2s;
}
div[data-baseweb="card"]:hover {
    transform: scale(1.03);
    box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# --- Banner Image ---
try:
    st.image("gold_banner.jpg", use_column_width=True)
except:
    st.warning("Gold-themed banner not found, skipping...")

st.title("💛 Skin Care Product Recommender App")
st.write("Capture your face using webcam to get colorful, personalized skin care recommendations!")

# --- Load Dataset ---
@st.cache_data
def load_data():
    df = pd.read_excel("skin_products.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data()

# --- Functions ---
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

def skin_emoji(skin_type):
    return {"dry":"💧 Dry", "normal":"🌿 Normal", "oily":"💦 Oily"}.get(skin_type, skin_type)

def skin_color(skin_type):
    return {"dry":"#FF6B6B","normal":"#6BCB77","oily":"#4D96FF"}.get(skin_type, "#FFD700")

# --- Session State ---
if "step" not in st.session_state: st.session_state.step = 1
if "brightness_skin_type" not in st.session_state: st.session_state.brightness_skin_type = None
if "quiz_skin_type" not in st.session_state: st.session_state.quiz_skin_type = None

# --- Step Navigation ---
steps = ["📷 Webcam", "📝 Quiz", "🛍️ Products"]
st.markdown(" | ".join([f"**{s}**" if i+1==st.session_state.step else s for i,s in enumerate(steps)]))

# --- Progress Bar with Gradient ---
st.progress(min(st.session_state.step/3.0, 1.0))

# --- Step 1: Webcam (Mandatory) ---
if st.session_state.step == 1:
    st.subheader("Step 1: Capture your face (Mandatory)")

    img_file = st.camera_input("📷 Capture Image")
    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Your Captured Face", use_column_width=True)
        brightness = get_brightness(image)
        st.session_state.brightness_skin_type = brightness_to_skin_type(brightness)
        st.markdown(f"<div style='background-color:{skin_color(st.session_state.brightness_skin_type)}; "
                    f"padding:10px; border-radius:12px; color:white;'>"
                    f"✅ Detected Skin Type: <b>{skin_emoji(st.session_state.brightness_skin_type)}</b></div>",
                    unsafe_allow_html=True)

        if st.button("Next: Skin Quiz"):
            st.session_state.step = 2
    else:
        st.warning("Please capture an image to continue.")

# --- Step 2: Optional Skin Quiz ---
elif st.session_state.step == 2:
    st.subheader("Step 2: Optional Skin Quiz")

    q1 = st.radio("How does your skin feel after washing?", ["Tight or dry","Comfortable","Oily/shiny"])
    q2 = st.radio("How often does your skin get oily?", ["Rarely","Sometimes","Often"])
    q3 = st.radio("Do you have visible pores?", ["Small/Invisible","Medium","Large"])
    q4 = st.radio("How often do you get dry patches?", ["Rarely","Sometimes","Often"])
    q5 = st.radio("Does your skin feel greasy by midday?", ["Never","Sometimes","Always"])
    q6 = st.radio("How sensitive is your skin?", ["Very sensitive","Slightly sensitive","Not sensitive"])
    q7 = st.radio("How prone is your skin to acne or breakouts?", ["Rarely","Sometimes","Often"])
    q8 = st.radio("How visible are fine lines or wrinkles?", ["Very visible","Slightly visible","Not visible"])

    score = 0
    for ans in [q1,q2,q3,q4,q5,q6,q7,q8]:
        if ans in ["Tight or dry","Rarely","Small/Invisible","Never","Very sensitive","Very visible"]:
            score += 1
        elif ans in ["Comfortable","Sometimes","Medium","Slightly sensitive","Slightly visible"]:
            score += 2
        else:
            score += 3

    if score <= 10: st.session_state.quiz_skin_type = "dry"
    elif score <=16: st.session_state.quiz_skin_type = "normal"
    else: st.session_state.quiz_skin_type = "oily"

    st.markdown(f"<div style='background-color:{skin_color(st.session_state.quiz_skin_type)}; padding:10px; border-radius:12px; color:white;'>"
                f"📝 Quiz-based Skin Type: <b>{skin_emoji(st.session_state.quiz_skin_type)}</b></div>",
                unsafe_allow_html=True)

    if st.button("Next: Recommended Products"):
        st.session_state.step = 3

# --- Step 3: Product Recommendations ---
elif st.session_state.step == 3:
    st.subheader("Step 3: Recommended Products")

    final_skin_type = st.session_state.brightness_skin_type or st.session_state.quiz_skin_type

    st.markdown(f"<div style='background-color:{skin_color(final_skin_type)}; padding:15px; border-radius:12px; color:white;'>"
                f"💛 Your Skin Type: <b>{skin_emoji(final_skin_type)}</b></div>", unsafe_allow_html=True)

    skin_col = next((c for c in df.columns if "skin" in c and "type" in c), None)
    if skin_col:
        products = df[df[skin_col].str.lower()==final_skin_type]
        if not products.empty:
            cols = st.columns(2)
            for i, row in enumerate(products.sample(min(5,len(products)))):
                with cols[i%2]:
                    st.markdown(f"**{row['product_name']}**")
                    if "price" in df.columns: st.write(f"💰 {row['price']}")
                    if "description" in df.columns: st.write(f"📝 {row['description']}")
                    if "image_url" in df.columns and pd.notna(r_
