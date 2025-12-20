import streamlit as st
import pandas as pd
from PIL import Image, ImageStat

# --- Page Config ---
st.set_page_config(
    page_title="Skin Care Product Recommender",
    page_icon="🧴",
    layout="wide"
)

# --- Theme / Banner ---
st.image("theme_banner.jpg", use_column_width=True)
st.title("🧴 Skin Care Product Recommendation App")
st.write("Follow the steps to discover your skin type and get personalized product recommendations!")

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
    if brightness < 80:
        return "dry"
    elif brightness < 140:
        return "normal"
    else:
        return "oily"

# --- Session State ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "brightness_skin_type" not in st.session_state:
    st.session_state.brightness_skin_type = None
if "quiz_skin_type" not in st.session_state:
    st.session_state.quiz_skin_type = None

# --- Step Progress Bar ---
st.progress(min(st.session_state.step / 3.0, 1.0))

# --- Step 1: Webcam ---
if st.session_state.step == 1:
    st.subheader("Step 1: Capture your face (Option
