import streamlit as st
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from PIL import Image
import os

# Set page layout and styling
st.set_page_config(page_title="AI Skincare Advisor", layout="wide")

st.title("✨ AI Skincare Product Predictor")
st.markdown("### Identify your skin type via Webcam and get instant recommendations")

# 1. Define Model Architecture (Exactly as in your notebook)
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
    
    # Attempt to load weights if the user has provided a 'model.h5' file
    if os.path.exists('model.h5'):
        try:
            model.load_weights('model.h5')
        except Exception as e:
            st.sidebar.warning(f"Could not load weights: {e}. Using uninitialized model.")
    else:
        st.sidebar.info("Note: 'model.h5' not found. Predictions will be random until weights are uploaded.")
    
    return model

# 2. Load the Product Database
@st.cache_data
def load_product_data():
    # Looking for the specific file name you uploaded
    filename = "skin_products (1).xlsx - Sheet1.csv"
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        st.error(f"⚠️ Database file '{filename}' not found in the repository!")
        return None

# Initialize Model and Data
model = load_skincare_model()
df = load_product_data()
skin_types = ["Oily", "Dry", "Normal", "Sensitive"]

# 3. Streamlit Interface
if df is not None:
    # Camera Input (Live Webcam)
    st.subheader("Step 1: Capture Photo")
    img_file = st.camera_input("Smile and look at the camera")

    if img_file:
        col1, col2 = st.columns([1, 1.5])
        
        # Display the captured image
        image = Image.open(img_file)
        with col1:
            st.image(image, caption="Your Skin Profile", use_container_width=True)
        
        # 4. Preprocessing & Prediction
        # Resize to 64x64, convert to RGB, and normalize (Matching notebook logic)
        img_array = np.array(image.convert('RGB'))
        img_array = cv2.resize(img_array, (64, 64)) / 255.0
        img_array = img_array.reshape(1, 64, 64, 3)
        
        prediction = model.predict(img_array)
        skin_index = np.argmax(prediction)
        detected_skin = skin_types[skin_index]
        confidence = np.max(prediction)
        
        with col2:
            st.subheader(f"Analysis Result: :blue[{detected_skin}]")
            st.write(f"**AI Confidence Score:** {confidence:.2%}")
            st.divider()
            
            # 5. Recommendation Logic
            st.subheader(f"Recommended for {detected_skin} Skin")
            
            # Filter the CSV based on the detected skin type
            recommendations = df[df["Skin Type"].str.contains(detected_skin, case=False, na=False)]
            
            if not recommendations.empty:
                # Sort by reviews and show the top 5
                top_recs = recommendations.sort_values(by="Reviews ⭐", ascending=False).head(5)
                
                # Show only relevant columns
                display_cols = ["Product Name", "Brand", "Price (₹)", "Reviews ⭐", "Low-Cost Website"]
                st.table(top_recs[display_cols])
            else:
                st.warning(f"No specific products found for {detected_skin} skin in our dataset.")
else:
    st.info("Please upload your CSV file to the GitHub repository to see recommendations.")
