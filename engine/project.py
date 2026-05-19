# Scene
debug_axes = False
debug_rotation_axes = False
objects = {
    #'Backpack' : {'type': 'Faces', 'path': 'Krafton/3d_models/scene/environnement.obj', 'coordinates': [30,10,0], 'color': None, 'to_be_drew': True},
    #'Environnement' : {'type': 'Faces', 'path': '3d_models/scene/environnement.obj', 'coordinates': [0,0,0], 'color': None, 'to_be_drew': True, "collide_box": None},
    'Block_1' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [0, 0, -30], 'color': None, "collide_box": [[0,0,0],[1,1,1]]},
    'Block_2' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [10, 0, -30], 'color': None, "collide_box": [[0,0,0],[1,1,1]]},
    'Block_3' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [20, 0, -30], 'color': None, "collide_box": [[0,0,0],[1,1,1]]},
    'Block_4' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [30, 0, -30], 'color': None, "collide_box": [[0,0,0],[1,1,1]]},
    'left_controller' : {'type': 'Faces', 'path': '3d_models/scene/Saber.obj', 'coordinates': [0, 0, 0], 'color': None, "collide_box": [[0,0,0],[0.5,2,0.5]]},
    'right_controller' : {'type': 'Faces', 'path': '3d_models/scene/Saber.obj', 'coordinates': [10, 0, 0], 'color': None, "collide_box": [[0,0,0],[0.5,2,0.5]]}
}

# Animation
animation = {
    'ToZero': {'goto': [0,0,0], 'time': 300}
}

# Display
display = [1920, 1080]
fpsLimit = 144

# Projection
fov = 45
near_plane = 1
far_plane = 500

# Déplacements
lockedAxe = None

# Jeux
temps_spawn_cube = 1000

# Cadre de la manette
pt1 = (10, 10, 10)
pt2 = (-10, -10, -10)