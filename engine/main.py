from objparser import *
from engine import *
import pygame
from OpenGL.GLU import *
from math import cos,sin,radians

#_______________________________________________________Main Loop_______________________________________________________

def main():
    pygame.init()
    display = [1920//2,1080//2]
    pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)

    #______________Objects to be compiled_______
    #    for object in objects_to_be_compiled:
    #        object.compile()
    #___________________________________________

    gluPerspective(45,display[0]/display[1], 0.01 , 500)
    glViewport(0,0,display[0],display[1])
    glTranslatef(0,0,-20)

    #glFrontFace(GL_CW)
    #glCullFace(GL_FRONT)
    #glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    clock=pygame.time.Clock()
    lastFps = 0
    run = True

    while run:
        clock.tick(144)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    quit()
        if pygame.key.get_pressed()[pygame.K_UP]:
            glTranslatef(0,0,0.05)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            glTranslatef(0,0,-0.05)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            glTranslatef(0.05,0,0)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            glTranslatef(-0.05,0,0)
        if pygame.key.get_pressed()[pygame.K_i]:
            glTranslatef(0,0.05,0)
        if pygame.key.get_pressed()[pygame.K_u]:
            glTranslatef(0,-0.05,0)
        if pygame.key.get_pressed()[pygame.K_z]:
            glRotatef(1,-1,0,0)
        if pygame.key.get_pressed()[pygame.K_s]:
            glRotatef(1,1,0,0)
        if pygame.key.get_pressed()[pygame.K_q]:
            glRotatef(1,0,-1,0)
        if pygame.key.get_pressed()[pygame.K_d]:
            glRotatef(1,0,1,0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #______________Objects to be drew___________
        for object in objects_to_be_drew:
            object.draw()
        #____________________________________________
        pygame.display.flip()
        print(clock.get_fps())

#_______________________________________________________________________________________________________________________

objects_to_be_compiled=[]
objects_to_be_drew=[]


my_object_file = OBJ_FILE('models/16834_hand_v1_NEW.obj')
my_object_file.parse()
my_object_file.releaseFile()

my_object=FACES(vertices=my_object_file.vertices,quads=my_object_file.quads,triangles=my_object_file.triangles)

objects_to_be_drew.append(my_object)

rotating_angle_X=LINES_LOOP(vertices=[(cos(radians(i)),0.0,sin(radians(i))) for i in range(0,360,1)])
rotating_angle_Y=LINES_LOOP(vertices=[(sin(radians(i)),cos(radians(i)),0.0) for i in range(0,360,1)])
rotating_angle_Z=LINES_LOOP(vertices=[(0.0,cos(radians(i)),sin(radians(i))) for i in range(0,360,1)])

#objects_to_be_drew.append(rotating_angle_X)
#objects_to_be_drew.append(rotating_angle_Y)
#objects_to_be_drew.append(rotating_angle_Z)


main()
