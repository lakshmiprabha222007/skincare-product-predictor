import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from PIL import Image

st.title("Skincare Product Predictor")

# 1. Load the Model (matching your notebook architecture)
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
    
    # IMPORTANT: Ensure 'skin_products.pkl' or your weights file is in your GitHub repo
    # If you have a saved .h5 file, use: model.load_weights('your_model.h5')
    return model

model = load_skincare_model()

# 2. Image Uploading
uploaded_file = st.file_uploader("Choose an image of your skin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the file to an image that OpenCV can read
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    # Preprocessing (Matching notebook logic)
    img_array = np.array(image.convert('RGB'))
    img_array = cv2.resize(img_array, (64, 64))
    img_array = img_array / 255.0
    img_array = img_array.reshape(1, 64, 64, 3)

    if st.button('Predict Product'):
        prediction = model.predict(img_array)
        class_idx = np.argmax(prediction)
        confidence = np.max(prediction)
        
        st.write(f"### Prediction: Product Category {class_idx}")
        st.write(f"**Confidence:** {confidence:.2%}")
