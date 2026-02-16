import numpy as np
from fonctions_images import *

x = np.array([[1, 4], [3, 2]])
y = np.array([[-7, 2], [1, 0]])

z = produit_scalaire(x,y)
print(z)