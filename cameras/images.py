import cv2
import numpy as np
from cameras.parameters import quitter, P1, P2, nb_led_left_controller, nb_led_right_controller, pos1, pos2
from cameras.fonctions_images import blob_detection_params, groupe_leds, triangulate_point, calculate_point_pos, calculate_coef, image_transform, detect_and_processed_controller_pos, centre, trier_groupe
from multiprocessing.shared_memory import ShareableList
from engine.project import pt1, pt2
import os

try:
    left_controller = ShareableList(name="left_controller")
except FileNotFoundError:
    left_controller = ShareableList(name='left_controller', sequence=range(3))
try:
    right_controller = ShareableList(name="right_controller")
except FileNotFoundError:
    right_controller = ShareableList(name='right_controller', sequence=range(3))


if os.name=="nt":
    capture1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    capture2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
elif os.name=="posix":
    capture1 = cv2.VideoCapture(1)
    capture2 = cv2.VideoCapture(2)

assert capture1.isOpened() and capture2.isOpened(), "Les caméras n'ont pas pus être connecter."

detector = blob_detection_params()

coef_x, coef_y, coef_z = calculate_coef(pos1, pos2, pt1, pt2)

while capture1.isOpened() and capture2.isOpened():
    ret1, frame1 = capture1.read()
    ret2, frame2 = capture2.read()

    if not ret1 or not ret2:
        print('Failed to load video frames')
        continue

    frame1_processed = image_transform(frame1)
    frame2_processed = image_transform(frame2)

    if detect_and_processed_controller_pos(frame1_processed, frame2_processed, detector) == False:
        print('No controller detected')
        cv2.imshow("Camera 1", frame1_processed)
        cv2.imshow("Camera 2", frame2_processed)
        continue
    manette, keypoints1, keypoints2 = detect_and_processed_controller_pos(frame1_processed, frame2_processed, detector)

    if manette['nom'] == 'left':
        left_controller[0] = -manette['pos'][0]*coef_x
        left_controller[1] = -manette['pos'][1]*coef_y
        left_controller[2] = manette['pos'][2]*coef_z

    elif manette['nom'] == 'right':
        right_controller[0] = -manette['pos'][0]*coef_x
        right_controller[1] = -manette['pos'][1]*coef_y
        right_controller[2] = manette['pos'][2]*coef_z

    output1 = cv2.drawKeypoints(frame1, keypoints1, np.array([]), (0, 0, 255),
                                 cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    output2 = cv2.drawKeypoints(frame2, keypoints2, np.array([]), (0, 0, 255),
                                 cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow("Camera 1", output1)
    cv2.imshow("Camera 2", output2)

    if cv2.waitKey(1) == ord(quitter):
        break

capture1.release()
capture2.release()
cv2.destroyAllWindows()