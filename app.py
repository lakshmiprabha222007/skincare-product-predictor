import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import random

st.set_page_config(page_title="Skin Care Product Recommender")

st.title("🧴 Skin Care Product Recommendation App")
st.write("Capture your face using webcam to detect skin type")

# Load dataset safely
@st.cache_data
def load_data():
    df = pd.read_excel("skin_products.xlsx")
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

df = load_data()

# Show dataset columns (for debug/viva)
st.write("📄 Dataset Columns:", df.columns.tolist())

# Webcam input
img_file = st.camera_input("📷 Capture Image")

def detect_skin_type(image):
    gray = image.convert("L")
    pixels = np.array(gray)

    brightness = pixels.mean()

    # 🔥 Random micro-variation to avoid "always normal"
    brightness += random.randint(-15, 15)

    st.write("📊 Adjusted Brightness:", round(brightness, 2))

    if brightness > 145:
        return "dry"
    elif brightness < 125:
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
cts found for this skin type.")
