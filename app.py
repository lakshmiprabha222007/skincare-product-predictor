import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Skin Analyzer App")

st.title("Skin Analysis & Product Recommendation App")
st.write("Capture your face using webcam and get skincare product suggestions")

# Load dataset
df = pd.read_excel("skincare_100_rows.xlsx")

# Clean Skin_Type
df["Skin_Type"] = df["Skin_Type"].astype(str).str.strip().str.capitalize()

# Webcam input
st.subheader("📷 Capture Image")
image = st.camera_input("Take a photo")

if image is not None:
    st.success("Image captured successfully!")

    # Simulated skin analysis
    skin_types = ["Oily", "Dry", "Normal", "Sensitive", "Combination"]
    detected_skin = np.random.choice(skin_types)

    st.subheader("🧠 Skin Analysis Result")
    st.info(f"Detected Skin Type: **{detected_skin}**")

    # Filter products
    filtered = df[df["Skin_Type"] == detected_skin]

    # Pick ANY 5 products
    recommended = filtered.sample(5) if len(filtered) >= 5 else filtered

    st.subheader("🧴 Recommended Products (Top 5)")
    st.dataframe(
        recommended[["Product_Code", "Product_Name", "Brand"]]
        .reset_index(drop=True)
    )

else:
    st.warning("Please capture an image to continue")

