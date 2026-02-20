import numpy as np
import ast

K = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def write(matrice):
    with open("cameras/sauvegarde_matrice.csv", "w") as f:
        f.write(str(matrice.tolist()))


def read(line_number):
    with open("cameras/sauvegarde_matrice.csv", "r") as f:
        for i, line in enumerate(f):
            if i == line_number:
                return np.array(ast.literal_eval(line.strip()))
    return None  # si la ligne n'existe pas


write(K)
print(read(0))
