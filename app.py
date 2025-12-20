import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# ======================
# App Configuration
# ======================
st.set_page_config(
    page_title="Skin Care Product Recommender",
    layout="centered"
)

st.title("🧴 Skin Care Product Recommendation App")
st.write("Capture your face using webcam to analyze skin type")

# ======================
# Load Excel Dataset
# ======================
@st.cache_data
def load_data():
    df = pd.read_excel("skin_products.xlsx")

    # Clean column names
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    # Clean Skin_Type values
    df["Skin_Type"] = df["Skin_Type"].astype(str).str.strip().str.capitalize()

    return df

df = load_data()

# ======================
# Webcam Input
# ======================
st.subheader("📷 Capture Image")
image_file = st.camera_input("Take a photo")

# ======================
# Improved Skin Detection
# ======================
def detect_skin_type(image):
    gray = image.convert("L")
    img_array = np.array(gray)

    brightness = img_array.mean()
    contrast = img_array.std()

    # Improved logic (not always Normal)
    if brightness < 115 and contrast > 40:
        return "Oily"
    elif brightness > 160 and contrast < 35:
        return "Dry"
    else:
        return "Normal"

# =====================
