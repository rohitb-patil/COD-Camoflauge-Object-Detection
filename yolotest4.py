import cv2
import ultralytics
from ultralytics import YOLO
import numpy as np

# Load the YOLOv8 model
model = YOLO('best.pt')

# Read the input image
image = cv2.imread('3-Images-of-Myanmar-rebel-armies-ambush-military-convoy-and-aftermath_mp4-20_jpg.rf.070e41d50445a11d4f72628f8f89eb49(1).jpg')
results = model.predict(image)
for result in results:
    boxes = result.boxes.xywh
    if boxes.size(0) > 0:
     print('DETECKTED',boxes)
    else:
      print('NOT DETCTED')

