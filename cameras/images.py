"""Capture vidéo en temps réel : détection de marqueurs LED par blob detection."""

import cv2
import numpy as np
import time
from parameters import *
from fonctions_images import *


def image_transform(image):
    """Prépare une frame pour la détection : niveaux de gris → ouverture morphologique → seuillage → miroir."""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    _, image = cv2.threshold(image, 250, 255, cv2.THRESH_BINARY)
    image = cv2.flip(image, 1)

    return image


# Faire fonction traitement image pour capture 1 et 2.
capture = cv2.VideoCapture(0)
"""capture_1 = cv2.VideoCapture(1)"""

x = 0
timer = 0
detector = blob_detection_params()
list_point = []

while capture.isOpened():
    start_time = time.perf_counter()
    x += 1
    ret, frame = capture.read()

    frame = image_transform(frame)

    # Detection led
    keypoints = detector.detect(frame)
    if keypoints != ():
        list_point.append((keypoints[0].pt[0], keypoints[0].pt[1]))
        end_time = time.perf_counter()
        timer += 1 / (end_time - start_time)
        print((timer) / x)
    output = cv2.drawKeypoints(
        frame,
        keypoints,
        np.array([]),
        (0, 0, 255),
        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
    )

    if ret:

        # Affiche l'image
        cv2.imshow("test", output)

        # Quitter la video
        if cv2.waitKey(1) == ord(quitter):
            break


capture.release()
