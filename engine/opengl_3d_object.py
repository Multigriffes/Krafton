"""Objets OpenGL 3D : géométrie compilée en display lists et caméra à quaternions."""

import logging
from OpenGL.GL import *
from random import randint

logger = logging.getLogger(__name__)

from engine.mathlib import crossProductNormalized, QUATERNION, radians, normalize
from math import cos, sin

# no_mat = [0.0, 0.0, 0.0, 1.0]
# mat_ambient = [0.0, 0.0, 0.3, 1.0]
# mat_diffuse = [1.0, 0.0, 0.0, 1.0]
# no_shininess = [0.0]


class OBJECT_BASE:
    """Classe de base pour tous les objets 3D renderables.

    Gère la position, la rotation, la couleur et l'identifiant de display list OpenGL.
    Les sous-classes implémentent `compile()` pour construire la display list.
    """

    def __init__(
        self,
        vertices: list = None,
        normals: list = None,
        triangles: list = None,
        quads: list = None,
        coordinates: list = None,
        rotation: list = None,
        color: list = None,
        to_be_drew: bool = False,
    ) -> None:
        self.vertices = vertices if vertices is not None else []
        self.normals = normals if normals is not None else []
        self.triangles = triangles if triangles is not None else []
        self.quads = quads if quads is not None else []
        self.gl_list_id = None
        self.coordinates = coordinates if coordinates is not None else [0, 0, 0]
        self.rotation = rotation if rotation is not None else [0, 0, 0]
        self.color = color if color is not None else [1, 1, 1]
        self.to_be_drew = to_be_drew

    def draw(self, coordinates: list = None, rotation: list = None) -> None:
        """Appelle la display list OpenGL avec translation et rotation.

        Si coordinates/rotation sont None, utilise les valeurs de l'objet.
        """
        if self.gl_list_id is not None:
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            (
                glTranslatef(
                    self.coordinates[0], self.coordinates[1], self.coordinates[2]
                )
                if coordinates is None
                else glTranslatef(coordinates[0], coordinates[1], coordinates[2])
            )
            (
                glRotatef(self.rotation[0], 1, 0, 0)
                if rotation is None
                else glRotatef(rotation[0], 1, 0, 0)
            )
            (
                glRotatef(self.rotation[1], 0, 1, 0)
                if rotation is None
                else glRotatef(rotation[1], 0, 1, 0)
            )
            (
                glRotatef(self.rotation[2], 0, 0, 1)
                if rotation is None
                else glRotatef(rotation[2], 0, 0, 1)
            )
            glCallList(self.gl_list_id)
            glPopMatrix()
        else:
            logger.warning(
                "draw() appelé sur un objet non compilé (%s).", self.__class__.__name__
            )

    def addCoordinates(self, coordinates: list = None) -> None:
        """Déplace l'objet en ajoutant [dx, dy, dz] à sa position courante."""
        if coordinates is not None:
            self.coordinates[0] += coordinates[0]
            self.coordinates[1] += coordinates[1]
            self.coordinates[2] += coordinates[2]

    def addRotation(self, rotation: list = None) -> None:
        """Applique une rotation incrémentale [rx, ry, rz] en degrés sur les axes X, Y, Z."""
        if rotation is not None:
            self.rotation[0] += rotation[0]
            self.rotation[1] += rotation[1]
            self.rotation[2] += rotation[2]


class VERTICES(OBJECT_BASE):
    def compile(self) -> None:
        """Compile les sommets en une display list GL_POINTS."""
        if glIsList(self.gl_list_id) == GL_FALSE:
            logger.debug("Compilation VERTICES (%d points).", len(self.vertices))
            self.gl_list_id = glGenLists(1, GL_COMPILE)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_POINTS)
            for vertex in self.vertices:
                glVertex3fv(vertex)
            glEnd()
            glEndList()
            logger.debug("VERTICES compilé (list id=%d).", self.gl_list_id)
        else:
            logger.warning("VERTICES déjà compilé, ignoré.")


class FACES(OBJECT_BASE):
    def compile(self) -> None:
        """Compile quads et triangles en une display list avec couleur aléatoire par face."""
        if self.gl_list_id is None:
            logger.debug(
                "Compilation FACES (%d quads, %d triangles).",
                len(self.quads[0]),
                len(self.triangles[0]),
            )
            self.gl_list_id = glGenLists(1)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_QUADS)
            for i in range(len(self.quads[0])):

                # glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
                # glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
                # glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, no_mat)
                # glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, no_shininess)
                # glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, no_mat)

                glColor3fv(
                    (
                        randint(0, 255) / 255,
                        randint(0, 255) / 255,
                        randint(0, 255) / 255,
                    )
                )
                for j in range(len(self.quads[0][i])):
                    glVertex3fv(self.vertices[self.quads[0][i][j] - 1])
                    # glNormal3fv(self.normals[self.quads[2][i][j]-1])
            glEnd()
            glBegin(GL_TRIANGLES)
            for i in range(len(self.triangles[0])):

                # glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
                # glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
                # glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, no_mat)
                # glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, no_shininess)
                # glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, no_mat)

                glColor3fv(
                    (
                        randint(0, 255) / 255,
                        randint(0, 255) / 255,
                        randint(0, 255) / 255,
                    )
                )
                for j in range(len(self.triangles[0][i])):
                    glVertex3fv(self.vertices[self.triangles[0][i][j] - 1])
                    # glNormal3fv(self.normals[self.triangles[2][i][j]-1])
            glEnd()
            glEndList()
            logger.debug("FACES compilé (list id=%d).", self.gl_list_id)
        else:
            logger.warning("FACES déjà compilé, ignoré.")


class LINES_LOOP(OBJECT_BASE):
    def compile(self) -> None:
        """Compile les sommets en une display list GL_LINE_LOOP (contour fermé)."""
        if self.gl_list_id is None:
            logger.debug("Compilation LINES_LOOP (%d sommets).", len(self.vertices))
            self.gl_list_id = glGenLists(1)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_LINE_LOOP)
            glColor3fv(self.color)
            for vertex in self.vertices:
                glVertex3fv(vertex)
            glEnd()
            glEndList()
            logger.debug("LINES_LOOP compilé (list id=%d).", self.gl_list_id)
        else:
            logger.warning("LINES_LOOP déjà compilé, ignoré.")


class LINES(OBJECT_BASE):
    def compile(self) -> None:
        """Compile les sommets en une display list GL_LINES (segments)."""
        if self.gl_list_id is None:
            logger.debug("Compilation LINES (%d sommets).", len(self.vertices))
            self.gl_list_id = glGenLists(1)
            glNewList(self.gl_list_id, GL_COMPILE)
            glBegin(GL_LINES)
            glColor3fv(self.color)
            for vertex in self.vertices:
                glVertex3fv(vertex)
            glEnd()
            glEndList()
            logger.debug("LINES compilé (list id=%d).", self.gl_list_id)
        else:
            logger.warning("LINES déjà compilé, ignoré.")


class CAMERA:
    """Caméra libre 6 degrés de liberté avec orientation par quaternions.

    Les trois axes (front, up, right) sont maintenus orthonormaux via Gram-Schmidt.
    """

    def __init__(self, coordinates: list = None, speed: float = None) -> None:
        self.coordinates = coordinates if coordinates is not None else [0, 0, 0]
        self.speed = speed if speed is not None else 0.05
        self.front = QUATERNION(w=0, x=0, y=0, z=-1)
        self.up = QUATERNION(w=0, x=0, y=1, z=0)
        self.right = QUATERNION(w=0, x=1, y=0, z=0)
        self.yaw = 0.0  # Pas indicatife d'une quelconque rotation
        self.pitch = 0.0  # Pas indicatife d'une quelconque rotation
        self.roll = 0.0  # Pas indicatife d'une quelconque rotation

    def updateFront(
        self,
    ) -> None:  # On utilise le process de Gramm-Schimdt. Pour les autres aussi
        """Recalcule le vecteur front comme cross product normalisé de up × right."""
        self.front = crossProductNormalized(self.up, self.right)

    def updateRight(self) -> None:
        """Recalcule le vecteur right comme cross product normalisé de front × up."""
        self.right = crossProductNormalized(self.front, self.up)

    def updateUp(self) -> None:
        """Recalcule le vecteur up comme cross product normalisé de right × front."""
        self.up = crossProductNormalized(self.right, self.front)

    def addYaw(self, angle: float) -> None:
        """Tourne autour de l'axe up (rotation gauche/droite), angle en degrés."""
        self.yaw += angle
        # invertedUp = not self.up
        halfAngle = radians(angle / 2)
        quaternionForRotation = QUATERNION(
            w=cos(halfAngle),
            x=sin(halfAngle) * self.up.x,
            y=sin(halfAngle) * self.up.y,
            z=sin(halfAngle) * self.up.z,
        )
        invertedQuaternionForRotation = quaternionForRotation.inverse()

        self.front = normalize(
            quaternionForRotation * self.front * invertedQuaternionForRotation
        )
        self.updateRight()  # Mise à jour du dernier vecteur

    def addPitch(self, angle: float) -> None:
        """Tourne autour de l'axe right (rotation haut/bas), angle en degrés."""
        self.pitch += angle
        halfAngle = radians(angle / 2)
        quaternionForRotation = QUATERNION(
            w=cos(halfAngle),
            x=sin(halfAngle) * self.right.x,
            y=sin(halfAngle) * self.right.y,
            z=sin(halfAngle) * self.right.z,
        )
        invertedQuaternionForRotation = quaternionForRotation.inverse()

        self.up = normalize(
            quaternionForRotation * self.up * invertedQuaternionForRotation
        )
        self.updateFront()  # Mise à jour du dernier vecteur

    def addRoll(self, angle: float) -> None:
        """Tourne autour de l'axe front (inclinaison latérale), angle en degrés."""
        self.roll += angle
        halfAngle = radians(angle / 2)
        quaternionForRotation = QUATERNION(
            w=cos(halfAngle),
            x=sin(halfAngle) * self.front.x,
            y=sin(halfAngle) * self.front.y,
            z=sin(halfAngle) * self.front.z,
        )
        invertedQuaternionForRotation = quaternionForRotation.inverse()

        self.right = normalize(
            quaternionForRotation * self.right * invertedQuaternionForRotation
        )
        self.updateUp()  # Mise à jour du dernier vecteur

    def addCoordinates(self, coordinates: list = None) -> None:
        """Déplace la caméra en ajoutant [dx, dy, dz] à sa position courante."""
        if coordinates is not None:
            self.coordinates[0] += coordinates[0]
            self.coordinates[1] += coordinates[1]
            self.coordinates[2] += coordinates[2]

    def _move(
        self,
        direction: QUATERNION,
        sign: float,
        include_y: bool = True,
        speed: float = None,
    ) -> None:
        """Déplace la caméra le long d'un axe donné.

        Args:
            direction: vecteur de direction (front, up ou right)
            sign: +1.0 = avant/haut/droite, -1.0 = arrière/bas/gauche
            include_y: si False, ignore la composante verticale (déplacement 2D)
            speed: vitesse override ; utilise self.speed si None
        """
        s = speed if speed is not None else self.speed
        self.coordinates[0] += sign * s * direction.x
        if include_y:
            self.coordinates[1] += sign * s * direction.y
        self.coordinates[2] += sign * s * direction.z

    def forward3D(self, speed: float = None) -> None:
        self._move(self.front, 1.0, True, speed)

    def backward3D(self, speed: float = None) -> None:
        self._move(self.front, -1.0, True, speed)

    def forward2D(self, speed: float = None) -> None:
        self._move(self.front, 1.0, False, speed)

    def backward2D(self, speed: float = None) -> None:
        self._move(self.front, -1.0, False, speed)

    def up3D(self, speed: float = None) -> None:
        self._move(self.up, 1.0, True, speed)

    def down3D(self, speed: float = None) -> None:
        self._move(self.up, -1.0, True, speed)

    def up2D(self, speed: float = None) -> None:
        self._move(self.up, 1.0, False, speed)

    def down2D(self, speed: float = None) -> None:
        self._move(self.up, -1.0, False, speed)

    def right3D(self, speed: float = None) -> None:
        self._move(self.right, 1.0, True, speed)

    def left3D(self, speed: float = None) -> None:
        self._move(self.right, -1.0, True, speed)

    def right2D(self, speed: float = None) -> None:
        self._move(self.right, 1.0, False, speed)

    def left2D(self, speed: float = None) -> None:
        self._move(self.right, -1.0, False, speed)

    def reset(self) -> None:
        """Réinitialise la position et l'orientation aux valeurs par défaut (origine, face vers -Z)."""
        self.coordinates = [0, 0, 0]
        self.front = QUATERNION(w=0, x=0, y=0, z=-1)
        self.up = QUATERNION(w=0, x=0, y=1, z=0)
        self.right = QUATERNION(w=0, x=1, y=0, z=0)


class AXES(LINES):
    pass


class ROTATION_AXES(LINES_LOOP):
    pass
