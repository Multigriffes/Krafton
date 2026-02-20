import numpy as np



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
object_points_list = [[i, j] for i in range(checkboard_info[0][0]) for j in range(checkboard_info[0][1])]

'''
fin configuration_camera.py
'''