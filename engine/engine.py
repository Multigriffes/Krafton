from OpenGL.GL import *
from random import randint

#no_mat = [0.0, 0.0, 0.0, 1.0]
#mat_ambient = [0.0, 0.0, 0.3, 1.0]
#mat_diffuse = [1.0, 0.0, 0.0, 1.0]
#no_shininess = [0.0]

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

    def draw(self):
        if self.gl_list_id is not None:
            glCallList(self.gl_list_id)
        else:
            print("Not compiled so let's compile")
            self.compile()

class LINES_LOOP:
    def __init__(self,vertices=[],normals=[],color=[1,1,1]):
        self.vertices=vertices
        self.normals=normals
        self.color=color
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
            glColor3fv(self.color)
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