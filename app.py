import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(page_title="Skin Care Product Recommender", layout="centered")

st.title("🧴 Skin Care Product Recommendation App")
st.write("Use webcam to analyze skin type and get product recommendations")

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
# Skin Type Detection (Simple Logic)
# ======================
def detect_skin_type(image):
    gray = image.convert("L")          # Convert to grayscale
    brightness = np.array(gray).mean() # Average brightness

    if brightness > 170:
        return "Dry"
    elif brightness < 100:
        return "Oily"
    else:
        return "Normal"

# ======================
# After Image Capture
# ======================
if image_file is not None:
    image = Image.open(image_file)

    skin_type = detect_skin_type(image)

    st.subheader("🧪 Detected Skin Type")
    st.success(skin_type)

    # ======================
    # Product Recommendation
    # ======================
    if "Skin_Type" in df.columns:
        filtered_products = df[df["Skin_Type"] == skin_type]

        if filtered_products.empty:
            st.warning("No products found for this skin type.")
        else:
            # Recommend up to 5 products
            recommended = (
                filtered_products.sample(5)
                if len(filtered_products) >= 5
                else filtered_products
            )

            st.subheader("🛍 Recommended Products")
            st.dataframe(
                recommended[["Product_Code", "Product_Name", "Brand"]]
                .reset_index(drop=True)
            )
    else:
        st.error("❌ 'Skin_Type' column not found in Excel file")

else:
    st.i

