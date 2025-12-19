import os
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, jsonify
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

app = Flask(__name__)

# 1. Recreate Model Architecture (matching the notebook)
def load_skincare_model():
    model = Sequential([
        Conv2D(16, (3,3), activation='relu', input_shape=(64,64,3)),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(32, activation='relu'),
        Dense(4, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Note: You need to have 'skin_products.pkl' or weights saved 
    # from your training session to load them here.
    # If you saved the whole model: model = tf.keras.models.load_model('model.h5')
    return model

model = load_skincare_model()

# 2. Preprocessing function
def prepare_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (64, 64))
    img = img / 255.0
    img = img.reshape(1, 64, 64, 3)
    return img

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    file_path = "temp_image.jpg"
    file.save(file_path)
    
    try:
        # Process image
        processed_img = prepare_image(file_path)
        
        # Predict
        prediction = model.predict(processed_img)
        class_idx = np.argmax(prediction)
        
        # Cleanup
        os.remove(file_path)
        
        return jsonify({
            'class_index': int(class_idx),
            'confidence': float(np.max(prediction))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
