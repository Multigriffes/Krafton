from OpenGL.GL import *
from random import randint


class VERTICES:
    def __init__(self,vertices=[],normals=[]):
        self.vertices=vertices
        self.normals=normals
        self.gl_list_id=None

    def set_vertices(self,vertices):
        self.vertices = vertices

    def set_normals(self,normals):
        self.normals = normals

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

    def draw(self):
        if self.gl_list_id is not None:
            glCallList(self.gl_list_id)
        else:
            print('Not compiled')

class FACES:
    def __init__(self,vertices=[],normals=[],triangles=[],quads=[]):
        self.vertices=vertices
        self.normals=normals
        self.triangles=triangles
        self.quads=quads
        self.gl_list_id=None

    def set_vertices(self,vertices):
        self.vertices = vertices

    def set_normals(self,normals):
        self.normals = normals

    def set_triangles(self,triangles):
        self.triangles = triangles

    def set_quads(self,quads):
        self.quads = quads

    def compile(self):
        if self.gl_list_id is None:
            self.gl_list_id = glGenLists(1)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_QUADS)
            for i in range(len(self.quads[0])):
                glColor3fv((randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255))
                for j in range(len(self.quads[0][i])):
                    glVertex3fv(self.vertices[self.quads[0][i][j] - 1])
                    #glNormal3fv(self.normals[self.faces[2][i][j]-1])
            glEnd()
            glBegin(GL_TRIANGLES)
            for i in range(len(self.triangles[0])):
                glColor3fv((randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255))
                for j in range(len(self.triangles[0][i])):
                    glVertex3fv(self.vertices[self.triangles[0][i][j] - 1])
                    #glNormal3fv(self.normals[self.faces[2][i][j]-1])
            glEnd()
            glEndList()
        else:
            print('Already compiled')

    def draw(self):
        if self.gl_list_id is not None:
            glCallList(self.gl_list_id)
        else:
            print("Not compiled so let's compile")
            self.compile()

class LINES_LOOP:
    def __init__(self,vertices=[],normals=[]):
        self.vertices=vertices
        self.normals=normals
        self.gl_list_id=None

    def set_vertices(self,vertices):
        self.vertices = vertices

    def set_normals(self,normals):
        self.normals = normals

    def compile(self):
        if self.gl_list_id is None:
            self.gl_list_id = glGenLists(1)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_LINE_LOOP)
            for vertex in self.vertices:
                glVertex3fv(vertex)
            glEnd()
            glEndList()
        else:
            print('Already compiled')

    def draw(self):
        if self.gl_list_id is not None:
            glCallList(self.gl_list_id)
        else:
            print("Not compiled so let's compile")
            self.compile()