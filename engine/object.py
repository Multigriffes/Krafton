from engine.mathlib import crossProductNormalized, QUATERNION, radians, normalize4, normalize3
from math import cos, sin
from OpenGL.GL import *
from random import randint

class OBJECT_BASE:
    def __init__(self,vertices: list = None,normals: list = None,triangles: list = None,quads: list = None,coordinates: list = None,rotation: list = None,color: list = None,to_be_drew: bool = False) -> None:
        self.coordinates=coordinates if coordinates is not None else [0,0,0]
        self.rotation=rotation if rotation is not None else [0,0,0]
        self.vertices=vertices if vertices is not None else []
        self.normals=normals if normals is not None else []
        self.triangles=triangles if triangles is not None else []
        self.quads=quads if quads is not None else []
        self.gl_list_id = None
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

    def moveAlong(self, unit: float = 1, vector: list = None) -> None:
        if vector is not None:
            vector = normalize3(vector)
            self.coordinates[0] += vector[0] * unit
            self.coordinates[1] += vector[1] * unit
            self.coordinates[2] += vector[2] * unit


class CAMERA:
    def __init__(self, coordinates: list = None, speed: float = None) -> None:
        self.coordinates = coordinates if coordinates is not None else [0,0,0]
        self.speed = speed if speed is not None else 0.05
        self.front_vec = QUATERNION(w=0, x=0, y=0, z=-1)
        self.up_vec = QUATERNION(w=0, x=0, y=1, z=0)
        self.right_vec = QUATERNION(w=0, x=1, y=0, z=0)

    def updateFront(self) -> None: # On utilise le process de Gramm-Schimdt. Pour les autres aussi
        self.front_vec = crossProductNormalized(self.up_vec, self.right_vec)

    def updateRight(self) -> None:
        self.right_vec = crossProductNormalized(self.front_vec, self.up_vec)

    def updateUp(self) -> None:
        self.up_vec = crossProductNormalized(self.right_vec, self.front_vec)

    def addYaw(self, angle: float) -> None:
        radiansHalfAngle=radians(angle/2)
        usefulSin=sin(radiansHalfAngle)
        usefulCos=cos(radiansHalfAngle)
        quaternionForRotation = QUATERNION(w = usefulCos, x = usefulSin*self.up_vec.x, y = usefulSin * self.up_vec.y, z = usefulSin * self.up_vec.z)
        invertedQuaternionForRotation = quaternionForRotation.inverse()

        self.front_vec = normalize4(quaternionForRotation * self.front_vec * invertedQuaternionForRotation)
        self.updateRight() # Mise à jour du dernier vecteur

    def addPitch(self, angle: float) -> None:
        radiansHalfAngle=radians(angle/2)
        usefulSin=sin(radiansHalfAngle)
        usefulCos=cos(radiansHalfAngle)
        quaternionForRotation = QUATERNION(w = usefulCos, x = usefulSin*self.right_vec.x, y = usefulSin * self.right_vec.y, z = usefulSin * self.right_vec.z)
        invertedQuaternionForRotation = quaternionForRotation.inverse()

        self.up_vec = normalize4(quaternionForRotation * self.up_vec * invertedQuaternionForRotation)
        self.updateFront() # Mise à jour du dernier vecteur

    def addRoll(self, angle: float) -> None:
        radiansHalfAngle=radians(angle/2)
        usefulSin=sin(radiansHalfAngle)
        usefulCos=cos(radiansHalfAngle)
        quaternionForRotation = QUATERNION(w = usefulCos, x = usefulSin*self.front_vec.x, y = usefulSin * self.front_vec.y, z = usefulSin * self.front_vec.z)
        invertedQuaternionForRotation = quaternionForRotation.inverse()

        self.right_vec = normalize4(quaternionForRotation * self.right_vec * invertedQuaternionForRotation)
        self.updateUp() # Mise à jour du dernier vecteur

    def moveForward(self, speed: float = None, locked_axe : str = None) -> None:
        if speed is None:
            speed = self.speed
        if locked_axe is None:
            # Il faudrait pas qu'en regardant en haut on se mette à moins avancer tout droit si on se déplace que sur le plan.
            # Il suffit pas de juste ne pas faire de déplacement en Y. Je sais pas encore comment faire ah si ah non
            self.coordinates[0] += speed*self.front_vec.x
            self.coordinates[1] += speed*self.front_vec.y
            self.coordinates[2] += speed*self.front_vec.z
        else:
            newUpVector=self.front_vec.getVectorWithout(locked_axe)
            self.coordinates[0] += speed * newUpVector.x
            self.coordinates[1] += speed * newUpVector.y
            self.coordinates[2] += speed * newUpVector.z

    def moveBackward(self, speed: float = None, locked_axe : str = None) -> None:
        if speed is None:
            speed = self.speed
        if locked_axe is None:
            # Il faudrait pas qu'en regardant en haut on se mette à moins avancer tout droit si on se déplace que sur le plan.
            # Il suffit pas de juste ne pas faire de déplacement en Y. Je sais pas encore comment faire ah si ah non
            self.coordinates[0] -= speed*self.front_vec.x
            self.coordinates[1] -= speed*self.front_vec.y
            self.coordinates[2] -= speed*self.front_vec.z
        else:
            newUpVector=self.front_vec.getVectorWithout(locked_axe)
            self.coordinates[0] -= speed * newUpVector.x
            self.coordinates[1] -= speed * newUpVector.y
            self.coordinates[2] -= speed * newUpVector.z

    def moveUp(self, speed: float = None, locked_axe : str = None) -> None:
        if speed is None:
            speed = self.speed
        if locked_axe is None:
            # Il faudrait pas qu'en regardant en haut on se mette à moins avancer tout droit si on se déplace que sur le plan.
            # Il suffit pas de juste ne pas faire de déplacement en Y. Je sais pas encore comment faire ah si ah non
            self.coordinates[0] += speed*self.up_vec.x
            self.coordinates[1] += speed*self.up_vec.y
            self.coordinates[2] += speed*self.up_vec.z
        else:
            newUpVector=self.up_vec.getVectorWithout(locked_axe)
            self.coordinates[0] += speed * newUpVector.x
            self.coordinates[1] += speed * newUpVector.y
            self.coordinates[2] += speed * newUpVector.z

    def moveDown(self, speed: float = None, locked_axe : str = None) -> None:
        if speed is None:
            speed = self.speed
        if locked_axe is None:
            # Il faudrait pas qu'en regardant en haut on se mette à moins avancer tout droit si on se déplace que sur le plan.
            # Il suffit pas de juste ne pas faire de déplacement en Y. Je sais pas encore comment faire ah si ah non
            self.coordinates[0] -= speed*self.up_vec.x
            self.coordinates[1] -= speed*self.up_vec.y
            self.coordinates[2] -= speed*self.up_vec.z
        else:
            newUpVector=self.up_vec.getVectorWithout(locked_axe)
            self.coordinates[0] -= speed * newUpVector.x
            self.coordinates[1] -= speed * newUpVector.y
            self.coordinates[2] -= speed * newUpVector.z

    def moveLeft(self, speed: float = None, locked_axe : str = None) -> None:
        if speed is None:
            speed = self.speed
        if locked_axe is None:
            # Il faudrait pas qu'en regardant en haut on se mette à moins avancer tout droit si on se déplace que sur le plan.
            # Il suffit pas de juste ne pas faire de déplacement en Y. Je sais pas encore comment faire ah si ah non
            self.coordinates[0] -= speed*self.right_vec.x
            self.coordinates[1] -= speed*self.right_vec.y
            self.coordinates[2] -= speed*self.right_vec.z
        else:
            newUpVector=self.right_vec.getVectorWithout(locked_axe)
            self.coordinates[0] -= speed * newUpVector.x
            self.coordinates[1] -= speed * newUpVector.y
            self.coordinates[2] -= speed * newUpVector.z

    def moveRight(self, speed: float = None, locked_axe : str = None) -> None:
        if speed is None:
            speed = self.speed
        if locked_axe is None:
            # Il faudrait pas qu'en regardant en haut on se mette à moins avancer tout droit si on se déplace que sur le plan.
            # Il suffit pas de juste ne pas faire de déplacement en Y. Je sais pas encore comment faire ah si ah non
            self.coordinates[0] += speed*self.right_vec.x
            self.coordinates[1] += speed*self.right_vec.y
            self.coordinates[2] += speed*self.right_vec.z
        else:
            newUpVector=self.right_vec.getVectorWithout(locked_axe)
            self.coordinates[0] += speed * newUpVector.x
            self.coordinates[1] += speed * newUpVector.y
            self.coordinates[2] += speed * newUpVector.z

    def reset(self) -> None:
        self.coordinates = [0,0,0]
        self.front_vec.w, self.front_vec.x, self.front_vec.y, self.front_vec.z = 0, 0, 0, -1
        self.up_vec.w, self.up_vec.x, self.up_vec.y, self.up_vec.z = 0, 0, 1, 0
        self.right_vec.w, self.right_vec.x, self.right_vec.y, self.right_vec.z = 0, 1, 0, 0

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
