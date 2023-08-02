from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
import starlette.status as status
from fastapi.staticfiles import StaticFiles
import sys
import os
from PIL import Image
import io
from datetime import datetime
from fastapi.responses import HTMLResponse
# sys.path.insert(0, '/Users/Shark/Projects/final_project/yolov5-fastapi-demo')

import cv2
import numpy as np

import torch
import base64
import random

root = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory=os.path.join(root, 'scripts')), name="js")
templates = Jinja2Templates(directory = 'templates')

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"
model_selection_options = ['best']
model_dict = {model_name: None for model_name in model_selection_options} #set up model cache

colors = [tuple([random.randint(0, 255) for _ in range(3)]) for _ in range(100)] #for bbox plotting

##############################################
#-------------GET Request Routes--------------
##############################################
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})



@app.get("/camera")
def camera(request: Request):
    ''' Returns html jinja2 template render for home page form
    '''

    return templates.TemplateResponse('camera.html', {
            "request": request,
            "model_selection_options": model_selection_options,
        })


@app.get("/detect")
def drag_and_drop_detect(request: Request):


    return templates.TemplateResponse('upload.html', 
            {"request": request,
            "model_selection_options": model_selection_options,
        })

@app.get("/images/{file_name}")
def show_results(request:Request,
                 file_name:str,
                 img_size:int = 640):

    file_path = "./images/"+ file_name + '.png'
    with open(file_path, 'rb') as f:
        data = f.read()
    img_batch  = [cv2.imdecode(np.fromstring(data, np.uint8), cv2.IMREAD_COLOR)]
    img_batch_rgb = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in img_batch]

    model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt', force_reload=True) 

    results = model(img_batch_rgb, size = img_size)
    json_results = results_to_json(results,model)
    img_str_list = []
    #plot bboxes on the image
    for img, bbox_list in zip(img_batch, json_results):
        for bbox in bbox_list:
            label = f'{bbox["class_name"]} {bbox["confidence"]:.2f}'
            plot_one_box(bbox['bbox'], img, label=label, 
                    line_thickness=3)

        img_str_list.append(base64EncodeImage(img))

    encoded_json_results = str(json_results).replace("'",r"\'").replace('"',r'\"')

    return templates.TemplateResponse('show_results.html', {
            'request': request,
            'bbox_image_data_zipped': zip(img_str_list,json_results), #unzipped in jinja2 template
            'bbox_data_str': encoded_json_results,
        })


##############################################
#------------POST Request Routes--------------
##############################################

@app.post("/save")
async def save_img(request: Request,
                    file_list: List[UploadFile] = File(...)):
    img_bytes = [file.file.read() for file in file_list][0]
    img = Image.open(io.BytesIO(img_bytes))
    now_time = datetime.now().strftime(DATETIME_FORMAT) # 저장 형식 
    img_savename = f"images/{now_time}.png"
    img.save(img_savename)
    img_savename = img_savename.split('.')[0]
    return RedirectResponse(url=img_savename, status_code=status.HTTP_302_FOUND)
    
@app.post("/camera")
async def detect_with_server_side_rendering(request: Request,
                        file_list: List[UploadFile] = File(...), 
                        model_name: str = Form('best'),
                        img_size: int = Form(640)):
    

    model_dict[model_name] = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt', force_reload=True) 
    img_batch = [cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_COLOR) for file in file_list]
    img_batch_rgb = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in img_batch]
    results = model_dict[model_name](img_batch_rgb, size = img_size)
    json_results = results_to_json(results,model_dict[model_name])

    img_str_list = []
    for img, bbox_list in zip(img_batch, json_results):
        for bbox in bbox_list:
            label = f'{bbox["class_name"]} {bbox["confidence"]:.2f}'
            plot_one_box(bbox['bbox'], img, label=label, 
                    line_thickness=3)

        img_str_list.append(base64EncodeImage(img))
    encoded_json_results = str(json_results).replace("'",r"\'").replace('"',r'\"')

    # show_results(request, zip(img_str_list,json_results), encoded_json_results)
    return templates.TemplateResponse('show_results.html', {
            'request': request,
            'bbox_image_data_zipped': zip(img_str_list,json_results), #unzipped in jinja2 template
            'bbox_data_str': encoded_json_results,
        })





@app.post("/detect")
def detect_via_api(request: Request,
                file_list: List[UploadFile] = File(...), 
                model_name: str = Form(...),
                img_size: Optional[int] = Form(640)):

    model_dict[model_name] = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt', force_reload=True) 
    img_batch = [cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_COLOR)
                for file in file_list]

    img_batch_rgb = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in img_batch]
    
    results = model_dict[model_name](img_batch_rgb, size = img_size) 
    json_results = results_to_json(results,model_dict[model_name])

    img_str_list = []
    for img, bbox_list in zip(img_batch, json_results):
        for bbox in bbox_list:
            label = f'{bbox["class_name"]} {bbox["confidence"]:.2f}'
            plot_one_box(bbox['bbox'], img, label=label, 
                    line_thickness=3)

        img_str_list.append(base64EncodeImage(img))
    encoded_json_results = str(json_results).replace("'",r"\'").replace('"',r'\"')

    # show_results(request, zip(img_str_list,json_results), encoded_json_results)
    return templates.TemplateResponse('show_results.html', {
            'request': request,
            'bbox_image_data_zipped': zip(img_str_list,json_results), #unzipped in jinja2 template
            'bbox_data_str': encoded_json_results,
        })
    
    
    
##############################################
#--------------Helper Functions---------------
##############################################

def results_to_json(results, model):
    ''' Converts yolo model output to json (list of list of dicts)'''
    return [
                [
                    {
                    "class": int(pred[5]),
                    "class_name": model.model.names[int(pred[5])],
                    "bbox": [int(x) for x in pred[:4].tolist()], #convert bbox results to int from float
                    "confidence": float(pred[4]),
                    }
                for pred in result
                ]
            for result in results.xyxy
            ]


def plot_one_box(x, im, color=(128, 128, 128), label=None, line_thickness=3):
    # Directly copied from: https://github.com/ultralytics/yolov5/blob/cd540d8625bba8a05329ede3522046ee53eb349d/utils/plots.py
    # Plots one bounding box on image 'im' using OpenCV
    assert im.data.contiguous, 'Image not contiguous. Apply np.ascontiguousarray(im) to plot_on_box() input image.'
    tl = line_thickness or round(0.002 * (im.shape[0] + im.shape[1]) / 2) + 1  # line/font thickness
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(im, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(im, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(im, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


def base64EncodeImage(img):
    ''' Takes an input image and returns a base64 encoded string representation of that image (jpg format)'''
    _, im_arr = cv2.imencode('.png', img)
    im_b64 = base64.b64encode(im_arr.tobytes()).decode('utf-8')

    return im_b64

if __name__ == '__main__':
    import uvicorn
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default = 'localhost')
    parser.add_argument('--port', default = 8000)
    parser.add_argument('--precache-models', action='store_true', 
            help='Pre-cache all models in memory upon initialization, otherwise dynamically caches models')
    opt = parser.parse_args()

    if opt.precache_models:
        model_dict = {model_name: torch.hub.load('ultralytics/yolov5', model_name, pretrained=True) 
                        for model_name in model_selection_options}
    
    app_str = 'server:app' #make the app string equal to whatever the name of this file is
    uvicorn.run(app_str, host= '0.0.0.0', port=opt.port, reload=True)