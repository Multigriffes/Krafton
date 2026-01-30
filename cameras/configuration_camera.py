import cv2
import numpy as np

checkboard_info = [(6, 8), 22] # dimension chessboard (en carres), dimension carre (en mm)

capture = cv2.VideoCapture(0)
'''
frame = cv2.imread("img.png")
cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
ret, corners = cv2.findChessboardCorners(frame, (6, 9), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
print(corners)
'''


while capture.isOpened():
    ret, frame = capture.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame, 1)
    if cv2.waitKey(1) == ord("p"):
        ret, corners = cv2.findChessboardCorners(frame, checkboard_info[0], cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        for i in corners:
            cv2.circle(frame, (int(i[0][0]), int(i[0][1])), 5, (0, 255, 0), 2)
        cv2.imshow('a', frame)

        objp = np.zeros((6*8, 3), np.float32)
        objp[:,:2] = np.mgrid[0:6,0:8].T.reshape(-1,2)
        objectPoints = [objp]
 
        imagePoints = [corners]
 
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectPoints, imagePoints, (frame[0].shape[1], frame[0].shape[0]), None, None)

    if cv2.waitKey(1) == ord("q"):
        break
    if ret:
        cv2.imshow("test", frame)

capture.release()
