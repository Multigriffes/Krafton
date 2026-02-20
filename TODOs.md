# TODOs

## Tâches ouvertes

- `engine/main.py:70` — Migrer le système de fenêtre de pygame vers GLUT
- `cameras/images.py:17` — Écrire la fonction de traitement d'image pour les captures 1 et 2

## Code commenté à décider (garder ou supprimer)

### Éclairage OpenGL (`engine/main.py` + `engine/opengl_3d_object.py`)
Tout le système d'éclairage fixe (`GL_LIGHT0`, `glMaterialfv`, `glNormal3fv`) est commenté.
Lignes concernées : `main.py:79-86`, `main.py:99-100`, `opengl_3d_object.py:7-10`, `:101-105`, `:116`, `:121-125`, `:136`

### Face culling (`engine/main.py:93-95`)
`glFrontFace`, `glCullFace`, `glEnable(GL_CULL_FACE)` désactivés.

### Prints de debug (`engine/main.py:136-138`)
Logs des vecteurs front/up/right et du FPS.

### Cache OBJ désactivé (`engine/dot_obj_parser.py:102`)
`self.writeToCache()` commenté — le système de cache n'est pas encore plus rapide que le parsing direct.

### Classe `VEC3` abandonnée (`engine/mathlib.py:77-88`)
Remplacée par les quaternions. Peut être supprimée.

### Méthode `__invert__` (`engine/mathlib.py:57-58`)
Prototype commenté sur `QUATERNION`.

### Conversion BGR→GRAY (`cameras/configuration_camera.py:14`)
`cv2.cvtColor` commenté dans la boucle de calibration.
