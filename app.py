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
st.set_page_config(page_title="Skincare AI Predictor", layout="centered")

st.title("✨ Skincare Product Predictor")
st.write("Take a photo or upload an image to identify your skin type and get recommendations.")

# 1. Load the Model Architecture (matching your notebook)
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
    
    # NOTE: In a real scenario, you would load your trained weights here:
    # if os.path.exists('skincare_model.h5'):
    #     model.load_weights('skincare_model.h5')
    
    return model

# 2. Load the Dataset
@st.cache_data
def load_recommendations():
    if os.path.exists('skin_products.pkl'):
        return pd.read_pickle('skin_products.pkl')
    else:
        st.warning("Product database (skin_products.pkl) not found. Recommendations will not be shown.")
        return None

model = load_skincare_model()
df = load_recommendations()
skin_types = ["Oily", "Dry", "Normal", "Sensitive"]

# 3. Input Selection: Upload or Webcam
option = st.radio("Choose Input Method:", ("Webcam (Live Snapshot)", "Upload Image"))

img_file = None
if option == "Webcam (Live Snapshot)":
    img_file = st.camera_input("Take a picture of your face")
else:
    img_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# 4. Processing and Prediction
if img_file is not None:
    # Convert file to image
    image = Image.open(img_file)
    st.image(image, caption='Processed Image', use_container_width=True)
    
    # Preprocessing (64x64, RGB, Normalized)
    img_array = np.array(image.convert('RGB'))
    img_array = cv2.resize(img_array, (64, 64))
    img_array = img_array / 255.0
    img_array = img_array.reshape(1, 64, 64, 3)

    if st.button('Analyze Skin Type'):
        with st.spinner('Analyzing...'):
            prediction = model.predict(img_array)
            skin_index = np.argmax(prediction)
            detected_skin = skin_types[skin_index]
            confidence = np.max(prediction)
            
            st.success(f"### Detected Skin Type: {detected_skin}")
            st.info(f"**Confidence Score:** {confidence:.2%}")
            
            # Show Recommendations
            if df is not None:
                st.subheader(f"Recommended Products for {detected_skin} Skin")
                # Filter based on notebook logic
                recommended = df[df["Skin Type"].str.contains(detected_skin, case=False)]
                
                if not recommended.empty:
                    display_cols = ["Product Name", "Brand", "Price (₹)", "Reviews ⭐", "Low-Cost Website"]
                    # Check if columns exist before displaying
                    existing_cols = [c for c in display_cols if c in recommended.columns]
                    st.dataframe(recommended[existing_cols].head(5), use_container_width=True)
                else:
                    st.write("No specific products found for this type in the database.")
