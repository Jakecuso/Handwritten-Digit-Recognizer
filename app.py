from flask import Flask, request, jsonify
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from flask_cors import CORS
import base64
from io import BytesIO
from PIL import Image

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Load the trained model
model = load_model("digit_recognizer.keras")

def preprocess_image(image):
    """Preprocess the drawn digit for model prediction"""
    img = Image.open(BytesIO(base64.b64decode(image)))  # Decode image from Base64
    img = img.convert("L")  # Convert to grayscale
    img = img.resize((28, 28))  # Resize to 28x28 pixels
    img = np.array(img)
    
    # Apply preprocessing (same as in digit_draw.py)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1]
    img = cv2.bitwise_not(img)
    img = img / 255.0  # Normalize
    img = img.reshape(1, 28, 28, 1)  # Reshape for CNN input
    
    return img

@app.route("/predict", methods=["POST"])
def predict():
    """Receive an image, process it, and return the model prediction"""
    data = request.json  # Get JSON data
    image_data = data.get("image")  # Extract Base64 image
    if not image_data:
        return jsonify({"error": "No image provided"}), 400
    
    img = preprocess_image(image_data)  # Preprocess image
    
    prediction = model.predict(img)[0]  # Make prediction
    top_3_indices = np.argsort(prediction)[-3:][::-1]  # Get top 3 predictions
    top_3_confidences = prediction[top_3_indices] * 100  # Convert to percentage
    
    return jsonify({
        "predictions": [
            {"digit": int(top_3_indices[i]), "confidence": float(top_3_confidences[i])}
            for i in range(3)
        ]
    })

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)