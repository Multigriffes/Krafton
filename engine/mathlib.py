from math import pi

def radians(degrees):
    return degrees*pi/180

def degrees(radians):
    return radians*180/pi

class VEC3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.list=[x,y,z]
    #def multiply(self, other):
    #    assert type(other) == VEC3
    #    return VEC3(x=)
    # Enft Hamilton à pas trouver donc c pas possible on doit forcement passer aux quaternions
    # Mais je viens de voire enft les vecteur 3d c'est juste des quaternions avec un parti real nul pour le w ou la partie scalaire donc .....
    def multiply(self, other):
        assert type(other) == VEC3
        return VEC3(
            x=(self.y*other.z - self.z*other.y),
            y=(self.z*other.x - self.x*other.z),
            z=(self.x*other.y - self.y*other.x)
        )

def dot(a, b):
    assert len(a.list) == len(b.list)
    dot_product = 0.0
    for i in range(len(a.list)):
        dot_product += a[i] * b[i]
    return dot_product

class QUATERNION:
    def __init__(self, w=0, x=0, y=0, z=0):
        self.w = w # partie réel égale cos(angle/2)+sin(angle/2)
        self.x = x # co du vecteur 3d autour duquel je tourne
        self.y = y # co du vecteur 3d autour duquel je tourne
        self.z = z # co du vecteur 3d autour duquel je tourne
        self.list=[w,x,y,z]
    def multiply(self, other):
        assert type(other) == QUATERNION
        return QUATERNION(
            w=(self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z),
            x=(self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y),
            y=(self.w*other.y + self.y*other.w + self.z*other.x - self.x*other.z),
            z=(self.w*other.z + self.z*other.w + self.x*other.y - self.y*other.x)
        )


