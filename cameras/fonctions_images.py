import cv2

def groupe_leds(point_list:list)->list:
    '''
    Forme les groupes de leds detectes a partir de leur coordonnees 2D
    '''
    point_visite = [1 for i in range(len(point_list))] # 1 pour point non visite, 0 sinon
    liste_groupe = []
    for i, point in enumerate(point_list):
        if point_visite[i]:
            groupe = []
            cluster_recur(i, point, groupe, point_visite, point_list)
            liste_groupe.append(groupe)

    return liste_groupe


def cluster_recur(index_point_depart:int, point_depart:tuple, cluster:list, point_visite:list, point_list:list):
    '''
    Fonction récursive qui forme un groupe de points en partant d'un point de départ
    '''
    from cameras.parameters import distance_max_carre

    point_visite[index_point_depart] = 0
    cluster.append(point_depart)
    for i, point in enumerate(point_list):
        if point_visite[i]:
            distance_carre = (point_depart[0]-point[0])**2 + (point_depart[1]-point[1])**2
            if distance_carre < distance_max_carre:
                cluster_recur(i, point, cluster, point_visite, point_list)

def blob_detection_params():
    '''
    Creation d'un objet de detection de blob lumineux
    '''
    import cv2
    from cameras.parameters import minThreshold, maxThreshold, filterByColor, blobColor, filterByArea, minArea

    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = minThreshold
    params.maxThreshold = maxThreshold
    params.filterByColor = filterByColor
    params.blobColor = blobColor
    params.filterByArea = filterByArea
    params.minArea = minArea

    detector = cv2.SimpleBlobDetector_create(params)
    return detector

def produit_matriciel(mat_1, mat_2):
    '''
    Fonction qui calcul le produit matriciel entre deux matrices (mat_1 et mat2)
    '''
    
    import numpy as np

    if mat_1.shape[1] != mat_2.shape[0]:
        raise ValueError("Dimensions incompatibles pour le produit matriciel")
    
    n, p = mat_1.shape
    n2, p2 = mat_2.shape
    
    mat = np.zeros((n, p2))
    
    for i in range(n):
        for j in range(p2):
            mat[i, j] = sum(mat_1[i, k] * mat_2[k, j] for k in range(p))
    
    return mat

def compute_A(lst_points_realite, lst_points_image):
    '''
    Cree la matrice A a partir des points detectes lors de la calibration de la camera
    '''
    import numpy as np

    n = len(lst_points_realite)
    A = np.zeros((2*n, 9))

    for i in range(n):
        X, Y = lst_points_realite[i]
        u, v = lst_points_image[i]

        A[2*i] = [-X, -Y, -1, 0, 0, 0, u*X, u*Y, u]
        A[2*i+1] = [0, 0, 0, -X, -Y, -1, v*X, v*Y, v]

    return A

def compute_homography(lst_images, object_points):
    '''
    Calcul des matrices H d'homographie pour chaque images.
    '''
    import numpy as np

    lst_H = []

    for image_points in lst_images:

        img_norm, T_img = normalize_points(image_points)
        obj_norm, T_obj = normalize_points(object_points)

        A = compute_A(obj_norm, img_norm)

        U, S, Vt = np.linalg.svd(A)
        h = Vt[-1]
        H_norm = h.reshape(3,3)

        H = produit_matriciel(np.linalg.inv(T_img),
                              produit_matriciel(H_norm, T_obj))

        H = H / H[2,2]

        lst_H.append(H)

    return lst_H

def compute_intrinsincs(B):
    '''
    Calcule les paramètres intrinsèques de la camera et renvoie la matrice intrinsèque.
    '''
    import numpy as np
    from math import sqrt

    Cy = (B[0, 1]*B[0, 2] - B[0, 0]*B[1, 2])/(B[0, 0]*B[1, 1] - B[0, 1]**2)
    l = B[2, 2] - (B[0, 2]**2 + Cy*(B[0, 1]*B[0, 2] - B[0, 0]*B[1, 2]))/B[0, 0]
    Fx = sqrt(l/B[0, 0])
    Fy = sqrt(l*B[0, 0]/(B[0, 0]*B[1, 1] - B[0, 1]**2))
    g = -B[0, 1]*(Fx**2)*Fy/l
    Cx = g*Cy/Fy - B[0, 2]*(Fx**2)/l

    K = np.array([[Fx, g, Cx],
                  [0, Fy, Cy],
                  [0, 0, 1]])

    return K

def compute_v(hi, hj):
    '''
    Calcul de la matrice v qui composeras V
    '''
    import numpy as np

    return np.array([hi[0]*hj[0],
                     hi[0]*hj[1] + hi[1]*hj[0],
                     hi[1]*hj[1],
                     hi[2]*hj[0] + hi[0]*hj[2],
                     hi[2]*hj[1] + hi[1]*hj[2],
                     hi[2]*hj[2]])

def compute_V(lst_H):
    '''
    Calcul de la matrice V formé par des matrices v qui permettras par SVD de calculer B
    '''
    import numpy as np

    V = np.zeros((2*len(lst_H), 6))
    for i in range(len(lst_H)):
        h1 = lst_H[i][:, 0]
        h2 = lst_H[i][:, 1]

        v11 = compute_v(h1, h1)
        v12 = compute_v(h1, h2)
        v22 = compute_v(h2, h2)

        V[2*i] = v12
        V[2*i+1] = v11.T - v22.T

    return V

def compute_B(V):
    '''
    Calcul de B par SVD de V. Cette matrice sert a former les parametres intrinseques de la camera. 
    '''
    import numpy as np

    U, S, Vt = np.linalg.svd(V)
    b = Vt[-1]
    B11, B12, B22, B13, B23, B33 = b
    B = np.array([[B11, B12, B13],
                  [B12, B22, B23],
                  [B13, B23, B33]])
    
    if B[0,0] < 0:
        B = -B
    
    return B

def compute_extrinsics(K, H):
    '''
    Calcul de la matrice extrinseque R d'une camera a partir de sa matrice intrinseque (K) et de H.
    '''
    import numpy as np

    inv_K = np.linalg.inv(K)

    h1 = H[:,0].reshape(3,1)
    h2 = H[:,1].reshape(3,1)
    h3 = H[:,2].reshape(3,1)

    r1 = produit_matriciel(inv_K, h1)
    l = 1 / np.linalg.norm(r1)
    r1 = l * r1

    r2 = l * produit_matriciel(inv_K, h2)
    r3 = np.cross(r1.flatten(), r2.flatten()).reshape(3,1)

    t = l * produit_matriciel(inv_K, h3)

    R = np.column_stack((r1.flatten(), r2.flatten(), r3.flatten()))

    U, _, Vt = np.linalg.svd(R)
    R = produit_matriciel(U, Vt)

    return R, t.flatten()

def normalize_points(points):
    '''
    Normalisation des points pour obtenir des valeurs plus facile a traiter.
    '''
    import numpy as np
    from math import sqrt

    n = len(points)
    points = np.array(points)

    mean_x = np.mean(points[:,0])
    mean_y = np.mean(points[:,1])

    translated = points - np.array([mean_x, mean_y])

    dist = np.sqrt(translated[:,0]**2 + translated[:,1]**2)
    mean_dist = np.mean(dist)

    s = np.sqrt(2) / mean_dist

    T = np.array([
        [s, 0, -s*mean_x],
        [0, s, -s*mean_y],
        [0, 0, 1]
    ])

    points_h = np.column_stack((points, np.ones(n))).T
    normalized = produit_matriciel(T, points_h)

    normalized = normalized[:2].T

    return normalized, T

def compute_stereo_extrinsecs(extrinsics1, extrinsics2):
    import numpy as np

    R_list = []
    t_list = []

    for (R1, t1), (R2, t2) in zip(extrinsics1, extrinsics2):
        R12 = produit_matriciel(R2, R1.T)
        t12 = t2 - produit_matriciel(R12, t1.reshape(3,1)).flatten()
        R_list.append(R12)
        t_list.append(t12.reshape(3,))

    t_mean = np.mean(np.array(t_list), axis=0)

    R_stack = np.mean(R_list, axis=0)
    U, _, Vt = np.linalg.svd(R_stack)
    R_mean = produit_matriciel(U, Vt)


    if np.linalg.det(R_mean) < 0:
        R_mean = -R_mean

    return R_mean, t_mean


def compute_projection_matrices(K1, K2, R, t):
    '''
    Formation des matrices de projection des deux cameras pour former des droites qui nous permettent de determiner la position
    3D d'un point
    '''
    import numpy as np

    P1 = K1 @ np.hstack((np.eye(3), np.zeros((3,1))))
    P2 = K2 @ np.hstack((R, t.reshape(3,1)))

    return P1, P2

def triangulate_point(P1, P2, pt1, pt2):
    '''
    Triangulation d'un point 3D à partir de deux observations image.
    
    P1 : matrice projection camera 1 (3x4)
    P2 : matrice projection camera 2 (3x4)
    pt1 : (u1,v1)
    pt2 : (u2,v2)

    retourne : (X,Y,Z)
    '''

    import numpy as np

    u1, v1 = pt1
    u2, v2 = pt2

    A = np.array([
        u1 * P1[2] - P1[0],
        v1 * P1[2] - P1[1],
        u2 * P2[2] - P2[0],
        v2 * P2[2] - P2[1]
    ])

    # résolution AX = 0 par SVD
    U, S, Vt = np.linalg.svd(A)

    print(f"Condition A : {np.linalg.cond(A):.1f}")  # Si > 1000 : matrice mal conditionnée

    X = Vt[-1]

    # passage homogène -> cartésien
    X = X / X[3]

    return X[:3]

def calculate_point_pos(lst_pts):
    lenght = len(lst_pts)
    x, y, z = (0, 0, 0)
    for pts in lst_pts:
        x += float(pts[0])
        y += float(pts[1])
        z += float(pts[2])

    return x/lenght, y/lenght, z/lenght

def centre(groupe):
    x = sum(p[0] for p in groupe) / len(groupe)
    y = sum(p[1] for p in groupe) / len(groupe)
    return (x, y)

def trier_groupe(groupe):
    return sorted(groupe, key=lambda p: (p[0], p[1]))

def image_transform(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def detect_and_processed_controller_pos(frame1_processed, frame2_processed, detector):
    from cameras.parameters import P1, P2, nb_led_left_controller, nb_led_right_controller

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
        manette = None
        for pos in pos_groupes:
            if len(pos) == 0:
                continue

            pos_manette = calculate_point_pos(pos)

            if len(pos) == nb_led_left_controller:
                manette = 'left'
            elif len(pos) == nb_led_right_controller:
                manette = 'right'

        return {'pos': pos_manette, 'nom': manette}, keypoints1, keypoints2

    return False