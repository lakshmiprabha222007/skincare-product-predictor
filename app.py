import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Skin Care Product Recommender")

st.title("🧴 Skin Care Product Recommendation App")
st.write("Use webcam or select your skin type manually to get product suggestions")

# Load dataset safely
@st.cache_data
def load_data():
    df = pd.read_excel("skin_products.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data()

# Show dataset columns
st.write("📄 Dataset Columns:", df.columns.tolist())

# Webcam input (optional, for demo)
img_file = st.camera_input("📷 Capture Image (Optional)")

if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="Captured Image", use_column_width=True)
    st.write("📊 Webcam analysis shown for demo only")

# ✅ Manual skin type selection
skin_type = st.radio(
    "Select your skin type",
    ["dry", "oily", "normal"]
)

st.subheader("🛍 Recommended Products")

# Auto-detect column
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

