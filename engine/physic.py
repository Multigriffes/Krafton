from multiprocessing.shared_memory import ShareableList
from time import sleep

from engine.opengl_3d_object import CAMERA


class MAIN:
    def __init__(self):
        self.sharedMainList = ShareableList(name='MainList', sequence=[None for i in range(256)])
        self.sharedLists = {}
        self.objects = []
        self.camera = CAMERA()
        self.cameraShared = ShareableList(sequence=[0,0,0,
                                                    0,0,-1,
                                                    0,1,0,
                                                    1,0,0
                                                    ], name='CameraList')
        while True:
            sleep(1)

    def registerSharedList(self, name: str, size: int):
        try:
            headIndex = self.sharedMainList.index(None)
        except ValueError:
            return False
        else:
            self.sharedMainList[headIndex] = name
            self.sharedLists[name](ShareableList(sequence=[None for i in range(size)], name=name))

    def constructSharedList(self):
        for sharedElement in self.sharedMainList:
            if sharedElement is not None:
                self.sharedLists[sharedElement] = ShareableList(name=sharedElement)

    def closeAllSharedObjects(self):
        for sharedElementName in self.sharedMainList:
            self.sharedList[sharedElementName].shm.close()



physic = MAIN()