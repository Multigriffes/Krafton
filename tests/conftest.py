"""Configuration pytest : ajout de cameras/ au chemin d'import."""

import sys
import os

# Les scripts caméra utilisent des imports directs (from parameters import *).
# On ajoute cameras/ au sys.path pour que pytest puisse les résoudre.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cameras"))
