import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Skin Care Product Recommender")

st.title("🧴 Skin Care Product Recommendation App")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_excel("skin_products.xlsx")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df

df = load_data()

st.write("📄 Dataset Columns:", df.columns.tolist())

# Webcam input
img_file = st.camera_input("📷 Capture Image")

def detect_skin_type(image):
    gray = image.convert("L")
    brightness = np.array(gray).mean()

    if brightness > 170:
        return "Dry"
    elif brightness < 100:
        return "Oily"
    else:
        return "Normal"

if img_file:
    image = Image.open(img_file)
    skin_type = detect_skin_type(image)

    st.subheader("🧪 Detected Skin Type")
    st.success(skin_type)

    # Filter products safely
    if "Skin_Type" in df.columns:
        products = df[df["Skin_Type"].str.lower() == skin_type.lower()]
        st.subheader("🛍 Recommended Products")
        st.table(products)
    else:
        st.error("❌ Column 'Skin_Type' not found in Excel file")
st.markdown(
    """
    <style>
    .website-link {
        font-size: 18px;
        text-align: center;
        margin-top: 15px;
    }
    .website-link a {
        color: #ffffff;
        background-color: #0078ff;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
    }
    .website-link a:hover {
        background-color: #005fcc;
    }
    </style>

    <div class="website-link">
        <a href="https://yourwebsite.com" target="_blank">🌐 Visit Our Website</a>
    </div>
    """,
    unsafe_allow_html=True
)
