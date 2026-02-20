import numpy as np
from write_read_csv import read



'''
pour utilisateur
'''

'''
fin pour utilisateur
'''

# Configuration touche clavier
quitter = 'q'

# Mode configuration
take_photo = 'p'

'''
images.py
'''

# Blob detection params
minThreshold = 10
maxThreshold = 200
filterByColor = True
blobColor = 255
filterByArea = True
minArea = 1

# Groupes de leds
distance_max = 50
distance_max_carre = distance_max**2

# Analyse image
kernel = np.ones((3,3), np.uint8)

'''
fin images.py
'''



'''
configuration_camera.py
'''

# dimension chessboard (en carres), dimension carre (en mm)
checkboard_info = [(6, 8), 22]
nb_photo_max = 15
object_points_list_2D = [[i, j] for i in range(checkboard_info[0][0]) for j in range(checkboard_info[0][1])]
object_points_list_3D = [[x*checkboard_info[1], y*checkboard_info[1], 0] for y in range(checkboard_info[0][0]) for x in range(checkboard_info[0][1])]
K1 = read('K1')
K2 = read('K2')
R1 = read('R1')
R2 = read('R2')
T1 = read('T1')
T2 = read('T2')
H1 = read('H1')
H2 = read('H2')

'''
fin configuration_camera.py
'''