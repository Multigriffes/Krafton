from parameters import *
import cv2

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

def produit_scalaire(mat_1: np.array, mat_2: np.array) -> np.array:
    if mat_1.shape[1] != mat_2.shape[0]:
        raise ValueError("Dimensions incompatibles pour le produit matriciel")
    
    n, p = mat_1.shape
    n2, p2 = mat_2.shape
    
    mat = np.zeros((n, p2))
    
    for i in range(n):
        for j in range(p2):
            mat[i, j] = sum(mat_1[i, k] * mat_2[k, j] for k in range(p))
    
    return mat