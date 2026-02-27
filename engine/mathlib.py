from math import pi, sqrt

class QUATERNION:
    def __init__(self, w: float = 0.0, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.w = w # partie réel égale cos(angle/2)+sin(angle/2) pour les rotation et 0 pour un vecteur 3d
        self.init_w = w
        self.x = x # co du vecteur 3d autour duquel je tourne
        self.init_x = x
        self.y = y # co du vecteur 3d autour duquel je tourne
        self.init_y = y
        self.z = z # co du vecteur 3d autour duquel je tourne
        self.init_z = z
        self.list=[w,x,y,z]

    def reset(self):
        self.w, self.x, self.y, self.z = self.init_w, self.init_x, self.init_y, self.init_z

    def __mul__(self, other): # jsp ce que je vais en faire,.... mtn je sais
        # il y a des méthodes qui permettent de faire supporter des operand a un object en l'occurance le *
        # python essaye d'abord la méthode de l'object de gauche spuis ensuite la méthode de droite
        # object1 * object2 --> object1.__mul__(object2) y'a aussi __rmul__ mais j'ai pas trop compris encore
        assert isinstance(other, QUATERNION)
        return QUATERNION(
            w=(self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z),
            x=(self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y),
            y=(self.w*other.y + self.y*other.w + self.z*other.x - self.x*other.z),
            z=(self.w*other.z + self.z*other.w + self.x*other.y - self.y*other.x)
        )
    def __getitem__(self, index: int) -> float: #pour les object[i]
        return self.list[index]

    def inverse(self):
        return QUATERNION(w= self.w / self.getLengthNoSqrt(), x= -self.x / self.getLengthNoSqrt(), y= -self.y / self.getLengthNoSqrt(), z= -self.z / self.getLengthNoSqrt())

    def __invert__(self): # hihihi je m'amuse ducoup
        return QUATERNION(w= self.w / self.getLengthNoSqrt(), x= -self.x / self.getLengthNoSqrt(), y= -self.y / self.getLengthNoSqrt(), z= -self.z / self.getLengthNoSqrt())

    def getLengthNoSqrt(self) -> float:
        return self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalize(self):
        length = sqrt(self.getLengthNoSqrt())
        return QUATERNION(w=0,
                          x = self.x / length,
                          y = self.y / length,
                          z = self.z / length
                          )

    def getVectorWithout(self, axe: str):
        match axe:
            case "x":
                return normalize(QUATERNION(y = self.y, z = self.z))
            case "y":
                return normalize(QUATERNION(x = self.x, z = self.z))
            case "z":
                return normalize(QUATERNION(x = self.x, y = self.y))
            case _:
                return self


# Yvan Monka like ptn j'adore ce type c'est un dieu :
# https://www.youtube.com/watch?v=zjMuIxRvygQ
# https://www.youtube.com/watch?v=d4EgbgTm0Bg


def radians(degrees: float) -> float:
    return degrees*pi/180

def degrees(radians: float) -> float:
    return radians*180/pi

#class VEC3: # ça dégage enft on va juste utiliser des lists
#    def __init__(self, x=0.0, y=0.0, z=0.0):
#        self.x = x
#        self.y = y
#        self.z = z
#        self.list=[x,y,z]
    #def multiply(self, other):
    #    assert type(other) == VEC3
    #    return VEC3(x=)
    # Enft Hamilton à pas trouver donc c pas possible on doit forcement passer aux quaternions
    # Mais je viens de voire enft les vecteur 3d c'est juste des quaternions avec un parti real nul pour le w ou la partie scalaire donc .....

def dotProduct(a: list, b: list) -> float:
    assert len(a) == len(b)
    dot_product = 0.0
    for i in range(len(a)):
        dot_product += a[i] * b[i]
    return dot_product

def crossProduct(a: QUATERNION, b: QUATERNION) -> QUATERNION: # Le cross product de deux vecteur donne un vecteur perpendiculaire aux deux autres, c'est l'équivalent d'une multiplication
    assert isinstance(a, QUATERNION) # faut faire comme ça selon les conventions PEP et pas type(a)==object
    assert isinstance(b, QUATERNION)
    return QUATERNION(w=0,
        x = (a.y*b.z - a.z*b.y),
        y = (a.z*b.x - a.x*b.z),
        z = (a.x*b.y - a.y*b.x)
    )

def normalize(vector: QUATERNION) -> QUATERNION:
    assert isinstance(vector, QUATERNION)
    length = sqrt(vector.getLengthNoSqrt())
    if length != 0.0:
        return QUATERNION(w=0,
            x = vector.x / length,
            y = vector.y / length,
            z = vector.z / length
        )
    else:
        return vector

def crossProductNormalized(a: QUATERNION, b: QUATERNION) -> QUATERNION: # https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process#/media/File:Gram-Schmidt_orthonormalization_process.gif
    assert isinstance(a, QUATERNION)
    assert isinstance(b, QUATERNION)
    return crossProduct(a, b).normalize()

