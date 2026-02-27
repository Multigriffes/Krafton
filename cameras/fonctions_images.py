from parameters import *
import cv2
from math import sqrt

def groupe_leds(point_list:list):
    point_visite = [1 for i in range(len(point_list))] # 1 pour point non visite, 0 sinon
    liste_groupe = []
    for i, point in enumerate(point_list):
        if point_visite[i]:
            groupe = []
            cluster_recur(i, point, groupe, point_visite, point_list)
            liste_groupe.append(groupe)

    return liste_groupe


def cluster_recur(index_point_depart:int, point_depart:tuple, cluster:list, point_visite:list, point_list:list):
    point_visite[index_point_depart] = 0
    cluster.append(point_depart)
    for i, point in enumerate(point_list):
        if point_visite[i]:
            distance_carre = (point_depart[0]-point[0])**2 + (point_depart[1]-point[1])**2
            if distance_carre < distance_max_carre:
                cluster_recur(i, point, cluster, point_visite, point_list)

def blob_detection_params():
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = minThreshold
    params.maxThreshold = maxThreshold
    params.filterByColor = filterByColor
    params.blobColor = blobColor
    params.filterByArea = filterByArea
    params.minArea = minArea

    detector = cv2.SimpleBlobDetector_create(params)
    return detector

def produit_matriciel(mat_1: np.array, mat_2: np.array) -> np.array:
    if mat_1.shape[1] != mat_2.shape[0]:
        raise ValueError("Dimensions incompatibles pour le produit matriciel")
    
    n, p = mat_1.shape
    n2, p2 = mat_2.shape
    
    mat = np.zeros((n, p2))
    
    for i in range(n):
        for j in range(p2):
            mat[i, j] = sum(mat_1[i, k] * mat_2[k, j] for k in range(p))
    
    return mat

def compute_A(lst_points_image, lst_points_realite):
    A = np.zeros((len(lst_points_realite)*2, 9))
    lst_type = [[], []]

    for i in range(0, len(lst_points_realite), 2):
        A[i, 0] = -lst_points_realite[i][0]
        A[i, 1] = -lst_points_realite[i][1]
        A[i, 2] = -1
        A[i, 3] = 0
        A[i, 4] = 0
        A[i, 5] = 0
        A[i, 6] = lst_points_image[i][0]*lst_points_realite[i][0]
        A[i, 7] = lst_points_image[i][0]*lst_points_realite[i][1]
        A[i, 8] = lst_points_image[i][0]

        A[i+1, 0] = 0
        A[i+1, 1] = 0
        A[i+1, 2] = 0
        A[i+1, 3] = -lst_points_realite[i][0]
        A[i+1, 4] = -lst_points_realite[i][1]
        A[i+1, 5] = -1
        A[i+1, 6] = lst_points_image[i][1]*lst_points_realite[i][0]
        A[i+1, 7] = lst_points_image[i][1]*lst_points_realite[i][1]
        A[i+1, 8] = lst_points_image[i][1]

    return A

def compute_homography(lst_images):
    lst_H = []
    for image in range(lst_images):
        A = compute_A(image, object_points_list_2D)

        U, S, V = np.linalg.svd(A)
        h = V[-1]
        H = reshape(h, (3, 3))
        # Normaliser
        lst_H.append(A)

    return lst_H

def reshape(mat, dimension):
    mat2 = np.zeros(dimension)

    for i in range(len(mat)):
        x, y = i%3, i//3
        mat2[x, y] = mat[i]
    
    return mat2

def compute_intrinsincs(B, H):
    Cy = (B[0, 1]*B[0, 2] - B[0, 0]*B[1, 2])/(B[0, 0]*B[1, 1] - B[0, 1]**2)
    l = B[2, 2] - (B[0, 2]**2 + Cy(B[0, 1]*B[0, 2] - B[0, 0]*B[1, 2]))/B[0, 0]
    Fx = sqrt(l/B[0, 0])
    Fy = sqrt(l*B[0, 0]/(B[0, 0]*B[1, 1] - B[0, 1]**2))
    g = -B[0, 1]*(Fx**2)*Fy/l
    Cx = l*Cy/Fy - B[0, 2]*(Fx**2)/l

    K = np.array([[Fx, g, Cx], [0, Fy, Cy], [0, 0, 1]])

    inv_K = np.linalg.inv(K)
    r1_r2_t = produit_matriciel(inv_K, H)

    R1 = produit_matriciel(inv_K, H[:, 0])
    R2 = produit_matriciel(inv_K, H[:, 1])
    T = produit_matriciel(inv_K, H[:, 2])

    r1 = l*R1
    r2 = l*R2
    r3 = produit_matriciel(r1, r2)
    T = l*T

    R = np.array([r1, r2, r3]).T

    return K, R, T

def compute_v(hi, hj):
    return np.array([hi[0]*hj[0],
                     hi[0]*hj[1] + hi[1]*hj[0],
                     hi[1]*hj[1],
                     hi[2]*hj[0] + hi[0]*hj[2],
                     hi[2]*hj[1] + hi[1]*hj[2],
                     hi[2]*hj[2]])

def compute_V(lst_H):
    V = np.zeros((len(lst_H)*2, 1))
    for i in range(0, 2*len(lst_H), 2):
        h1 = lst_H[i/2][:, 0]
        h2 = lst_H[i/2][:, 1]

        v11 = compute_v(h1, h1)
        v12 = compute_v(h1, h2)
        v22 = compute_v(h1, h2)

        V[i, 0] = v12.T
        V[i+1, 0] = v11.T - v22.T

    return V