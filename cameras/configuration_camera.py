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

if lst_points1 != [] and lst_points2 != [0]:
    K1 = compute_intrinsics(object_points_list_2D, lst_points1)
    K2 = compute_intrinsics(object_points_list_2D, lst_points2)
    write('K1', K1)
    write('K2', K2)

    R1 = np.identity(3)
    T1 = [0, 0, 0]
    write('R1', R1)
    write('T1', T1)

    ret, K1, dist1, K2, dist2, R2, T2, E, F = cv2.stereoCalibrate(
        objectPoints=object_points_list_3D,
        imagePoints1=lst_points1,
        imagePoints2=lst_points2,
        cameraMatrix1=K1,
        distCoeffs1=None,
        cameraMatrix2=K2,
        distCoeffs2=None,
        imageSize=image_size,
        flags=cv2.CALIB_FIX_INTRINSIC
    )

    write('R2', R2)
    write('T2', 'T2')

    H1, H2 = rectify_cameras(K1, R1, T1, K2, R2, T2)
    write('H1', H1)
    write('H2', H2)