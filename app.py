import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Skin Care Product Recommender")

st.title("🧴 Skin Care Product Recommendation App")
st.write("Capture your face using webcam to detect skin type")

# Load dataset safely
@st.cache_data
def load_data():
    df = pd.read_excel("skin_products.xlsx")

    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df

df = load_data()

# Show columns (for debugging/demo)
st.write("📄 Dataset Columns:", df.columns.tolist())

# Webcam input
img_file = st.camera_input("📷 Capture Image")

def detect_skin_type(image):
    gray = image.convert("L")
    pixels = np.array(gray)

    brightness = pixels.mean()
    st.write("📊 Brightness:", round(brightness, 2))

    if brightness > 50:
        return "dry"
    elif brightness < 20:
        return "oily"
    else:
        return "normal"

if img_file is not None:
    image = Image.open(img_file)

    # Auto detection
    auto_skin_type = detect_skin_type(image)

    st.subheader("🧪 Auto Detected Skin Type")
    st.success(auto_skin_type.capitalize())

    # Manual confirmation
    skin_type = st.radio(
        "Confirm your skin type",
        ["dry", "oily", "normal"],
        index=["dry", "oily", "normal"].index(auto_skin_type)
    )

    st.subheader("🛍 Recommended Products")

    # Find correct skin type column automatically
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
            st.table(products)
        else:
            st.warning("No products found for this skin type.")

