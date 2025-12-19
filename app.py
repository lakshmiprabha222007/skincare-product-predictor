import streamlit as st
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from PIL import Image
import os

# Set page config
st.set_page_config(page_title="AI Skincare Advisor", layout="wide")

st.title("✨ AI Skincare Product Predictor")
st.write("Use your webcam or upload a photo to get personalized product recommendations.")

# 1. Load the Model Architecture
@st.cache_resource
def load_skincare_model():
    # Architecture from your notebook
    model = Sequential([
        Conv2D(16, (3,3), activation='relu', input_shape=(64,64,3)),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(32, activation='relu'),
        Dense(4, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    # In a real app, you must upload your trained weights 'model.h5' to GitHub
    # if os.path.exists('model.h5'):
    #     model.load_weights('model.h5')
    
    return model

# 2. Load the Product CSV
@st.cache_data
def load_product_data():
    csv_path = "skincare_products.xlsx - Sheet1.csv"
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        st.error(f"File '{csv_path}' not found! Please upload it to your repository.")
        return None

model = load_skincare_model()
df = load_product_data()
skin_types = ["Oily", "Dry", "Normal", "Sensitive"]

# 3. Sidebar for Input Selection
st.sidebar.header("Input Method")
option = st.sidebar.radio("Choose how to provide image:", ("Live Webcam", "Upload File"))

img_file = None
if option == "Live Webcam":
    img_file = st.camera_input("Take a photo")
else:
    img_file = st.sidebar.file_uploader("Upload an image of your skin", type=["jpg", "jpeg", "png"])

# 4. Main Prediction Logic
if img_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        image = Image.open(img_file)
        st.image(image, caption='Captured Image', use_container_width=True)
    
    # Preprocessing
    img_array = np.array(image.convert('RGB'))
    img_array = cv2.resize(img_array, (64, 64))
    img_array = img_array / 255.0
    img_array = img_array.reshape(1, 64, 64, 3)

    with col2:
        if st.button('Analyze & Suggest Products'):
            prediction = model.predict(img_array)
            skin_index = np.argmax(prediction)
            detected_skin = skin_types[skin_index]
            confidence = np.max(prediction)
            
            st.subheader(f"Detected Skin: :blue[{detected_skin}]")
            st.progress(float(confidence))
            st.write(f"**Confidence:** {confidence:.2%}")

            # 5. Recommendation Logic (Matching Notebook)
            if df is not None:
                st.divider()
                st.subheader(f"Top Recommendations for {detected_skin} Skin")
                
                # Filter products where the 'Skin Type' column contains the detected type
                recommendations = df[df["Skin Type"].str.contains(detected_skin, case=False, na=False)]
                
                if not recommendations.empty:
                    # Sort by Rating if the column exists
                    if "Reviews ⭐" in recommendations.columns:
                        recommendations = recommendations.sort_values(by="Reviews ⭐", ascending=False)
                    
                    # Display as a clean table
                    st.table(recommendations[["Product Name", "Brand", "Price (₹)", "Reviews ⭐", "Low-Cost Website"]].head(5))
                else:
                    st.warning("No products found in the database for this skin type.")
