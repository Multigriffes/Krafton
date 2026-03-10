from time import sleep
from shareLib import *
from pygame import Clock

from engine.physic_object import *


class PHYSIC:
    def __init__(self):
        self.sharedMainList = ShareableList(name='MainList', sequence=[None for i in range(256)])
        self.sharedLists = {}
        self.objects = []
        self.cameraShared = ShareableList(sequence=[0,0,0,
                                                    0,0,-1,
                                                    0,1,0,
                                                    1,0,0],
                                          name='CameraList')
        self.camera = CAMERA()
        while True:
            sleep(1)





physic = PHYSIC()