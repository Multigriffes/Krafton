"""Persistance de matrices NumPy dans un fichier CSV (sauvegarde_matrice.csv)."""

import numpy as np
import ast

K = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def write(matrice):
    """Sauvegarde une matrice NumPy sous forme de liste Python dans le CSV."""
    with open("cameras/sauvegarde_matrice.csv", "w") as f:
        f.write(str(matrice.tolist()))


def read(line_number):
    """Lit et retourne la matrice à la ligne donnée du CSV, ou None si absente."""
    with open("cameras/sauvegarde_matrice.csv", "r") as f:
        for i, line in enumerate(f):
            if i == line_number:
                return np.array(ast.literal_eval(line.strip()))
    return None  # si la ligne n'existe pas


write(K)
print(read(0))
