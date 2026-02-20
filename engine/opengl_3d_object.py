from OpenGL.GL import *
from random import randint

from engine.mathlib import crossProductNormalized, QUATERNION, radians, normalize
from math import cos, sin

#no_mat = [0.0, 0.0, 0.0, 1.0]
#mat_ambient = [0.0, 0.0, 0.3, 1.0]
#mat_diffuse = [1.0, 0.0, 0.0, 1.0]
#no_shininess = [0.0]



class OBJECT_BASE:
    def __init__(self,vertices: list = None,normals: list = None,triangles: list = None,quads: list = None,coordinates: list = None,rotation: list = None,color: list = None,to_be_drew: bool = False) -> None:
        self.vertices=vertices if vertices is not None else []
        self.normals=normals if normals is not None else []
        self.triangles=triangles if triangles is not None else []
        self.quads=quads if quads is not None else []
        self.gl_list_id=None
        self.coordinates=coordinates if coordinates is not None else [0,0,0]
        self.rotation=rotation if rotation is not None else [0,0,0]
        self.color=color if color is not None else [1,1,1]
        self.to_be_drew=to_be_drew

    def draw(self,coordinates: list = None,rotation: list = None) -> None:
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

    def addCoordinates(self,coordinates: list = None) -> None:
        if coordinates is not None:
            self.coordinates[0] += coordinates[0]
            self.coordinates[1] += coordinates[1]
            self.coordinates[2] += coordinates[2]

    def addRotation(self,rotation: list = None) -> None:
        if rotation is not None:
            self.rotation[0] += rotation[0]
            self.rotation[1] += rotation[1]
            self.rotation[2] += rotation[2]

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
    def compile(self) -> None:
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

class LINES(OBJECT_BASE):
    def compile(self) -> None:
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

class CAMERA:
    def __init__(self, coordinates: list = None, speed: float = None) -> None:
        self.coordinates = coordinates if coordinates is not None else [0,0,0]
        self.speed = speed if speed is not None else 0.05
        self.front = QUATERNION(w=0, x=0, y=0, z=-1)
        self.up = QUATERNION(w=0, x=0, y=1, z=0)
        self.right = QUATERNION(w=0, x=1, y=0, z=0)
        self.yaw = 0.0 # Pas indicatife d'une quelconque rotation
        self.pitch = 0.0 # Pas indicatife d'une quelconque rotation
        self.roll = 0.0 # Pas indicatife d'une quelconque rotation

    def updateFront(self) -> None: # On utilise le process de Gramm-Schimdt. Pour les autres aussi
        self.front = crossProductNormalized(self.up, self.right)

    def updateRight(self) -> None:
        self.right = crossProductNormalized(self.front, self.up)

    def updateUp(self) -> None:
        self.up = crossProductNormalized(self.right, self.front)

    def addYaw(self, angle: float) -> None:
        self.yaw += angle
        #invertedUp = not self.up
        halfAngle=radians(angle/2)
        quaternionForRotation = QUATERNION(w = cos(halfAngle), x = sin(halfAngle)*self.up.x, y = sin(halfAngle)*self.up.y, z = sin(halfAngle)*self.up.z)
        invertedQuaternionForRotation = quaternionForRotation.inverse()

        self.front = normalize(quaternionForRotation * self.front * invertedQuaternionForRotation)
        self.updateRight() # Mise à jour du dernier vecteur

    def addPitch(self, angle: float) -> None:
        self.pitch += angle
        halfAngle=radians(angle/2)
        quaternionForRotation = QUATERNION(w = cos(halfAngle), x = sin(halfAngle)*self.right.x, y = sin(halfAngle)*self.right.y, z = sin(halfAngle)*self.right.z)
        invertedQuaternionForRotation = quaternionForRotation.inverse()

        self.up = normalize(quaternionForRotation * self.up * invertedQuaternionForRotation)
        self.updateFront() # Mise à jour du dernier vecteur

    def addRoll(self, angle: float) -> None:
        self.roll += angle
        halfAngle=radians(angle/2)
        quaternionForRotation = QUATERNION(w = cos(halfAngle), x = sin(halfAngle)*self.front.x, y = sin(halfAngle)*self.front.y, z = sin(halfAngle)*self.front.z)
        invertedQuaternionForRotation = quaternionForRotation.inverse()

        self.right = normalize(quaternionForRotation * self.right  * invertedQuaternionForRotation)
        self.updateUp() # Mise à jour du dernier vecteur

    def addCoordinates(self,coordinates: list = None) -> None:
        if coordinates is not None:
            self.coordinates[0] += coordinates[0]
            self.coordinates[1] += coordinates[1]
            self.coordinates[2] += coordinates[2]

    def _move(self, direction: QUATERNION, sign: float, include_y: bool = True, speed: float = None) -> None:
        s = speed if speed is not None else self.speed
        self.coordinates[0] += sign * s * direction.x
        if include_y:
            self.coordinates[1] += sign * s * direction.y
        self.coordinates[2] += sign * s * direction.z

    def forward3D(self, speed: float = None) -> None:  self._move(self.front,  1.0, True,  speed)
    def backward3D(self, speed: float = None) -> None: self._move(self.front, -1.0, True,  speed)
    def forward2D(self, speed: float = None) -> None:  self._move(self.front,  1.0, False, speed)
    def backward2D(self, speed: float = None) -> None: self._move(self.front, -1.0, False, speed)

    def up3D(self, speed: float = None) -> None:   self._move(self.up,  1.0, True,  speed)
    def down3D(self, speed: float = None) -> None: self._move(self.up, -1.0, True,  speed)
    def up2D(self, speed: float = None) -> None:   self._move(self.up,  1.0, False, speed)
    def down2D(self, speed: float = None) -> None: self._move(self.up, -1.0, False, speed)

    def right3D(self, speed: float = None) -> None: self._move(self.right,  1.0, True,  speed)
    def left3D(self, speed: float = None) -> None:  self._move(self.right, -1.0, True,  speed)
    def right2D(self, speed: float = None) -> None: self._move(self.right,  1.0, False, speed)
    def left2D(self, speed: float = None) -> None:  self._move(self.right, -1.0, False, speed)

    def reset(self) -> None:
        self.coordinates = [0,0,0]
        self.front = QUATERNION(w=0, x=0, y=0, z=-1)
        self.up = QUATERNION(w=0, x=0, y=1, z=0)
        self.right = QUATERNION(w=0, x=1, y=0, z=0)


class AXES(LINES):
    pass

class ROTATION_AXES(LINES_LOOP):
    pass