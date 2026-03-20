# Scene
debug_axes = True
debug_rotation_axes = True
objects = {
    #'Backpack' : {'type': 'Faces', 'path': 'Krafton/3d_models/scene/environnement.obj', 'coordinates': [30,10,0], 'color': None, 'to_be_drew': True},
    'Environnement' : {'type': 'Faces', 'path': '3d_models/scene/environnement.obj', 'coordinates': [0,0,0], 'color': None, 'to_be_drew': True},
    'Block_1' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [0,0,0], 'color': None, 'to_be_drew': True},
    'Block_2' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [0,0,0], 'color': None, 'to_be_drew': True},
    'Block_3' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [0,0,0], 'color': None, 'to_be_drew': True},
    'Block_4' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [0,0,0], 'color': None, 'to_be_drew': True},
    'Manette_1' : {'type': 'Faces', 'path': '3d_models/scene/Saber.obj', 'coordinates': [0,0,0], 'color': None, 'to_be_drew': True},
    'Manette_2' : {'type': 'Faces', 'path': '3d_models/scene/Saber.obj', 'coordinates': [0,0,0], 'color': None, 'to_be_drew': True}
}

# Animation
animation = {
    'ToZero': {'goto': [0,0,0], 'time': 300}
}

# Display
display = [1920//2, 1080//2]
fpsLimit = 144

# Projection
fov = 45
near_plane = 1
far_plane = 500

# Déplacements
lockedAxe = None

# Jeux
temps_spawn_cube = 1000