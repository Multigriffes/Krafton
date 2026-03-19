from multiprocessing.shared_memory import ShareableList
import pygame
from OpenGL.GLU import *
from render_object import *
from mathlib import *
from dot_obj_parser import *
import project


def main():

    all_objects=[]
    camera=CAMERA()

    for object_to_be_created in project.objects:
        object_file = OBJ_FILE(object_to_be_created['path'])
        try:
            object_file.parse(force_parse=True)# Cache system not faster yet
        except FileNotFoundError:
            pass
        else:
            match object_to_be_created['type']:
                case 'Faces':
                    my_object=FACES(to_be_drew=True,vertices=object_file.vertices,quads=object_file.quads,triangles=object_file.triangles,normals=object_file.normals,coordinates=object_to_be_created['coordinates'])
                    all_objects.append(my_object)
                case 'Vertices':
                    my_object=VERTICES(to_be_drew=True,vertices=object_file.vertices,normals=object_file.normals,coordinates=object_to_be_created['coordinates'])
                    all_objects.append(my_object)
        finally:
            del object_file # Release some memory

    if project.debug_axes: # Création des axes en créant des lignes à deux points
        axe_x=AXES(to_be_drew=True,vertices=[[0, 0, 0], [1, 0, 0]], color=[1, 0, 0])
        axe_y=AXES(to_be_drew=True,vertices=[[0, 0, 0], [0, 1, 0]], color=[0, 1, 0])
        axe_z=AXES(to_be_drew=True,vertices=[[0, 0, 0], [0, 0, 1]], color=[0, 0, 1])
        all_objects.append(axe_x)
        all_objects.append(axe_y)
        all_objects.append(axe_z)

    if project.debug_rotation_axes: # Création des axes de rotation à partir des sin et cos
        rotation_axe_x=ROTATION_AXES(to_be_drew=True,vertices=[(0.0, cos(radians(i)), sin(radians(i))) for i in range(0, 360, 1)], color=[1, 0, 0])
        rotation_axe_y=ROTATION_AXES(to_be_drew=True,vertices=[(cos(radians(i)), 0.0, sin(radians(i))) for i in range(0, 360, 1)], color=[0, 1, 0])
        rotation_axe_z=ROTATION_AXES(to_be_drew=True,vertices=[(cos(radians(i)), sin(radians(i)), 0.0) for i in range(0, 360, 1)], color=[0, 0, 1])
        all_objects.append(rotation_axe_x)
        all_objects.append(rotation_axe_y)
        all_objects.append(rotation_axe_z)


    pygame.init()
    pygame.display.set_mode(project.display, pygame.DOUBLEBUF|pygame.OPENGL)
    glViewport(0,0, project.display[0], project.display[1])
    glMatrixMode(GL_PROJECTION)
    gluPerspective(project.fov, project.display[0]/project.display[1], project.near_plane, project.far_plane)


    #light_ambient = [1.0, 1.0, 1.0, 1.0]
    #light_diffuse = [1.0, 1.0, 1.0, 1.0]
    #light_specular = [1.0, 1.0, 1.0, 1.0]
    #light_position = [100.0, 2.0, 1.0, 1.0]
    #glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    #glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    #glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    #glLightfv(GL_LIGHT0, GL_POSITION, light_position)


    #______________Objects to be compiled_______
    for object_to_be_compiled in all_objects:
        object_to_be_compiled.compile()
    #___________________________________________


    #glFrontFace(GL_CW)
    #glCullFace(GL_BACK)
    #glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0,100/255,0,1)

    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)

    clock=pygame.time.Clock()
    selected = camera
    run = True
    something_changed = True

#_______________________________________________________Main Loop_______________________________________________________
    while run:
        timeSinceLastFrame = clock.tick(project.fpsLimit)
        if something_changed:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            gluLookAt(
                camera.coordinates[0], camera.coordinates[1], camera.coordinates[2],
                camera.coordinates[0] + camera.front_vec.x, camera.coordinates[1] + camera.front_vec.y, camera.coordinates[2] + camera.front_vec.z,
                camera.up_vec.x, camera.up_vec.y, camera.up_vec.z
            )


        #______________Objects to be drew___________
            for object in all_objects:
                if object.to_be_drew:
                    object.draw()
        #____________________________________________
            pygame.display.flip()
            something_changed=False

            #print(camera.front_vec.list, camera.right_vec.list, camera.up_vec.list)
            #print(camera.front_vec.getLengthNoSqrt(), camera.right_vec.getLengthNoSqrt(), camera.up_vec.getLengthNoSqrt())
        #print(clock.get_fps())

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected = camera
                if event.key == pygame.K_2:
                    selected = all_objects[0]
                if event.key == pygame.K_3:
                    selected = all_objects[1]
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            quit()
        if pygame.key.get_pressed()[pygame.K_UP]:
            if isinstance(selected, CAMERA):
                selected.moveForward(locked_axe=project.lockedAxe)
            else:
                selected.addCoordinates([0, 0, -0.05])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if isinstance(selected, CAMERA):
                selected.moveBackward(locked_axe=project.lockedAxe)
            else:
                selected.addCoordinates([0, 0, 0.05])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if isinstance(selected, CAMERA):
                selected.moveLeft(locked_axe=project.lockedAxe)
            else:
                selected.addCoordinates([-0.05, 0, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if isinstance(selected, CAMERA):
                selected.moveRight(locked_axe=project.lockedAxe)
            else:
                selected.addCoordinates([0.05, 0, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_c]:
            if isinstance(selected, CAMERA):
                selected.moveDown(locked_axe=project.lockedAxe)
            else:
                selected.addCoordinates([0, -0.05, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if isinstance(selected, CAMERA):
                selected.moveUp(locked_axe=project.lockedAxe)
            else:
                selected.addCoordinates([0, 0.05, 0])
            something_changed = True

        if pygame.key.get_pressed()[pygame.K_z]:
            if isinstance(selected, CAMERA):
                selected.addPitch(1)
            else:
                selected.addRotation([-1, 0, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_s]:
            if isinstance(selected, CAMERA):
                selected.addPitch(-1)
            else:
                selected.addRotation([1, 0, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_q]:
            if isinstance(selected, CAMERA):
                selected.addYaw(1)
            else:
                selected.addRotation([0, -1, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_d]:
            if isinstance(selected, CAMERA):
                selected.addYaw(-1)
            else:
                selected.addRotation([0, 1, 0])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_a]:
            if isinstance(selected, CAMERA):
                selected.addRoll(-1)
            else:
                selected.addRotation([0, 0, 1])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_e]:
            if isinstance(selected, CAMERA):
                selected.addRoll(1)
            else:
                selected.addRotation([0, 0, -1])
            something_changed = True
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            if isinstance(selected, CAMERA):
                selected.reset()
            something_changed = True


#_______________________________________________________________________________________________________________________
main()
