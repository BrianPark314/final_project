# Flask imports
from flask import Flask, request, render_template

# Inference imports
import torch
import cv2
import numpy as np
import os

# Initialize app
app = Flask(__name__)
# Load model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', _verbose=False)
# Define folder to save images
IMG_DIR = os.path.join('static', 'results')

# Default route, page to prompt image upload
@app.route('/')
def home():
    return render_template('index.html')

# Handling form submission
@app.route('/predict', methods=['POST'])
def predict():
    # Get file from the form's POST request
    file = request.files['file']
    bytes = np.fromfile(file, np.uint8)
    # Convert to NumPy array
    img_array = cv2.imdecode(bytes, cv2.IMREAD_COLOR)
    # Inference
    result = model(img_array)
    # Save results
    filename = os.path.join(IMG_DIR, file.filename)
    cv2.imwrite(filename, result.render()[0])
    # Render page with image
    return render_template("index.html", image = filename)

# Start server
app.run()