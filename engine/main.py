from engine import *
import pygame
from OpenGL.GLU import *
from math import cos,sin,radians
from objparser import *





def main():
    axe_X=AXES(vertices=[[0,0,0],[1,0,0]],color=[1,0,0])
    axe_Y=AXES(vertices=[[0,0,0],[0,1,0]],color=[0,1,0])
    axe_Z=AXES(vertices=[[0,0,0],[0,0,1]],color=[0,0,1])

    rotation_axe_X=ROTATION_AXES(vertices=[(0.0,cos(radians(i)),sin(radians(i))) for i in range(0,360,1)],color=[1,0,0])
    rotation_axe_Y=ROTATION_AXES(vertices=[(cos(radians(i)),0.0,sin(radians(i))) for i in range(0,360,1)],color=[0,1,0])
    rotation_axe_Z=ROTATION_AXES(vertices=[(cos(radians(i)),sin(radians(i)),0.0) for i in range(0,360,1)],color=[0,0,1])

    all_objects=[]
    camera=CAMERA()

    my_object_file = OBJ_FILE('engine/models/theiere.obj')
    my_object_file.parse(forceParse=True)# Cache system not faster yet

    my_object=FACES(vertices=my_object_file.vertices,quads=my_object_file.quads,triangles=my_object_file.triangles,normals=my_object_file.normals,coordinates=[0,0,0])

    all_objects.append(my_object)

    #sol = [[FACES(vertices=my_object_file.vertices,quads=my_object_file.quads,triangles=my_object_file.triangles,normals=my_object_file.normals,coordinates=[i,0,-j]) for i in range(-1000,1000)] for j in range(-1000,1000)]
    #for i in range(len(sol)):
    #    for j in range(len(sol[i])):
    #        all_objects.append(sol[i][j])


    #my_object_file2 = OBJ_FILE('engine/models/backpack.obj')
    #my_object_file2.parse(forceParse=True)

    #my_object2=FACES(vertices=my_object_file2.vertices,quads=my_object_file2.quads,triangles=my_object_file2.triangles,normals=my_object_file2.normals,coordinates=[0,0,0])

    #all_objects.append(my_object2)

    debug_axes=True
    if debug_axes:
        all_objects.append(rotation_axe_X)
        all_objects.append(rotation_axe_Y)
        all_objects.append(rotation_axe_Z)
        all_objects.append(axe_X)
        all_objects.append(axe_Y)
        all_objects.append(axe_Z)


    pygame.init()
    # todo: changer le systeme de fenetre par celui de opengl GLUT
    display = [1920,1080]
    pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)
    glViewport(0,0,display[0],display[1])
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45,display[0]/display[1], 1, 500)


    #light_ambient = [1.0, 1.0, 1.0, 1.0]
    #light_diffuse = [1.0, 1.0, 1.0, 1.0]
    #light_specular = [1.0, 1.0, 1.0, 1.0]
    #light_position = [100.0, 2.0, 1.0, 1.0]
    #glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    #glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    #glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    #glLightfv(GL_LIGHT0, GL_POSITION, light_position)


    #______________Objects to be compiled_______
    for object in all_objects:
        object.compile()
    #___________________________________________


    #glFrontFace(GL_CW)
    #glCullFace(GL_FRONT)
    #glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0,100/255,0,1)

    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)

    clock=pygame.time.Clock()
    lastFps = 0
    selected = camera
    run = True

#_______________________________________________________Main Loop_______________________________________________________
    while run:
        clock.tick(144)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glTranslatef(
            -camera.coordinates[0],
            -camera.coordinates[1],
            -camera.coordinates[2]
            )
        glRotatef(-camera.rotation[0],1,0,0)
        glRotatef(-camera.rotation[1],0,1,0)
        glRotatef(-camera.rotation[2],0,0,1)

        #______________Objects to be drew___________
        for object in all_objects:
            object.draw()
        #____________________________________________



        pygame.display.flip()
        #print(clock.get_fps())

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected = camera
                if event.key == pygame.K_2:
                    selected = all_objects[0]
                if event.key == pygame.K_3:
                    selected = all_objects[1]
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            quit()
        if pygame.key.get_pressed()[pygame.K_UP]:
                selected.add_coordinates([0,0,-0.05])
        if pygame.key.get_pressed()[pygame.K_DOWN]:
                selected.add_coordinates([0,0,0.05])
        if pygame.key.get_pressed()[pygame.K_LEFT]:
                selected.add_coordinates([-0.05,0,0])
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
                selected.add_coordinates([0.05,0,0])
        if pygame.key.get_pressed()[pygame.K_i]:
                selected.add_coordinates([0,-0.05,0])
        if pygame.key.get_pressed()[pygame.K_u]:
                selected.add_coordinates([0,0.05,0])

        if pygame.key.get_pressed()[pygame.K_z]:
                selected.add_rotation([-1,0,0])
        if pygame.key.get_pressed()[pygame.K_s]:
                selected.add_rotation([1,0,0])
        if pygame.key.get_pressed()[pygame.K_q]:
                selected.add_rotation([0,-1,0])
        if pygame.key.get_pressed()[pygame.K_d]:
                selected.add_rotation([0,1,0])
        if pygame.key.get_pressed()[pygame.K_a]:
                selected.add_rotation([0,0,1])
        if pygame.key.get_pressed()[pygame.K_e]:
                selected.add_rotation([0,0,-1])
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            selected.rotation=[0,0,0]
            selected.coordinates=[0,0,0]


#_______________________________________________________________________________________________________________________
main()
