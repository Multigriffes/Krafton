import cv2
from cameras.parameters import object_points_list, take_photo, nb_photo_max, quitter, chessboard_info
from cameras.fonctions_images import compute_homography, compute_V, compute_B, compute_intrinsincs, compute_extrinsics, compute_stereo_extrinsecs, compute_projection_matrices
from cameras.write_read_csv import write, clear_file

#capture1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#capture2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
capture1 = cv2.VideoCapture(1)
capture2 = cv2.VideoCapture(2)
assert capture1.isOpened() and capture2.isOpened(), "Les caméras n'ont pas pus être connecter."

nb_photo = 0
lst_photo1 = []
lst_photo2 = []

while capture1.isOpened() and capture2.isOpened():


    ret1, frame1 = capture1.read()
    ret2, frame2 = capture2.read()

    
    key = cv2.waitKey(100)
    if key == ord(take_photo) and nb_photo != nb_photo_max:
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        corners_ret1, corners1 = cv2.findChessboardCorners(frame1, chessboard_info[0])
        corners_ret2, corners2 = cv2.findChessboardCorners(frame2, chessboard_info[0])

        if corners_ret1 and corners_ret2:
            lst_photo1.append(corners1.reshape(-1,2))
            lst_photo2.append(corners2.reshape(-1,2))
            nb_photo += 1
            print(nb_photo)
        else:
            print("Chessboard non detecte")

    elif (key == ord(quitter)) or nb_photo == nb_photo_max:
        break
    
    if ret1 and ret2:
        cv2.imshow("test1", frame1)
        cv2.imshow("test2", frame2)

#capture1.release()
#capture2.release()

clear_file()

lst1_H = compute_homography(lst_photo1, object_points_list)
lst2_H = compute_homography(lst_photo2, object_points_list)

V1 = compute_V(lst1_H)
V2 = compute_V(lst2_H)

B1 = compute_B(V1)
B2 = compute_B(V2)

K1 = compute_intrinsincs(B1)
K2 = compute_intrinsincs(B2)

extrinsics1 = []
extrinsics2 = []

for H1 in lst1_H:
    R1, t1 = compute_extrinsics(K1, H1)
    extrinsics1.append((R1, t1))
for H2 in lst2_H:
    R2, t2 = compute_extrinsics(K2, H2)
    extrinsics2.append((R2, t2))


R, t = compute_stereo_extrinsecs(extrinsics1, extrinsics2)

P1, P2 = compute_projection_matrices(K1, K2, R, t)

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