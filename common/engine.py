from common.params import args
from ultralytics import YOLO
from common.utils import timeit

@timeit
def init_model():
    model = YOLO(args.base_path / 'model/yolov8n.pt')
    return model