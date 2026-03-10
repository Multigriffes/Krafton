import cv2
import time
import numpy as np
from parameters import kernel, quitter, P1, P2
from fonctions_images import blob_detection_params, groupe_leds, triangulate_point

def image_transform(image, H):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    _, image = cv2.threshold(image, 250, 255, cv2.THRESH_BINARY)
    image = cv2.flip(image, 1)
    image = cv2.warpPerspective(image, H)

    return image


# Faire fonction traitement image pour capture 1 et 2.
capture1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)

x=0
timer = 0
detector = blob_detection_params()
list_point1 = []
list_point2 = []

while capture1.isOpened() and capture2.isOpened():
    start_time = time.perf_counter()
    x+=1

    ret1, frame1 = capture1.read()
    ret2, frame2 = capture2.read()

    # Detection led
    keypoints1 = detector.detect(frame1)
    keypoints2 = detector.detect(frame2)
    if keypoints1 != () and keypoints2 != ():
        list_point1.append((keypoints1[0].pt[0], keypoints1[0].pt[1]))
        list_point2.append((keypoints2[0].pt[0], keypoints2[0].pt[1]))

        groupe_img_1 = groupe_leds(list_point1)
        groupe_img_2 = groupe_leds(list_point2)

        pos_groupes = []
        if groupe_img_1 != [] and groupe_img_2 != []:
            for i in range(min(len(groupe_img_1), len(groupe_img_2))):
                print(1, groupe_img_1)
                print(2, groupe_img_2)
                pos_groupes.append(triangulate_point(P1, P2, groupe_img_1[i][0], groupe_img_2[i][0]))
            
            print(3, pos_groupes)
                
       
        end_time = time.perf_counter()
        timer += 1/(end_time-start_time)

    output1 = cv2.drawKeypoints(frame1, keypoints1, np.array([]), (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    output2 = cv2.drawKeypoints(frame2, keypoints2, np.array([]), (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    if ret1 and ret2:

        # Affiche l'image
        cv2.imshow("test1", output1)
        cv2.imshow("test2", output2)
        

        # Quitter la video
        if cv2.waitKey(1) == ord(quitter):
            break
    

capture1.release()
capture2.release()