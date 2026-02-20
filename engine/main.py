"""Point d'entrée du moteur 3D Krafton : initialisation OpenGL/pygame et boucle principale."""

import logging
import pygame
from pathlib import Path
from OpenGL.GLU import *
from engine.opengl_3d_object import *
from engine.mathlib import *
from engine.dot_obj_parser import *
from engine import config

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

MODELS_DIR = Path(__file__).parent / "models"


def main():
    """Initialise la scène, la fenêtre OpenGL et lance la boucle d'événements."""

    all_objects = []
    camera = CAMERA(speed=config.CAMERA_SPEED)
    logger.info("Caméra initialisée (speed=%.3f)", config.CAMERA_SPEED)

    model_path = MODELS_DIR / config.MODEL_FILE
    logger.info("Chargement du modèle : %s", model_path)
    my_object_file = OBJ_FILE(str(model_path))
    try:
        my_object_file.parse(force_parse=True)  # Cache system not faster yet
    except FileNotFoundError:
        logger.warning("Modèle introuvable : %s", model_path)
    else:
        logger.info(
            "Modèle chargé — %d sommets, %d triangles, %d quads",
            len(my_object_file.vertices),
            len(my_object_file.triangles[0]),
            len(my_object_file.quads[0]),
        )
        my_object = FACES(
            to_be_drew=True,
            vertices=my_object_file.vertices,
            quads=my_object_file.quads,
            triangles=my_object_file.triangles,
            normals=my_object_file.normals,
            coordinates=[0, 0, 0],
        )
        all_objects.append(my_object)
    finally:
        del my_object_file  # Release some memory

    debug_axes = config.DEBUG_AXES
    if debug_axes:
        logger.debug("Axes de debug activés")
        axe_x = AXES(to_be_drew=True, vertices=[[0, 0, 0], [1, 0, 0]], color=[1, 0, 0])
        axe_y = AXES(to_be_drew=True, vertices=[[0, 0, 0], [0, 1, 0]], color=[0, 1, 0])
        axe_z = AXES(to_be_drew=True, vertices=[[0, 0, 0], [0, 0, 1]], color=[0, 0, 1])

        rotation_axe_x = ROTATION_AXES(
            to_be_drew=True,
            vertices=[
                (0.0, cos(radians(i)), sin(radians(i))) for i in range(0, 360, 1)
            ],
            color=[1, 0, 0],
        )
        rotation_axe_y = ROTATION_AXES(
            to_be_drew=True,
            vertices=[
                (cos(radians(i)), 0.0, sin(radians(i))) for i in range(0, 360, 1)
            ],
            color=[0, 1, 0],
        )
        rotation_axe_z = ROTATION_AXES(
            to_be_drew=True,
            vertices=[
                (cos(radians(i)), sin(radians(i)), 0.0) for i in range(0, 360, 1)
            ],
            color=[0, 0, 1],
        )
        all_objects.append(rotation_axe_x)
        all_objects.append(rotation_axe_y)
        all_objects.append(rotation_axe_z)
        all_objects.append(axe_x)
        all_objects.append(axe_y)
        all_objects.append(axe_z)

    pygame.init()
    # todo: changer le système de fenêtre par celui de opengl GLUT
    display = config.DISPLAY
    logger.info("Fenêtre pygame créée (%dx%d)", display[0], display[1])
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    glViewport(0, 0, display[0], display[1])
    glMatrixMode(GL_PROJECTION)
    gluPerspective(
        config.FOV, display[0] / display[1], config.CLIP_NEAR, config.CLIP_FAR
    )

    # light_ambient = [1.0, 1.0, 1.0, 1.0]
    # light_diffuse = [1.0, 1.0, 1.0, 1.0]
    # light_specular = [1.0, 1.0, 1.0, 1.0]
    # light_position = [100.0, 2.0, 1.0, 1.0]
    # glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    # glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    # glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # ______________Objects to be compiled_______
    logger.info("Compilation de %d objet(s) en display list…", len(all_objects))
    for object_to_be_compiled in all_objects:
        object_to_be_compiled.compile()
    logger.info("Compilation terminée.")
    # ___________________________________________

    # glFrontFace(GL_CW)
    # glCullFace(GL_BACK)
    # glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glClearColor(*config.BACKGROUND)

    # glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)

    clock = pygame.time.Clock()
    lastFps = 0
    selected = camera
    run = True
    something_changed = True
    logger.info("Boucle principale démarrée (FPS cible : %d)", config.FPS_TARGET)

    # _______________________________________________________Main Loop_______________________________________________________
    while run:
        clock.tick(config.FPS_TARGET)
        if something_changed:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            gluLookAt(
                camera.coordinates[0],
                camera.coordinates[1],
                camera.coordinates[2],
                camera.coordinates[0] + camera.front.x,
                camera.coordinates[1] + camera.front.y,
                camera.coordinates[2] + camera.front.z,
                camera.up.x,
                camera.up.y,
                camera.up.z,
            )

            # ______________Objects to be drew___________
            for object_to_be_drew in all_objects:
                if object_to_be_drew.to_be_drew:
                    object_to_be_drew.draw()
            # ____________________________________________
            pygame.display.flip()
            something_changed = False

            # print(camera.front.list, camera.up.list, camera.right.list)
            # print(camera.front.getLength(), camera.right.getLength(), camera.up.getLength())
        # print(clock.get_fps())

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected = camera
                    logger.debug("Sélection : caméra")
                if event.key == pygame.K_2:
                    selected = all_objects[0]
                    logger.debug("Sélection : objet 0")
                if event.key == pygame.K_3:
                    selected = all_objects[1]
                    logger.debug("Sélection : objet 1")
            if event.type == pygame.QUIT:
                logger.info("Événement QUIT reçu, arrêt.")
                run = False
                pygame.quit()
                quit()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            logger.info("ESCAPE pressé, arrêt.")
            run = False
            pygame.quit()
            quit()
        if pygame.key.get_pressed()[pygame.K_UP]:
            if isinstance(selected, CAMERA):
                selected.forward3D()
            else:
                selected.addCoordinates([0, 0, -config.OBJECT_MOVE_STEP])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if isinstance(selected, CAMERA):
                selected.backward3D()
            else:
                selected.addCoordinates([0, 0, config.OBJECT_MOVE_STEP])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if isinstance(selected, CAMERA):
                selected.left3D()
            else:
                selected.addCoordinates([-config.OBJECT_MOVE_STEP, 0, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if isinstance(selected, CAMERA):
                selected.right3D()
            else:
                selected.addCoordinates([config.OBJECT_MOVE_STEP, 0, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_c]:
            if isinstance(selected, CAMERA):
                selected.down3D()
            else:
                selected.addCoordinates([0, -config.OBJECT_MOVE_STEP, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if isinstance(selected, CAMERA):
                selected.up3D()
            else:
                selected.addCoordinates([0, config.OBJECT_MOVE_STEP, 0])
            something_changed = True

        if pygame.key.get_pressed()[pygame.K_z]:
            if isinstance(selected, CAMERA):
                selected.addPitch(config.OBJECT_ROTATE_STEP)
            else:
                selected.addRotation([-config.OBJECT_ROTATE_STEP, 0, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_s]:
            if isinstance(selected, CAMERA):
                selected.addPitch(-config.OBJECT_ROTATE_STEP)
            else:
                selected.addRotation([config.OBJECT_ROTATE_STEP, 0, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_q]:
            if isinstance(selected, CAMERA):
                selected.addYaw(config.OBJECT_ROTATE_STEP)
            else:
                selected.addRotation([0, -config.OBJECT_ROTATE_STEP, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_d]:
            if isinstance(selected, CAMERA):
                selected.addYaw(-config.OBJECT_ROTATE_STEP)
            else:
                selected.addRotation([0, config.OBJECT_ROTATE_STEP, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_a]:
            if isinstance(selected, CAMERA):
                selected.addRoll(-config.OBJECT_ROTATE_STEP)
            else:
                selected.addRotation([0, 0, config.OBJECT_ROTATE_STEP])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_e]:
            if isinstance(selected, CAMERA):
                selected.addRoll(config.OBJECT_ROTATE_STEP)
            else:
                selected.addRotation([0, 0, -config.OBJECT_ROTATE_STEP])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            if isinstance(selected, CAMERA):
                selected.reset()
            else:
                selected.rotation = [0, 0, 0]
                selected.coordinates = [0, 0, 0]
            something_changed = True


# _______________________________________________________________________________________________________________________
if __name__ == "__main__":
    main()
