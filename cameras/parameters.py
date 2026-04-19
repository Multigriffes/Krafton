import numpy as np
from cameras.write_read_csv import read

'''
pour utilisateur
'''
# Configuration touche clavier
quitter = 'q'

# Mode configuration
take_photo = 'p'
'''
fin pour utilisateur
'''

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
nb_groupe = 2

# Nombre leds par manette
nb_led_left_controller = 4
nb_led_right_controller = 3

# Analyse image
kernel = np.ones((3,3), np.uint8)

'''
fin images.py
'''



'''
configuration_camera.py
'''

# dimension chessboard (en carres), dimension carre (en mm)
chessboard_info = [(6, 8), 22]
nb_photo_max = 15
cols, rows = chessboard_info[0]
square = chessboard_info[1]

object_points_list = [
    [j * square, i * square]
    for i in range(rows)
    for j in range(cols)
]

K1 = read('K1')
K2 = read('K2')
R = read('R')
R1 = read('R1')
R2 = read('R2')
t = read('t')
t1 = read('t1')
t2 = read('t2')
P1 = read('P1')
P2 = read('P2')

'''
fin configuration_camera.py
'''