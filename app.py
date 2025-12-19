import streamlit as st
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from PIL import Image
import os

# Set page layout
st.set_page_config(page_title="AI Skincare Advisor", layout="wide")

st.title("✨ AI Skincare Product Predictor")
st.write("Use your webcam or upload a photo to find your skin type and get product suggestions.")

# 1. Load the Model Architecture (matches your notebook)
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
    
    # IMPORTANT: If you have a trained weights file, rename it to 'model.h5' 
    # and upload it to your GitHub.
    if os.path.exists('model.h5'):
        model.load_weights('model.h5')
    return model

# 2. Load the specific CSV you uploaded
@st.cache_data
def load_product_data():
    filename = "skin_products.xlsx - Sheet1.csv"
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return None

model = load_skincare_model()
df = load_product_data()
skin_types = ["Oily", "Dry", "Normal", "Sensitive"]

# Check if data file is missing
if df is None:
    st.error(f"⚠️ File Not Found: 'skin_products.xlsx - Sheet1.csv'")
    st.info("Please make sure you uploaded the CSV file to the same folder as app.py in GitHub.")
    st.stop()

# 3. Sidebar - Selection
st.sidebar.header("Choose Input")
option = st.sidebar.radio("Method:", ("Live Webcam", "Upload File"))

if option == "Live Webcam":
    img_file = st.camera_input("Take a photo")
else:
    img_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# 4. Analysis and Suggestions
if img_file:
    col1, col2 = st.columns(2)
    
    # Process Image
    image = Image.open(img_file)
    with col1:
        st.image(image, caption='Captured Profile', use_container_width=True)
    
    # Preprocessing
    img_array = np.array(image.convert('RGB'))
    img_array = cv2.resize(img_array, (64, 64)) / 255.0
    img_array = img_array.reshape(1, 64, 64, 3)
    
    # Prediction
    prediction = model.predict(img_array)
    skin_index = np.argmax(prediction)
    detected_skin = skin_types[skin_index]
    confidence = np.max(prediction)
    
    with col2:
        st.subheader(f"Analysis: :blue[{detected_skin} Skin]")
        st.write(f"**Confidence Score:** {confidence:.2%}")
        st.divider()
        
        # 5. Recommendation Logic using the CSV data
        st.subheader("Personalized Recommendations")
        
        # We search the 'Skin Type' column for the detected type (e.g., 'Dry')
        recommendations = df[df["Skin Type"].str.contains(detected_skin, case=False, na=False)]
        
        if not recommendations.empty:
            # Sort by rating and show the top 5
            top_recs = recommendations.sort_values(by="Reviews ⭐", ascending=False).head(5)
            st.table(top_recs[["Product Name", "Brand", "Price (₹)", "Reviews ⭐", "Low-Cost Website"]])
        else:
            st.warning(f"No specific products found for {detected_skin} skin in this list.")
