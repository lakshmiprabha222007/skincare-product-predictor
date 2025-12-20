import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Skin Care Product Recommender")

st.title("🧴 Skin Care Product Recommendation App")
st.write("Capture your face using webcam to detect skin type")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_excel("skin_products.xlsx")
    df.columns = df.columns.str.strip()  # safety
    return df

df = load_data()

# Webcam input
img_file = st.camera_input("📷 Capture Image")

def detect_skin_type(image):
    gray = image.convert("L")
    pixels = np.array(gray)

    brightness = pixels.mean()

    # Show value for demo/viva
    st.write("📊 Brightness value:", round(brightness, 2))

    if brightness > 150:
        return "Dry"
    elif brightness < 120:
        return "Oily"
    else:
        return "Normal"

if img_file is not None:
    image = Image.open(img_file)

    # Auto detection
    auto_skin_type = detect_skin_type(image)

    st.subheader("🧪 Auto Detected Skin Type")
    st.success(auto_skin_type)

    # Manual confirmation (IMPORTANT FIX)
    st.info("If detection is not accurate, please confirm manually:")

    skin_type = st.radio(
        "Confirm your skin type",
        ["Dry", "Oily", "Normal"],
        index=["Dry", "Oily", "Normal"].index(auto_skin_type)
    )

    st.subheader("🛍 Recommended Products")

    products = df[df["Skin_Type"].str.lower() == skin_type.lower()]

    if not products.empty:
        st.table(products[["Product_Name", "Brand", "Price"]])
    else:
        st.warning("No products found for this skin type.")
