# Scene
debug_axes = False
debug_rotation_axes = False
objects = {
    'Block_1' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [0, 0, -30], 'color': None, "collide_box": [[0,0,0],[1,1,1]]},
    'Block_2' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [10, 0, -30], 'color': None, "collide_box": [[0,0,0],[1,1,1]]},
    'Block_3' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [20, 0, -30], 'color': None, "collide_box": [[0,0,0],[1,1,1]]},
    'Block_4' : {'type': 'Faces', 'path': '3d_models/scene/Block.obj', 'coordinates': [30, 0, -30], 'color': None, "collide_box": [[0,0,0],[1,1,1]]},
    'left_controller' : {'type': 'Faces', 'path': '3d_models/scene/Saber.obj', 'coordinates': [0, 0, 0], 'color': None, "collide_box": [[0,0,0],[0.5,2,0.5]]},
    'right_controller' : {'type': 'Faces', 'path': '3d_models/scene/Saber.obj', 'coordinates': [10, 0, 0], 'color': None, "collide_box": [[0,0,0],[0.5,2,0.5]]}
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

# Cadre de la manette
pt1 = (10, 10, 10)
pt2 = (-10, -10, -10)