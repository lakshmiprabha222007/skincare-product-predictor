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
    st.subheader("Step 1: Capture your face (Optional)")
    st.image("webcam_frame.png", width=400)  # Optional themed frame

    img_file = st.camera_input("📷 Capture Image")
    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Captured Image", use_column_width=True)
        brightness = get_brightness(image)
        st.write(f"🌞 Estimated brightness: {brightness:.2f}")
        st.session_state.brightness_skin_type = brightness_to_skin_type(brightness)
        st.success(f"🧴 Predicted skin type: **{st.session_state.brightness_skin_type}**")

    if st.button("Next: Skin Quiz"):
        st.session_state.step = 2

# --- Step 2: Skin Quiz ---
elif st.session_state.step == 2:
    st.subheader("Step 2: Take a detailed skin quiz (Optional)")
    st.image("quiz_theme.png", width=500)  # Optional themed image

    q1 = st.radio("How does your skin feel after washing your face?", ["Tight or dry", "Comfortable", "Oily/shiny"])
    q2 = st.radio("How often does your skin get oily during the day?", ["Rarely", "Sometimes", "Often"])
    q3 = st.radio("Do you have visible pores?", ["Small/Invisible", "Medium", "Large"])
    q4 = st.radio("How often do you get dry patches?", ["Rarely", "Sometimes", "Often"])
    q5 = st.radio("Does your skin feel greasy by midday?", ["Never", "Sometimes", "Always"])
    q6 = st.radio("How sensitive is your skin?", ["Very sensitive", "Slightly sensitive", "Not sensitive"])
    q7 = st.radio("How prone is your skin to acne or breakouts?", ["Rarely", "Sometimes", "Often"])
    q8 = st.radio("How visible are fine lines or wrinkles?", ["Very visible", "Slightly visible", "Not visible"])

    # Calculate quiz score
    answers = [q1,q2,q3,q4,q5,q6,q7,q8]
    score = 0
    for ans in answers:
        if ans in ["Tight or dry", "Rarely", "Small/Invisible", "Never", "Very sensitive", "Very visible"]:
            score += 1
        elif ans in ["Comfortable", "Sometimes", "Medium", "Slightly sensitive", "Slightly visible"]:
            score += 2
        else:
            score += 3

    # Map score to skin type
    if score <= 10:
        st.session_state.quiz_skin_type = "dry"
    elif score <= 16:
        st.session_state.quiz_skin_type = "normal"
    else:
        st.session_state.quiz_skin_type = "oily"

    st.info(f"🧴 Quiz-based predicted skin type: **{st.session_state.quiz_skin_type}**")

    if st.button("Next: Recommended Products"):
        st.session_state.step = 3

# --- Step 3: Product Recommendation ---
elif st.session_state.step == 3:
    st.subheader("Step 3: Recommended Products")
    st.image("product_theme.png", width=500)  # Optional theme image

    manual_skin_type = st.radio("Or select your skin type manually", ["dry", "normal", "oily"])
    final_skin_type = st.session_state.brightness_skin_type or st.session_state.quiz_skin_type or manual_skin_type

    # Color-coded final skin type card
    skin_colors = {"dry":"#f4c2c2", "normal":"#c2f4c2", "oily":"#c2c2f4"}
    st.markdown(
        f"<div style='background-color:{skin_colors.get(final_skin_type,'#fff')}; padding:15px; border-radius:10px'>"
        f"✅ Final skin type used for recommendations: <b>{final_skin_type}</b></div>", 
        unsafe_allow_html=True
    )

    # Find skin type column
    skin_col = next((c for c in df.columns if "skin" in c and "type" in c), None)

    if skin_col:
        products = df[df[skin_col].str.lower() == final_skin_type]
        if not products.empty:
            st.table(products.sample(min(5, len(products))))
        else:
            st.warning("No products found for this skin type.")
    else:
        st.error("❌ Skin type column not found in dataset")

    # Restart
    if st.button("Restart"):
        st.session_state.step = 1
        st.session_state.brightness_skin_type = None
        st.session_state.quiz_skin_type = None
