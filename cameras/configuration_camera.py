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
lst_photo1 = []
lst_photo2 = []

while capture1.isOpened() and capture2.isOpened():
    ret1, frame1 = capture1.read()
    ret2, frame2 = capture2.read()

    if cv2.waitKey(1) == ord(take_photo) and nb_photo != nb_photo_max:
        nb_photo += 1
        lst_photo1.append(frame1)
        lst_photo2.append(frame2)

    if cv2.waitKey(1) == ord(quitter):
        break
    if ret1 and ret2:
        cv2.imshow("test1", frame1)
        cv2.imshow("test2", frame2)

capture1.release()
capture2.release()

clear_file()

lst_H1 = compute_homography(lst_photo1)
lst_H2 = compute_homography(lst_photo2)