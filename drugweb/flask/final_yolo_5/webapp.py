"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
from PIL import Image
import datetime
import cv2 
import ssl
import base64
import uuid
import pandas as pd

import torch
from flask import Flask, render_template, request, redirect , Response , jsonify

app = Flask(__name__)

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"

@app.route('/')
def main_page():
    return render_template('home.html')

#capture 1 용 predict 
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model([img])

        results.render()  # updates results.imgs with boxes and labels
        now_time = datetime.datetime.now().strftime(DATETIME_FORMAT) # 저장 형식 
        img_savename = f"static/{now_time}.png"
        Image.fromarray(results.ims[0]).save(img_savename)
        
    return render_template("image.html")
        # df = results.pandas().xyxy[0]
        # return redirect('result.html', table=df.to_html())
        # return redirect(img_savename)

    return render_template("image.html")


@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/capture2')
def index2():
    return render_template('capture2.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


# @app.route("/upload", methods=["GET", "POST"])


# @app.route('/upload', methods=['GET','POST'])
# def upload():
#     # Get the uploaded file
#     file = request.files['image']

#     # Save the file to the 'uploads' folder
#     file.save(os.path.join('uploads', file.filename))

#     return render_template("tem.html")



# def save_photo():
#     try:
#         data = request.get_json()
#         image_data = data.get('imageData', '')
#         # Generate a unique filename for the photo (you can use other methods too)
#         filename = 'photo_' + str(uuid.uuid4()) + '.webp'
#         # Decode the base64 image data
#         decoded_image_data = base64.b64decode(image_data)
#         # Specify the path where the photo will be saved on the server
#         folder_path = '/path/to/server/folder/'  # Replace this with the actual path
#         file_path = os.path.join(folder_path, filename)
#         # Save the photo on the server
#         with open(file_path, 'wb') as f:
#             f.write(decoded_image_data)
#         return jsonify({"message": "Photo saved successfully"}), 200
    
#     except Exception as e:
#         print('Error:', str(e))
#         return jsonify({"message": "Failed to save the photo"}), 500

# @app.route('/upload', methods=['GET','POST'])
# def upload():
#     if request.method == "POST":
#         # if "file" not in request.files:
#         #     return redirect(request.url)
#         webcam = cv2.VideoCapture(0)
#         ret, frame = webcam.read()   
#         # if not frame:
#         #     return
#         cv2.imwrite('static/photo.jpg', frame)
#         return redirect(frame)
#     return render_template("capture.html")

# @app.route('/capture')
# def capture():
#     return render_template('capture.html')


# @app.route('/upload', methods=['GET', 'POST'])
#     # 웹캠에서 사진을 가져오기
# def upload():    
#     if request.method == "POST":
#         webcam = cv2.VideoCapture(0)
#         ret, frame = webcam.read()
#         cv2.imwrite('static/photo.jpg', frame)  # 이미지를 저장
#     return render_template('capture.html')




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', _verbose=False)  # force_reload = recache latest code
    model.eval()
    # app.debug=True
    app.run(host="0.0.0.0", port=args.port,ssl_context='adhoc')  # debug=True causes Restarting with stat
