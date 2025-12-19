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

# 1. Load the Model Architecture
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
    
    # If you have a trained weights file (e.g. skin_model.h5), uncomment the line below:
    # if os.path.exists('skin_model.h5'): model.load_weights('skin_model.h5')
    
    return model

# 2. Load the CSV Data
@st.cache_data
def load_product_data():
    # Try the exact name of the file you uploaded
    filename = "https://github.com/lakshmiprabha222007/skincare-product-predictor/blob/main/skin_products.xlsx"
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        # Fallback for common renames
        if os.path.exists("products.csv"):
            return pd.read_csv("products.csv")
    return None

model = load_skincare_model()
df = load_product_data()
skin_types = ["Oily", "Dry", "Normal", "Sensitive"]

# Check if data loaded
if df is None:
    st.error("Database file not found! Ensure 'skincare_products.xlsx - Sheet1.csv' is in your GitHub folder.")
    st.stop()

# 3. Sidebar/Webcam UI
st.sidebar.header("Settings")
option = st.sidebar.radio("Input Source:", ("Live Webcam", "Upload Image"))

if option == "Live Webcam":
    img_file = st.camera_input("Snap a photo of your skin")
else:
    img_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

# 4. Prediction Logic
if img_file:
    col1, col2 = st.columns(2)
    
    # Process Image
    image = Image.open(img_file)
    with col1:
        st.image(image, caption='Input Photo', use_container_width=True)
    
    # Preprocessing
    img_array = np.array(image.convert('RGB'))
    img_array = cv2.resize(img_array, (64, 64)) / 255.0
    img_array = img_array.reshape(1, 64, 64, 3)
    
    # Predict
    prediction = model.predict(img_array)
    skin_index = np.argmax(prediction)
    detected_skin = skin_types[skin_index]
    
    with col2:
        st.subheader(f"Result: :blue[{detected_skin} Skin]")
        st.write(f"Match Confidence: {np.max(prediction):.2%}")
        st.divider()
        
        # 5. Fixed Recommendation Logic
        st.subheader("Recommended Products")
        
        # Filter for the detected skin type
        recs = df[df["Skin Type"].str.contains(detected_skin, case=False, na=False)]
        
        if not recs.empty:
            st.table(recs[["Product Name", "Brand", "Price (₹)", "Reviews ⭐"]].head(5))
        else:
            st.warning("No specific products found for this skin type in the database.")
