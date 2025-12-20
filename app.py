import streamlit as st
import pandas as pd
from PIL import Image, ImageStat

st.set_page_config(page_title="Skin Care Product Recommender")

st.title("🧴 Skin Care Product Recommendation App")
st.write("Go step by step: Webcam → Quiz → Product Recommendations")

# Load dataset safely
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

# --- Initialize session state ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "brightness_skin_type" not in st.session_state:
    st.session_state.brightness_skin_type = None
if "quiz_skin_type" not in st.session_state:
    st.session_state.quiz_skin_type = None

# --- Step 1: Webcam ---
if st.session_state.step == 1:
    st.subheader("Step 1: Capture your face (Optional)")
    img_file = st.camera_input("📷 Capture Image")

    if img_file is not None:
        image = Image.open(img_file)
        st.image(image, caption="Captured Image", use_column_width=True)
        brightness = get_brightness(image)
        st.write(f"🌞 Estimated brightness: {brightness:.2f}")
        st.session_state.brightness_skin_type = brightness_to_skin_type(brightness)
        st.write(f"🧴 Predicted skin type: **{st.session_state.brightness_skin_type}**")

    if st.button("Next: Skin Quiz"):
        st.session_state.step = 2

# --- Step 2: Skin Quiz ---
elif st.session_state.step == 2:
    st.subheader("Step 2: Take a detailed skin quiz (Optional)")

    q1 = st.radio("How does your skin feel after washing your face?", ["Tight or dry", "Comfortable", "Oily/shiny"])
    q2 = st.radio("How often does your skin get oily during the day?", ["Rarely", "Sometimes", "Often"])
    q3 = st.radio("Do you have visible pores?", ["Small/Invisible", "Medium", "Large"])
    q4 = st.radio("How often do you get dry patches?", ["Rarely", "Sometimes", "Often"])
    q5 = st.radio("Does your skin feel greasy by midday?", ["Never", "Sometimes", "Always"])
    q6 = st.radio("How sensitive is your skin?", ["Very sensitive", "Slightly sensitive", "Not sensitive"])
    q7 = st.radio("How prone is your skin to acne or breakouts?", ["Rarely", "Sometimes", "Often"])
    q8 = st.radio("How visible are fine lines or wrinkles?", ["Very visible", "Slightly visible", "Not visible"])

    # Calculate quiz score
    score = 0
    answers = [q1,q2,q3,q4,q5,q6,q7,q8]
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

    st.write(f"🧴 Quiz-based predicted skin type: **{st.session_state.quiz_skin_type}**")

    if st.button("Next: Recommended Products"):
        st.session_state.step = 3

# --- Step 3: Product Recommendation ---
elif st.session_state.step == 3:
    st.subheader("Step 3: Recommended Products")

    manual_skin_type = st.radio("Or select your skin type manually", ["dry", "normal", "oily"])

    # Final skin type priority: Webcam > Quiz > Manual
    final_skin_type = st.session_state.brightness_skin_type or st.session_state.quiz_skin_type or manual_skin_type
    st.write(f"✅ Final skin type used for recommendations: **{final_skin_type}**")

    # Find skin type column
    skin_col = None
    for col in df.columns:
        if "skin" in col and "type" in col:
            skin_col = col
            break

    if skin_col is None:
        st.error("❌ Skin type column not found in dataset")
    else:
        products = df[df[skin_col].str.lower() == final_skin_type]
        if not products.empty:
            st.table(products.head(5))
        else:
            st.warning("No products found for this skin type.")

    # Restart button
    if st.button("Restart"):
        st.session_state.step = 1
        st.session_state.brightness_skin_type = None
        st.session_state.quiz_skin_type = None
