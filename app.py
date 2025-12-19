import streamlit as st
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from PIL import Image
import os

st.set_page_config(page_title="AI Skincare Advisor", layout="wide")

st.title("✨ AI Skincare Product Predictor")

# 1. Load the Model
@st.cache_resource
def load_skincare_model():
    model = Sequential([
        Conv2D(16, (3,3), activation='relu', input_shape=(64,64,3)),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(32, activation='relu'),
        Dense(4, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    # Optional: model.load_weights('model.h5') if you have a weights file
    return model

# 2. Robust File Loading
@st.cache_data
def load_product_data():
    # List of possible names the file might have on GitHub
    possible_names = [
        "skincare_products.xlsx - Sheet1.csv",
        "skincare_products.csv",
        "products.csv"
    ]
    
    for name in possible_names:
        if os.path.exists(name):
            return pd.read_csv(name)
    
    return None

model = load_skincare_model()
df = load_product_data()
skin_types = ["Oily", "Dry", "Normal", "Sensitive"]

if df is None:
    st.error("⚠️ Error: Product database file not found in GitHub. Please check your filename.")
    st.info("Ensure the CSV file is in the same folder as app.py and is named: `skincare_products.xlsx - Sheet1.csv`")
    st.stop()

# 3. Sidebar and Webcam Input
st.sidebar.header("Input Source")
option = st.sidebar.radio("Method:", ("Live Webcam", "Upload File"))

img_file = st.camera_input("Take a photo") if option == "Live Webcam" else st.sidebar.file_uploader("Upload Image", type=["jpg", "png"])

if img_file:
    col1, col2 = st.columns(2)
    image = Image.open(img_file)
    with col1:
        st.image(image, caption='Captured Skin Profile', use_container_width=True)
    
    # Predict
    img_array = np.array(image.convert('RGB'))
    img_array = cv2.resize(img_array, (64, 64)) / 255.0
    prediction = model.predict(img_array.reshape(1, 64, 64, 3))
    detected_skin = skin_types[np.argmax(prediction)]
    
    with col2:
        st.subheader(f"Analysis: :blue[{detected_skin} Skin]")
        st.write(f"Confidence: {np.max(prediction):.2%}")
        
        st.divider()
        st.subheader("Recommended for You:")
        # Filter logic
        recs = df[df["Skin Type"].str.contains(detected_skin, case=False, na=False)]
        st.table(recs[["Product Name", "Brand", "Price (₹)", "Reviews ⭐"]].head(5))warning("No products found in the database for this skin type.")
