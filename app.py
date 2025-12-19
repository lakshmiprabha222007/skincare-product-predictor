import streamlit as st
import cv2
import numpy as np
import pandas as pd

st.set_page_config(page_title="Skin Care Product Recommender")

st.title("🧴 Skin Care Product Recommendation App")
st.write("Use your webcam to detect skin type and get product suggestions")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_excel("skin_products.xlsx")

df = load_data()

# Webcam capture
img_file = st.camera_input("📷 Capture your face")

def detect_skin_type(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)

    if brightness > 170:
        return "Dry"
    elif brightness < 100:
        return "Oily"
    else:
        return "Normal"

if img_file is not None:
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    skin_type = detect_skin_type(img)

    st.subheader("🧪 Detected Skin Type:")
    st.success(skin_type)

    st.subheader("🛍️ Recommended Products:")
    products = df[df["Skin_Type"] == skin_type]

    st.table(products[["Product_Name", "Brand", "Price"]])
