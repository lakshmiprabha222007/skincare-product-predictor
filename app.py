import streamlit as st
import pandas as pd
from PIL import Image, ImageStat

st.set_page_config(page_title="Skin Care Product Recommender")

st.title("🧴 Skin Care Product Recommendation App")
st.write("Capture your face, take a skin quiz, or select your skin type to get product suggestions")

# Load dataset safely
@st.cache_data
def load_data():
    df = pd.read_excel("skin_products.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data()
st.write("📄 Dataset Columns:", df.columns.tolist())

# Function to calculate brightness
def get_brightness(img):
    img = img.convert("L")  # convert to grayscale
    stat = ImageStat.Stat(img)
    return stat.mean[0]

# Map brightness to skin type
def brightness_to_skin_type(brightness):
    if brightness < 90:
        return "dry"
    elif brightness < 160:
        return "normal"
    else:
        return "oily"

# --- Step 1: Webcam input ---
img_file = st.camera_input("📷 Capture Image (Optional)")

brightness_skin_type = None
if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="Captured Image", use_column_width=True)
    
    # Estimate brightness and skin type
    brightness = get_brightness(image)
    st.write(f"🌞 Estimated brightness: {brightness:.2f}")
    brightness_skin_type = brightness_to_skin_type(brightness)
    st.write(f"🧴 Predicted skin type based on brightness: **{brightness_skin_type}**")

# --- Step 2: Enhanced Skin Quiz ---
st.subheader("📝 Take a detailed skin quiz (Optional)")

q1 = st.radio("How does your skin feel after washing your face?", ["Tight or dry", "Comfortable", "Oily/shiny"])
q2 = st.radio("How often does your skin get oily during the day?", ["Rarely", "Sometimes", "Often"])
q3 = st.radio("Do you have visible pores?", ["Small/Invisible", "Medium", "Large"])
q4 = st.radio("How often do you get dry patches?", ["Rarely", "Sometimes", "Often"])
q5 = st.radio("Does your skin feel greasy by midday?", ["Never", "Sometimes", "Always"])
q6 = st.radio("How sensitive is your skin?", ["Very sensitive", "Slightly sensitive", "Not sensitive"])
q7 = st.radio("How prone is your skin to acne or breakouts?", ["Rarely", "Sometimes", "Often"])
q8 = st.radio("How visible are fine lines or wrinkles?", ["Very visible", "Slightly visible", "Not visible"])

# Scoring for quiz
score = 0
answers = [q1,q2,q3,q4,q5,q6,q7,q8]
for ans in answers:
    if ans in ["Tight or dry", "Rarely", "Small/Invisible", "Never", "Very sensitive", "Very visible"]:
        score += 1
    elif ans in ["Comfortable", "Sometimes", "Medium", "Slightly sensitive", "Slightly visible"]:
        score += 2
    else:
        score += 3

# Map total score to skin type
quiz_skin_type = None
if score <= 10:
    quiz_skin_type = "dry"
elif score <= 16:
    quiz_skin_type = "normal"
else:
    quiz_skin_type = "oily"

st.write(f"🧴 Quiz-based predicted skin type: **{quiz_skin_type}**")

# --- Step 3: Manual selection ---
manual_skin_type = st.radio("Or select your skin type manually", ["dry", "normal", "oily"])

# --- Step 4: Determine final skin type ---
# Priority: Webcam brightness > Quiz > Manual
if brightness_skin_type:
    final_skin_type = brightness_skin_type
elif quiz_skin_type:
    final_skin_type = quiz_skin_type
else:
    final_skin_type = manual_skin_type

st.write(f"✅ Final skin type used for recommendations: **{final_skin_type}**")

# --- Step 5: Show recommended products ---
st.subheader("🛍 Recommended Products")

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
        st.table(products.head(5))  # show top 5 products
    else:
        st.warning("No products found for this skin type.")

