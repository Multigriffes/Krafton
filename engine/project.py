# Scene
debug_axes = True
debug_rotation_axes = True
objects = [
    {'type': 'Faces', 'path': 'C:/Users/Multi/Documents/GitHub/Krafton/engine/models/backpack.obj', 'coordinates': [30,10,0], 'color': None, 'to_be_drew': True},
    {'type': 'Faces', 'path': 'C:/Users/Multi/Documents/GitHub/Krafton/3d_models/scene/environnement.obj', 'coordinates': [0,0,0], 'color': None, 'to_be_drew': True},
]

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