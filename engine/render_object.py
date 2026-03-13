from OpenGL.GL import *
from random import randint


class OBJECT_BASE:
    def __init__(self,vertices: list = None,normals: list = None,triangles: list = None,quads: list = None,coordinates: list = None,rotation: list = None,color: list = None,to_be_drew: bool = False) -> None:
        self.vertices=vertices if vertices is not None else []
        self.normals=normals if normals is not None else []
        self.triangles=triangles if triangles is not None else []
        self.quads=quads if quads is not None else []
        self.gl_list_id=None
        self.coordinates=coordinates if coordinates is not None else [0,0,0]
        self.rotation=rotation if rotation is not None else [0,0,0]
        self.color=color
        self.to_be_drew=to_be_drew

    def draw(self,coordinates: list = None,rotation: list = None) -> None:
        if self.gl_list_id is None:
            self.compile()
        else:
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glTranslatef(self.coordinates[0],self.coordinates[1],self.coordinates[2]) if coordinates is None else glTranslatef(coordinates[0],coordinates[1],coordinates[2])
            glRotatef(self.rotation[0],1,0,0) if rotation is None else glRotatef(rotation[0],1,0,0)
            glRotatef(self.rotation[1],0,1,0) if rotation is None else glRotatef(rotation[1],0,1,0)
            glRotatef(self.rotation[2],0,0,1) if rotation is None else glRotatef(rotation[2],0,0,1)
            glCallList(self.gl_list_id)
            glPopMatrix()

class VERTICES(OBJECT_BASE):
    def compile(self) -> None:
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
    def compile(self) -> None:
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

                glColor3fv((randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255)) if self.color is None else glColor3fv(self.color)
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

                glColor3fv((randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255)) if self.color is None else glColor3fv(self.color)
                for j in range(len(self.triangles[0][i])):
                    glVertex3fv(self.vertices[self.triangles[0][i][j] - 1])
                    #glNormal3fv(self.normals[self.triangles[2][i][j]-1])
            glEnd()
            glEndList()
        else:
            print('Already compiled')

class LINES_LOOP(OBJECT_BASE):
    def compile(self) -> None:
        if self.gl_list_id is None:
            self.gl_list_id = glGenLists(1)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_LINE_LOOP)
            glColor3fv((randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255)) if self.color is None else glColor3fv(self.color)
            for vertex in self.vertices:
                glVertex3fv(vertex)
            glEnd()
            glEndList()
        else:
            print('Already compiled')

class LINES(OBJECT_BASE):
    def compile(self) -> None:
        if self.gl_list_id is None:
            self.gl_list_id = glGenLists(1)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_LINES)
            glColor3fv((randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255)) if self.color is None else glColor3fv(self.color)
            for vertex in self.vertices:
                glVertex3fv(vertex)
            glEnd()
            glEndList()
        else:
            print('Already compiled')

class AXES(LINES):
    pass

class ROTATION_AXES(LINES_LOOP):
    pass

class CAMERA:
    def __init__(self, coordinates: list = None, front_vec: list = None, up_vec: list = None, right_vec: list = None) -> None:
        self.coordinates = coordinates if coordinates is not None else [0,0,0]
        self.front_vec = front_vec if front_vec is not None else [0,0,0]
        self.up_vec = up_vec if up_vec is not None else [0,0,0]
        self.right_vec = right_vec if right_vec is not None else [0,0,0]
