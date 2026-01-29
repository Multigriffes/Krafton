import random

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos,sin,radians
from objparserV2 import OBJfile


MyVerticesCube = (
    (1,-1,-1),
    (1,1,-1),
    (-1,1,-1),
    (-1,-1,-1),
    (1,-1,1),
    (1,1,1),
    (-1,-1,1),
    (-1,1,1)
)

MyEdgesCube = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
)

MyVerticesTriangle = (
    (0,0,1),
    (-1,0,0),
    (1,-1,0),
    (1,1,0)
)

MyFacesTriangle = (
    (0,1,2),
    (0,1,3),
    (0,2,3),
    (1,2,3)
)

MyEdgesBase = (
    (0,1),
    (0,2),
    (0,3)
)

MyVerticesXAxe = [(cos(radians(i)),0.0,sin(radians(i))) for i in range(0,360,1)]
MyVerticesYAxe = [(sin(radians(i)),cos(radians(i)),0.0) for i in range(0,360,1)]
MyVerticesZAxe = [(0.0,cos(radians(i)),sin(radians(i))) for i in range(0,360,1)]

MyVerticesBase = (
    (0,0,0),
    (1,0,0),
    (0,1,0),
    (0,0,1)
)

MyColors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0)

)

MyAxisColor = (
    (1,0,0),
    (0,1,0),
    (0,0,1)
)

CoordZero3d = (0,0,0)

class Volume:
    def __init__(self,type):
        self.type=type
        self.vertices=[]
        self.quads=[]
        self.triangles=[]
        self.edges=[]
        self.normals=[]

    def draw(self,coordinates=(0,0,0),color=(0,0,0)):
        match self.type:
            case 'Lines':
                glBegin(GL_LINES)
                for edge in self.edges:
                    for vertex in edge:
                        glVertex3fv((self.vertices[vertex][0]+coordinates[0],self.vertices[vertex][1]+coordinates[1],self.vertices[vertex][2]+coordinates[2]))
                glEnd()

            case 'Triangles':
                glBegin(GL_TRIANGLES)
                NumeroCouleur = 0
                for face in self.faces:
                    for vertex in face:
                        NumeroCouleur = (NumeroCouleur % 3) + 1
                        glColor3fv(MyColors[NumeroCouleur])
                        glVertex3fv((self.vertices[vertex][0]+coordinates[0],self.vertices[vertex][1]+coordinates[1],self.vertices[vertex][2]+coordinates[2]))
                glEnd()
            case 'Base':
                glBegin(GL_LINES)
                NumeroCouleur = 0
                for edge in self.edges:
                    glColor3fv(MyAxisColor[NumeroCouleur])
                    for vertex in edge:
                        glVertex3fv((self.vertices[vertex][0]+coordinates[0],self.vertices[vertex][1]+coordinates[1],self.vertices[vertex][2]+coordinates[2]))
                    NumeroCouleur += 1
                glEnd()
            case 'Axe':
                glBegin(GL_LINE_LOOP)
                glColor3fv(color)
                for vertex in self.vertices:
                    glVertex3fv((vertex[0]+coordinates[0],vertex[1]+coordinates[1],vertex[2]+coordinates[2]))
                glEnd()

            case 'Points':
                glBegin(GL_POINTS)
                for vertex in self.vertices:
                    glVertex3fv((vertex[0]+coordinates[0],vertex[1]+coordinates[1],vertex[2]+coordinates[2]))
                glEnd()

            case 'Quads':
                if glIsList(1)==GL_FALSE:
                    glNewList(1,GL_COMPILE)
                    glBegin(GL_QUADS)
                    for i in range(len(self.faces[0])):
                        glColor3fv((random.randint(0,255)/255,random.randint(0,255)/255,random.randint(0,255)/255))
                        for j in range(len(self.faces[0][i])):
                            glVertex3fv(self.vertices[self.faces[0][i][j]-1])
                            #glNormal3fv(self.normals[self.faces[2][i][j]-1])
                    glEnd()
                    glEndList()
                else:
                    glCallList(1)
            case 'Polygons':
                if glIsList(1) == GL_FALSE:
                    glNewList(1, GL_COMPILE)
                    glBegin(GL_POLYGON)
                    for i in range(len(self.faces[0])):
                        #glColor3fv((random.randint(0, 255) / 255, random.randint(0, 255) / 255, random.randint(0, 255) / 255))
                        for j in range(len(self.faces[0][i])):
                            glVertex3fv(self.vertices[self.faces[0][i][j]-1])
                            #glNormal3fv(self.normals[self.faces[2][i][j]-1])
                    glEnd()
                    glEndList()
                else:
                    glCallList(1)
            case 'Faces':
                if glIsList(1) == GL_FALSE:
                    glNewList(1, GL_COMPILE)
                    glBegin(GL_QUADS)
                    for i in range(len(self.quads[0])):
                        glColor3fv((random.randint(0, 255) / 255, random.randint(0, 255) / 255, random.randint(0, 255) / 255))
                        for j in range(len(self.quads[0][i])):
                            glVertex3fv(self.vertices[self.quads[0][i][j] - 1])
                            #glNormal3fv(self.normals[self.faces[2][i][j]-1])
                    glEnd()
                    glBegin(GL_TRIANGLES)
                    for i in range(len(self.triangles[0])):
                        glColor3fv((random.randint(0, 255) / 255, random.randint(0, 255) / 255, random.randint(0, 255) / 255))
                        for j in range(len(self.triangles[0][i])):
                            glVertex3fv(self.vertices[self.triangles[0][i][j] - 1])
                            #glNormal3fv(self.normals[self.faces[2][i][j]-1])
                    glEnd()
                    glEndList()
                else:
                    glCallList(1)


    def SetVertices(self,vertices):
        self.vertices=vertices

    def SetEdges(self,edges):
        self.edges=edges
    
    def SetTriangles(self,triangles):
        self.triangles=triangles

    def SetQuads(self,quads):
        self.quads=quads

    def SetNormals(self,normals):
        self.normals=normals



def main():
    pygame.init()
    display = [1920//2,1080//2]
    pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)


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
        clock.tick(-1)
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


            #if event.type == pygame.MOUSEBUTTONDOWN:
            #    if pygame.mouse.get_pressed()[0]:
            #        pygame.mouse.get_rel()
            #if event.type == pygame.MOUSEBUTTONUP:
            #    if not pygame.mouse.get_pressed()[0]:
            #        MyCamera.AddAngles(pygame.mouse.get_rel())

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Objet.draw()

        #for k in range(0,12,2):
        #    CubeLines.draw((k,0,0))
        #TriangleFaces.draw(CoordZero3d)
        #BaseLines.draw()
        #AxeX.draw(color=(1,0,0))
        #AxeY.draw(color=(0,1,0))
        #AxeZ.draw(color=(0,0,1))


        pygame.display.flip()
        #if clock.get_fps()<=40:
        #    print(clock.get_fps())
        #if clock.get_fps()!=lastFps:
        #    print(clock.get_fps())
        #    lastFps = clock.get_fps()
        print(clock.get_fps())


FichierObjet=OBJfile('models/bugatti.obj')
FichierObjet.parse()
FichierObjet.releaseFile()
Objet=Volume('Faces')
Objet.SetVertices(FichierObjet.vertices)
Objet.SetTriangles(FichierObjet.triangles)
Objet.SetQuads(FichierObjet.quads)


main()