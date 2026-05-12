import cv2
import time
import numpy as np
from cameras.parameters import kernel, quitter, P1, P2, nb_led_left_controller, nb_led_right_controller
from cameras.fonctions_images import blob_detection_params, groupe_leds, triangulate_point, calculate_point_pos
from multiprocessing.shared_memory import ShareableList
import os

try:
    left_controller = ShareableList(name="left_controller")
except FileNotFoundError:
    left_controller = ShareableList(name='left_controller', sequence=range(3))
try:
    right_controller = ShareableList(name="right_controller")
except FileNotFoundError:
    right_controller = ShareableList(name='right_controller', sequence=range(3))


def image_transform(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def centre(groupe):
    x = sum(p[0] for p in groupe) / len(groupe)
    y = sum(p[1] for p in groupe) / len(groupe)
    return (x, y)


def trier_groupe(groupe):
    return sorted(groupe, key=lambda p: (p[0], p[1]))


if os.name=="nt":
    capture1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    capture2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
elif os.name=="posix":
    capture1 = cv2.VideoCapture(1)
    capture2 = cv2.VideoCapture(2)

assert capture1.isOpened() and capture2.isOpened(), "Les caméras n'ont pas pus être connecter."

timer = 0
nb_frames = 0
detector = blob_detection_params()
print("P1 =", P1)
print("P2 =", P2)

while capture1.isOpened() and capture2.isOpened():
    start_time = time.perf_counter()

    ret1, frame1 = capture1.read()
    ret2, frame2 = capture2.read()

    if not ret1 or not ret2:
        continue

    frame1_processed = image_transform(frame1)
    frame2_processed = image_transform(frame2)

    keypoints1 = detector.detect(frame1_processed)
    keypoints2 = detector.detect(frame2_processed)

    if len(keypoints1) > 0 and len(keypoints2) > 0:
        points1 = [(kp.pt[0], kp.pt[1]) for kp in keypoints1]
        points2 = [(kp.pt[0], kp.pt[1]) for kp in keypoints2]

        groupe_img_1 = groupe_leds(points1)
        groupe_img_2 = groupe_leds(points2)

        pos_groupes = []

        if len(groupe_img_1) > 0 and len(groupe_img_2) > 0:

            groupe_img_1 = sorted(groupe_img_1, key=lambda g: centre(g)[1])
            groupe_img_2 = sorted(groupe_img_2, key=lambda g: centre(g)[1])

            nb_groupes = min(len(groupe_img_1), len(groupe_img_2))

            for i in range(nb_groupes):
                groupe1_trie = trier_groupe(groupe_img_1[i])
                groupe2_trie = trier_groupe(groupe_img_2[i])

                nb_points = min(len(groupe1_trie), len(groupe2_trie))

                if nb_points == 0:
                    continue

                points_3d = []
                for k in range(nb_points):
                    pt3d = triangulate_point(P1, P2, groupe1_trie[k], groupe2_trie[k])
                    points_3d.append(pt3d)

                pos_groupes.append(points_3d)

        for pos in pos_groupes:
            if len(pos) == 0:
                continue

            pos_manette = calculate_point_pos(pos)
            print('gauche', pos_manette)

            if len(pos) == nb_led_left_controller:
                left_controller[0] = pos_manette[0]
                left_controller[1] = pos_manette[1]
                left_controller[2] = pos_manette[2]

            elif len(pos) == nb_led_right_controller:
                right_controller[0] = pos_manette[0]
                right_controller[1] = pos_manette[1]
                right_controller[2] = pos_manette[2]

        end_time = time.perf_counter()
        elapsed = end_time - start_time
        if elapsed > 0:
            timer += 1 / elapsed
            nb_frames += 1
            if nb_frames % 30 == 0:
                print(f"FPS moyen : {timer / nb_frames:.1f}")

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