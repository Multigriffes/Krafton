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

def triangulate_parallel(p1, p2, K, B):
    """
    triangulation dans le cas ou les caméras sont parallèles
    """
    
    u1, v1 = p1
    u2, v2 = p2
    
    f, cx, cy = K
    
    disparity = u1 - u2
    
    if disparity == 0:
        return None  # profondeur infinie
    
    Z = f * B / disparity
    
    X = Z * (u1 - cx) / f
    Y = Z * (v1 - cy) / f
    
    return (X, Y, Z)

def rotation_matrix_x(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ])

def rectify_cameras(K1, R1, T1, K2, R2, T2):
    """
    Calcule les homographies H1 et H2
    permettant de rectifier les deux images.
    """

    C1 = produit_scalaire(-R1.T, T1)
    C2 = produit_scalaire(-R2.T, T2)

    baseline = C2 - C1
    x_new = baseline / np.linalg.norm(baseline)

    z1 = produit_scalaire(R1.T, np.array([0, 0, 1]))
    z2 = produit_scalaire(R2.T, np.array([0, 0, 1]))
    z_new = (z1 + z2) / 2
    z_new = z_new / np.linalg.norm(z_new)

    y_new = np.cross(z_new, x_new)
    y_new = y_new / np.linalg.norm(y_new)

    z_new = np.cross(x_new, y_new)

    R_rect = np.vstack((x_new, y_new, z_new)).T

    H1 = produit_scalaire(produit_scalaire(produit_scalaire(K1, R_rect), R1.T), np.linalg.inv(K1))
    H2 = produit_scalaire(produit_scalaire(produit_scalaire(K2, R_rect), R2.T), np.linalg.inv(K2))

    return H1, H2

def compute_homography(obj_pts, img_pts):
    N = obj_pts.shape[0]
    A = []

    for i in range(N):
        X, Y = obj_pts[i]
        u, v = img_pts[i]

        A.append([-X, -Y, -1, 0, 0, 0, u*X, u*Y, u])
        A.append([0, 0, 0, -X, -Y, -1, v*X, v*Y, v])

    A = np.array(A)

    # SVD
    U, S, Vt = np.linalg.svd(A)
    h = Vt[-1]

    H = h.reshape(3,3)
    return H / H[2,2]

def build_v_ij(H, i, j):
    return np.array([
        H[0,i]*H[0,j],
        H[0,i]*H[1,j] + H[1,i]*H[0,j],
        H[1,i]*H[1,j],
        H[2,i]*H[0,j] + H[0,i]*H[2,j],
        H[2,i]*H[1,j] + H[1,i]*H[2,j],
        H[2,i]*H[2,j]
    ])

def compute_intrinsics(object_points_list, image_points_list):
    """
    object_points_list : liste de Nx2
    image_points_list  : liste de Nx2
    """

    H_list = []

    # 1. Calcul des homographies
    for obj_pts, img_pts in zip(object_points_list, image_points_list):
        H = compute_homography(obj_pts, img_pts)
        H_list.append(H)

    # 2. Construction matrice V
    V = []

    for H in H_list:
        v12 = build_v_ij(H, 0, 1)
        v11 = build_v_ij(H, 0, 0)
        v22 = build_v_ij(H, 1, 1)

        V.append(v12)
        V.append(v11 - v22)

    V = np.array(V)

    # 3. Résolution Vb = 0
    U, S, Vt = np.linalg.svd(V)
    b = Vt[-1]

    # 4. Reconstruction de B
    B11, B12, B22, B13, B23, B33 = b

    # 5. Extraction paramètres
    v0 = (B12*B13 - B11*B23) / (B11*B22 - B12**2)

    lambda_ = B33 - (B13**2 + v0*(B12*B13 - B11*B23)) / B11

    fx = np.sqrt(lambda_ / B11)
    fy = np.sqrt(lambda_ * B11 / (B11*B22 - B12**2))
    cx = -B13 / B11
    cy = v0

    K = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]
    ])

    return K