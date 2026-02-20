"""Calibration intrinsèque d'une caméra par détection de chessboard.

Capture des photos avec la touche configurée dans parameters.py,
détecte les coins du damier et calcule la matrice K via compute_intrinsics().
Le résultat est sauvegardé avec write().
"""

import cv2
import numpy as np
from parameters import *
from fonctions_images import *
import csv
from write_read_csv import *

capture = cv2.VideoCapture(0)
nb_photo = 0
lst_points = []

while capture.isOpened():
    ret, frame = capture.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame, 1)
    if cv2.waitKey(1) == ord(take_photo) and nb_photo != nb_photo_max:
        nb_photo += 1
        ret, corners = cv2.findChessboardCorners(
            frame,
            checkboard_info[0],
            cv2.CALIB_CB_ADAPTIVE_THRESH
            + cv2.CALIB_CB_FAST_CHECK
            + cv2.CALIB_CB_NORMALIZE_IMAGE,
        )
        lst_points.append(corners)
        for i in corners:
            cv2.circle(frame, (int(i[0][0]), int(i[0][1])), 5, (0, 255, 0), 2)
        cv2.imshow("a", frame)

    if cv2.waitKey(1) == ord(quitter):
        break
    if ret:
        cv2.imshow("test", frame)

capture.release()

K = compute_intrinsics(object_points_list, lst_points)

write(K)
