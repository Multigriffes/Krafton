from OpenGL.GL import *
from random import randint

#no_mat = [0.0, 0.0, 0.0, 1.0]
#mat_ambient = [0.0, 0.0, 0.3, 1.0]
#mat_diffuse = [1.0, 0.0, 0.0, 1.0]
#no_shininess = [0.0]



class OBJECT_BASE:
    def __init__(self,vertices=None,normals=None,triangles=None,quads=None,coordinates=None,rotation=None,color=None,to_be_drew=False):
        self.vertices=vertices if vertices is not None else []
        self.normals=normals if normals is not None else []
        self.triangles=triangles if triangles is not None else []
        self.quads=quads if quads is not None else []
        self.gl_list_id=None
        self.coordinates=coordinates if coordinates is not None else [0,0,0]
        self.rotation=rotation if rotation is not None else [0,0,0]
        self.color=color if color is not None else [1,1,1]
        self.to_be_drew=to_be_drew

    def draw(self,coordinates=None,rotation=None):
        if self.gl_list_id is not None:
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glTranslatef(self.coordinates[0],self.coordinates[1],self.coordinates[2]) if coordinates is None else glTranslatef(coordinates[0],coordinates[1],coordinates[2])
            glRotatef(self.rotation[0],1,0,0) if rotation is None else glRotatef(rotation[0],1,0,0)
            glRotatef(self.rotation[1],0,1,0) if rotation is None else glRotatef(rotation[1],0,1,0)
            glRotatef(self.rotation[2],0,0,1) if rotation is None else glRotatef(rotation[2],0,0,1)
            glCallList(self.gl_list_id)
            glPopMatrix()
        else:
            print('Not compiled')

    def addCoordinates(self,coordinates=None):
        if coordinates is not None:
            self.coordinates[0] += coordinates[0]
            self.coordinates[1] += coordinates[1]
            self.coordinates[2] += coordinates[2]

    def addRotation(self,rotation=None):
        if rotation is not None:
            self.rotation[0] += rotation[0]
            self.rotation[1] += rotation[1]
            self.rotation[2] += rotation[2]

class VERTICES(OBJECT_BASE):
    def compile(self):
        if glIsList(self.gl_list_id) == GL_FALSE:
            self.gl_list_id = glGenLists(1, GL_COMPILE)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_POINTS)
            for vertex in self.vertices:
                glVertex3fv(vertex)
            glEnd()
            glEndList()
        else:
            print('Already compiled')

class FACES(OBJECT_BASE):
    def compile(self):
        if self.gl_list_id is None:
            self.gl_list_id = glGenLists(1)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_QUADS)
            for i in range(len(self.quads[0])):

                #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
                #glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
                #glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, no_mat)
                #glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, no_shininess)
                #glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, no_mat)

                glColor3fv((randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255))
                for j in range(len(self.quads[0][i])):
                    glVertex3fv(self.vertices[self.quads[0][i][j] - 1])
                    #glNormal3fv(self.normals[self.quads[2][i][j]-1])
            glEnd()
            glBegin(GL_TRIANGLES)
            for i in range(len(self.triangles[0])):

                #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
                #glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
                #glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, no_mat)
                #glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, no_shininess)
                #glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, no_mat)

                glColor3fv((randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255))
                for j in range(len(self.triangles[0][i])):
                    glVertex3fv(self.vertices[self.triangles[0][i][j] - 1])
                    #glNormal3fv(self.normals[self.triangles[2][i][j]-1])
            glEnd()
            glEndList()
        else:
            print('Already compiled')

class LINES_LOOP(OBJECT_BASE):
    def compile(self):
        if self.gl_list_id is None:
            self.gl_list_id = glGenLists(1)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_LINE_LOOP)
            glColor3fv(self.color)
            for vertex in self.vertices:
                glVertex3fv(vertex)
            glEnd()
            glEndList()
        else:
            print('Already compiled')

class CAMERA(OBJECT_BASE):
    pass

class AXES(OBJECT_BASE):
    def compile(self):
        if self.gl_list_id is None:
            self.gl_list_id = glGenLists(1)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_LINES)
            glColor3fv(self.color)
            for vertex in self.vertices:
                glVertex3fv(vertex)
            glEnd()
            glEndList()
        else:
            print('Already compiled')

class ROTATION_AXES(OBJECT_BASE):
    def compile(self):
        if self.gl_list_id is None:
            self.gl_list_id = glGenLists(1)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_LINE_LOOP)
            glColor3fv(self.color)
            for vertex in self.vertices:
                glVertex3fv(vertex)
            glEnd()
            glEndList()
        else:
            print('Already compiled')