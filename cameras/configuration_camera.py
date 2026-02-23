import cv2
import numpy as np
from parameters import *
from fonctions_images import *
import csv
from write_read_csv import write, clear_file

capture1 = cv2.VideoCapture(0)
capture2 = cv2.VideoCapture(1)
ret, frame = capture1.read()
image_size = (frame.shape[0], frame.shape[1])

nb_photo = 0
lst_points1 = []
lst_points2 = []

while capture1.isOpened() and capture2.isOpened():
    ret1, frame1 = capture1.read()
    ret2, frame2 = capture2.read()

    if cv2.waitKey(1) == ord(take_photo) and nb_photo != nb_photo_max:
        nb_photo += 1
        ret1, corners1 = cv2.findChessboardCorners(frame1, checkboard_info[0],
                cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        ret2, corners2 = cv2.findChessboardCorners(frame2, checkboard_info[0],
                cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        lst_points1.append(corners1)
        lst_points2.append(corners2)
        for i in corners1:
            cv2.circle(frame1, (int(i[0][0]), int(i[0][1])), 5, (0, 255, 0), 2)
        cv2.imshow('1', frame1)
        for i in corners2:
            cv2.circle(frame2, (int(i[0][0]), int(i[0][1])), 5, (0, 255, 0), 2)
        cv2.imshow('2', frame2)


    if cv2.waitKey(1) == ord(quitter):
        break
    if ret1 and ret2:
        cv2.imshow("test1", frame1)
        cv2.imshow("test2", frame2)

capture1.release()
capture2.release()

clear_file()

