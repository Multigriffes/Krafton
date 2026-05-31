import cv2
from cameras.parameters import object_points_list, take_photo, nb_photo_max, quitter, chessboard_info, place_point
from cameras.fonctions_images import compute_homography, compute_V, compute_B, compute_intrinsincs, compute_extrinsics, compute_stereo_extrinsecs, compute_projection_matrices, image_transform, blob_detection_params
from cameras.write_read_csv import write, clear_file
import os

# Verification du systeme d'exploitation de l'utilisateur
if os.name == "nt": # Windows
    capture1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    capture2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
elif os.name == "posix": # Linux
    capture1 = cv2.VideoCapture(1)
    capture2 = cv2.VideoCapture(2)


assert capture1.isOpened() and capture2.isOpened(), "Les caméras n'ont pas pus être connectés."

nb_photo = 0
lst_photo1 = []
lst_photo2 = []

run_chessboard_calibration = True
run_3d_box_calibration = False
place_pt_hg_print = False
place_pt_bd_print = False
place_pt_hg = False
place_pt_bd = False

while capture1.isOpened() and capture2.isOpened():
    # lecture des images
    ret1, frame1 = capture1.read()
    ret2, frame2 = capture2.read()

    # recupere les inputs utilisateur
    key = cv2.waitKey(100)

    if run_chessboard_calibration:
        # si la touche pressee correspond a celle pour prendre des photo
        if key == ord(take_photo) and nb_photo != nb_photo_max:
            # met les images en nuance de gris
            frame1 = image_transform(frame1)
            frame2 = image_transform(frame2)
            # detection des coins du damier
            corners_ret1, corners1 = cv2.findChessboardCorners(frame1, chessboard_info[0])
            corners_ret2, corners2 = cv2.findChessboardCorners(frame2, chessboard_info[0])

            # Si il y a bien des coins detectes
            if corners_ret1 and corners_ret2:
                lst_photo1.append(corners1.reshape(-1, 2))
                lst_photo2.append(corners2.reshape(-1, 2))
                nb_photo += 1
                print(nb_photo)
            else:
                print("Chessboard non detecte")

        # s'active si la toucue quitter est pressee ou si le nombre de photo est egal au nombre de photo max
        elif (key == ord(quitter)) or nb_photo == nb_photo_max:
            run_chessboard_calibration = False # stoppe l'etape de la calibration avec le damier
            run_3d_box_calibration = True # demarre la partie de la calibration configurant l'aire de jeu
            place_pt_hg_print = True

    if run_3d_box_calibration:
        if place_pt_hg_print:
            print("Après avoir installé les filtres infrarouges,",
                  "allumez la manette et positionnez la dans l'angle en haut a gauche des deux images de caméras",
                  "(elle doit aussi etre le plus proche possible des caméras)",
                  "Ce point serviras de limite virtuelle au position des manettes.")
            place_pt_hg_print = False
        elif place_pt_bd_print:
            print("Après avoir installé les filtres infrarouges,",
                  "allumez la manette et positionnez la dans l'angle en bas a droite des deux images de caméras",
                  "(elle doit aussi etre le plus loin possible des caméras)",
                  "Ce point serviras de limite virtuelle au position des manettes.")
            place_pt_bd_print = False

        # quand la touche permettant de placer un point est pressee
        if key == ord(place_point):
            # si le premier point n'a pas encore ete place
            if not place_pt_hg:
                frame1_processed_1 = image_transform(frame1)
                frame2_processed_1 = image_transform(frame2)
                place_pt_hg = True
                place_pt_bd_print = True
            # sinon si le deuxieme point n'a pas ete place
            elif not place_pt_bd:
                frame1_processed_2 = image_transform(frame1)
                frame2_processed_2 = image_transform(frame2)
                place_pt_bd = True
            else:
                break

    # affichage des images si elles sont disponibles
    if ret1 and ret2:
        cv2.imshow("test1", frame1)
        cv2.imshow("test2", frame2)

capture1.release()
capture2.release()

# vide le ficher csv
clear_file()

# calcul des matrices d'homographies de chaque images
lst1_H = compute_homography(lst_photo1, object_points_list)
lst2_H = compute_homography(lst_photo2, object_points_list)

V1 = compute_V(lst1_H)
V2 = compute_V(lst2_H)

B1 = compute_B(V1)
B2 = compute_B(V2)

# calcul des parametres intrinseques de chaque camera
K1 = compute_intrinsincs(B1)
K2 = compute_intrinsincs(B2)

extrinsics1 = []
extrinsics2 = []

# Calcul des parametres extrinseques de chaque camera
for H1 in lst1_H:
    R1, t1 = compute_extrinsics(K1, H1)
    extrinsics1.append((R1, t1))
for H2 in lst2_H:
    R2, t2 = compute_extrinsics(K2, H2)
    extrinsics2.append((R2, t2))

# calcul des parametres intrinseques d'une camera par rapport a l'autre
R, t = compute_stereo_extrinsecs(extrinsics1, extrinsics2)

# calcul des matrice de projection
P1, P2 = compute_projection_matrices(K1, K2, R, t)

# sauvegarde des parametres dans un fichier csv
write('K1', K1)
write('K2', K2)
write('R', R)
write('R1', R1)
write('R2', R2)
write('t', t)
write('t1', t1)
write('t2', t2)
write('P1', P1)
write('P2', P2)

# importation faite ici pour recuperer de nouveau les parametres du fichier csv que l'on vient d'ecrire
from cameras.fonctions_images import detect_and_processed_controller_pos

detector = blob_detection_params()
manette1, _, _ = detect_and_processed_controller_pos(frame1_processed_1, frame2_processed_1, detector)
manette2, _, _ = detect_and_processed_controller_pos(frame1_processed_2, frame2_processed_2, detector)

# sauvegarde des position de l'aire du terrain de jeu
write('pos1', manette1['pos'])
write('pos2', manette2['pos'])
