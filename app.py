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
    return pd.read_excel("skin_products.xlsx")

df = load_data()

# Webcam input
img_file = st.camera_input("📷 Capture Image")

def detect_skin_type(image):
    gray = image.convert("L")  # Convert to grayscale
    pixels = np.array(gray)
    brightness = pixels.mean()

    if brightness > 170:
        return "Dry"
    elif brightness < 100:
        return "Oily"
    else:
        return "Normal"

if img_file is not None:
    image = Image.open(img_file)

    skin_type = detect_skin_type(image)

    st.subheader("🧪 Detected Skin Type")
    st.success(skin_type)

    st.subheader("🛍 Recommended Products")
    products = df[df["Skin_Type"] == skin_type]

    st.table(products[["Product_Name", "Brand", "Price"]])

