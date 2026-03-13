from engine.mathlib import crossProductNormalized, QUATERNION, radians, normalize4, normalize3
from math import cos, sin

class ANIMATION:
    def __init__(self, coordinates: list = None, time: float = None) -> None:
        self.goto = coordinates
        self.time = time if time is not None else 0
        self.timePassed = 0.0
        self.timeLeft = time

    def move(self, timeSinceLastFrame: float, object) -> None:
        vector = [self.goto[0] - object.coordinates[0], self.goto[1] - object.coordinates[1], self.goto[2] - object.coordinates[2]]



        self.timeLeft = self.time - self.timePassed



class OBJECT_BASE:
    def __init__(self,coordinates: list = None,rotation: list = None) -> None:
        self.coordinates=coordinates if coordinates is not None else [0,0,0]
        self.rotation=rotation if rotation is not None else [0,0,0]
        self.animation = {}

    def addAnimation(self, name: str, animation: ANIMATION) -> None:
        self.animation[name] = animation


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

