import streamlit as st
import pandas as pd
from PIL import Image, ImageStat

st.set_page_config(page_title="Skin Care Product Recommender")

st.title("🧴 Skin Care Product Recommendation App")
st.write("Capture your face or select your skin type to get product suggestions")

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

# Webcam input
img_file = st.camera_input("📷 Capture Image (Optional)")

if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="Captured Image", use_column_width=True)
    
    # Estimate brightness and skin type
    brightness = get_brightness(image)
    st.write(f"🌞 Estimated brightness: {brightness:.2f}")
    skin_type = brightness_to_skin_type(brightness)
    st.write(f"🧴 Predicted skin type based on brightness: **{skin_type}**")
else:
    # Manual skin type selection if webcam not used
    skin_type = st.radio(
        "Select your skin type manually",
        ["dry", "oily", "normal"]
    )

# Show recommended products
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
    products = df[df[skin_col].str.lower() == skin_type]
    if not products.empty:
        st.table(products.head(5))  # show top 5 products
    else:
        st.warning("No products found for this skin type.")


