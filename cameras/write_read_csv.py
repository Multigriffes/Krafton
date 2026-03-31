import numpy as np
import ast

def write(name, data):
    if isinstance(data, np.ndarray):
        data = data.tolist()

    new_line = f"{name}:{data}\n"

    with open('sauvegarde_matrice.csv', 'a') as f:
        f.write(new_line)

def read(name):
    with open('sauvegarde_matrice.csv', 'r') as f:
        for line in f:
            if line.startswith(name + ":"):
                data_str = line.split(":", 1)[1].strip()
                data = ast.literal_eval(data_str)

                # Si matrice → reconvertir en numpy
                if isinstance(data, list) and all(isinstance(row, list) for row in data):
                    return np.array(data)

                return data
    return None

def clear_file():
    open('sauvegarde_matrice.csv', 'w').close()