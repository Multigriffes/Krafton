import cv2
import numpy as np
import time
from sklearn import metrics
from sklearn.cluster import DBSCAN
from parameters import *

def groupe_leds(points_list: list):
    groupe = DBSCAN(eps=max_distance_pixel)

def blob_detection_params():
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = minThreshold
    params.maxThreshold = maxThreshold
    params.filterByColor = filterByColor
    params.blobColor = blobColor
    params.filterByArea = filterByArea
    params.minArea = minArea

    detector = cv2.SimpleBlobDetector_create(params)
    return detector

# Faire fonction traitement image pour capture 1 et 2.
capture = cv2.VideoCapture(0)
'''capture_1 = cv2.VideoCapture(1)'''

x=0
timer = 0
detector = blob_detection_params()
list_point = []

while capture.isOpened():
    start_time = time.perf_counter()
    x+=1
    ret, frame = capture.read()
    # conversion en couleur binaire (noir OU blanc)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Floutage de l'immage
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    _, frame = cv2.threshold(frame, 250, 255, cv2.THRESH_BINARY)
    frame = cv2.flip(frame, 1)
    # Detection led
    #detector = blob_detection_params()
    keypoints = detector.detect(frame)
    if keypoints != ():
        list_point.append((keypoints[0].pt[0], keypoints[0].pt[1]))
        end_time = time.perf_counter()
        timer += 1/(end_time-start_time)
        print((timer)/x)
    output = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    if ret:

        # Affiche l'image
        cv2.imshow("test", output)
        

        # Quitter la video
        if cv2.waitKey(1) == ord(quitter):
            break
    

capture.release()