import numpy as np
import cv2 as cv
import cv2
import argparse
from ultralytics import YOLO
import numpy as np  
# # Add the video file argument with a default value
# parser.add_argument('video_file', type=str, default='part4.mp4', help='Path to the video file. Default is part4.mp4')
# # Parse the command line arguments
# args = parser.parse_args()
# take first frame of the video
# setup initial location of window
#x, y, w, h = 300, 200, 100, 50  # simply hardcoded the values
# set up the ROI for tracking

def tracking():
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                    # Read a frame from the video
                frame = cv2.resize(frame,(640,640))
                height ,width ,_ = frame.shape 

                # Run YOLOv8 tracking on the frame, persisting tracks between frames
                print("W,H = ", height,width)

                
                results = model.predict(frame)
                for result in results:
                    n_detections = result.boxes.shape[0]
                    if(n_detections ==0):
                        continue
                    print(result.boxes.data.shape[0],result.boxes.data.dtype)
                    k_model = (np.asarray(result.boxes.data[0])[:4]).flatten().astype(np.int32)
                    print("k-model ", k_model)
                    # k_remaped_x = (k_model[::2]) #/640)*width
                    # k_remaped_y = (k_model[1::2]) #/640)*height
                    # x, y = (k_remaped_x[0]+k_remaped_x[1])/2 ,(k_remaped_y[0]+k_remaped_y[1])/2
                    # w, h = (k_remaped_x[1]-k_remaped_x[0]) ,(k_remaped_y[1]-k_remaped_y[0]) 
                    # print(width,height)
                    # print(x,y,w,h)

                    # track_window = (int(x),int( y),int( w),int( h))
                    # roi = frame[int(y):int(y+h), int(x):int(x+w)]
                    # print("track-window = ",k_model)
                    roi = frame[k_model[1]:k_model[3], k_model[0]:k_model[2],:]
                    track_window = (k_model[0],k_model[1], k_model[2]-k_model[0], k_model[3]-k_model[1])
                    # track_window = (281,193,31,128)

                    # print("track-window = ",track_window)
                    # cv.imshow("ROI ",roi)
                    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
                    # mask = cv.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
                    roi_hist = cv.calcHist([hsv_roi], [0], None, [180], [0, 180])
                    cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)     
                    # cv2.imshow("Mask ", mask)
                    # Setup the termination criteria, either 10 iteration or move by at least 1 pt
                    term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
                    # print(x,y,w,h)
                    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                    dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
                    
                    # apply camshift to get the new locationq
                    ret, track_window = cv.CamShift(dst, track_window, term_crit)
                    print('return = ',ret)
                    print("Final_Track_Window= ", track_window)
                    # Draw it on image
                    pts = cv.boxPoints(ret)
                    pts = np.int0(pts)
                    img2 = cv.polylines(frame, [pts], True, 255, 2)
                    cv.imshow('img2', img2)
                    cv.imshow("ROI ",roi)
                    
                    k = cv.waitKey(30) & 0xff
                    if k == 27:
                        cv.destroyAllWindows()
                        break
            else:
                break

# Load the YOLOv8 model
model = YOLO('best.pt')

# Open the video file
video_path = "part4.mp4"
cap = cv2.VideoCapture(video_path)
tracking()