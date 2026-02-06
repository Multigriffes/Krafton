from engine import *
import pygame
from OpenGL.GLU import *
from math import cos,sin,radians
from objparser import *

#_______________________________________________________Main Loop_______________________________________________________

def main():
    pygame.init()
    # todo: changer le systeme de fenetre par celui de opengl GLUT
    display = [1920,1080]
    pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)


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

    gluPerspective(45,display[0]/display[1], 1, 500)
    glViewport(0,0,display[0],display[1])

    #glFrontFace(GL_CW)
    #glCullFace(GL_FRONT)
    #glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)

    clock=pygame.time.Clock()
    lastFps = 0
    selected = camera
    run = True

    while run:
        clock.tick(144)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #______________Objects to be drew___________
        for object in all_objects:
            object.draw()
        #____________________________________________
        pygame.display.flip()
        #print(clock.get_fps())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected = camera
                if event.key == pygame.K_2:
                    selected = my_object
                if event.key == pygame.K_3:
                    selected = my_object2
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            run = False
            pygame.quit()
            quit()
        if pygame.key.get_pressed()[pygame.K_UP]:
            if selected == camera:
                camera.add_coordinates([0,0,0.05])
                glTranslatef(0,0,0.05)
            else:
                selected.add_coordinates([0,0,-0.05])
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if selected == camera:
                camera.add_coordinates([0,0,-0.05])
                glTranslatef(0,0,-0.05)
            else:
                selected.add_coordinates([0,0,0.05])
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if selected == camera:
                camera.add_coordinates([0.05,0,0])
                glTranslatef(0.05,0,0)
            else:
                selected.add_coordinates([-0.05,0,0])
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if selected == camera:
                camera.add_coordinates([-0.05,0,0])
                glTranslatef(-0.05,0,0)
            else:
                selected.add_coordinates([0.05,0,0])
        if pygame.key.get_pressed()[pygame.K_i]:
            if selected == camera:
                camera.add_coordinates([0,0.05,0])
                glTranslatef(0,0.05,0)
            else:
                selected.add_coordinates([0,-0.05,0])
        if pygame.key.get_pressed()[pygame.K_u]:
            if selected == camera:
                camera.add_coordinates([0,-0.05,0])
                glTranslatef(0,-0.05,0)
            else:
                selected.add_coordinates([0,0.05,0])
        if pygame.key.get_pressed()[pygame.K_z]:
            if selected == camera:
                glRotatef(-1,1,0,0)
            else:
                selected.add_rotation([1,0,0])
        if pygame.key.get_pressed()[pygame.K_s]:
            if selected == camera:
                glRotatef(1,1,0,0)
            else:
                selected.add_rotation([-1,0,0])
        if pygame.key.get_pressed()[pygame.K_q]:
            if selected == camera:
                glRotatef(-1,0,1,0)
            else:
                selected.add_rotation([0,1,0])
        if pygame.key.get_pressed()[pygame.K_d]:
            if selected == camera:
                glRotatef(1,0,1,0)
            else:
                selected.add_rotation([0,-1,0])
        if pygame.key.get_pressed()[pygame.K_a]:
            if selected == camera:
                glRotatef(1,0,0,1)
            else:
                selected.add_rotation([0,0,-1])
        if pygame.key.get_pressed()[pygame.K_e]:
            if selected == camera:
                glRotatef(-1,0,0,1)
            else:
                selected.add_rotation([0,0,1])


#_______________________________________________________________________________________________________________________

all_objects=[]

camera = CAMERA()


my_object_file = OBJ_FILE('models/theiere.obj')
my_object_file.parse(forceParse=True)# Cache system not faster yet


my_object=FACES(vertices=my_object_file.vertices,quads=my_object_file.quads,triangles=my_object_file.triangles,normals=my_object_file.normals,coordinates=[0,0,0])

all_objects.append(my_object)


my_object_file2 = OBJ_FILE('models/backpack.obj')
my_object_file2.parse(forceParse=True)

my_object2=FACES(vertices=my_object_file2.vertices,quads=my_object_file2.quads,triangles=my_object_file2.triangles,normals=my_object_file2.normals,coordinates=[0,0,0])

all_objects.append(my_object2)


rotating_angle_X=LINES_LOOP(vertices=[(cos(radians(i)),0.0,sin(radians(i))) for i in range(0,360,1)],color=[1,0,0])
rotating_angle_Y=LINES_LOOP(vertices=[(sin(radians(i)),cos(radians(i)),0.0) for i in range(0,360,1)],color=[0,1,0])
rotating_angle_Z=LINES_LOOP(vertices=[(0.0,cos(radians(i)),sin(radians(i))) for i in range(0,360,1)],color=[0,0,1])

#objects_to_be_drew.append(rotating_angle_X)
#objects_to_be_drew.append(rotating_angle_Y)
#objects_to_be_drew.append(rotating_angle_Z)


main()
