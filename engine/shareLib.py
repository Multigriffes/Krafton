from multiprocessing.shared_memory import ShareableList, SharedMemory

def registerSharedList(self, name: str, size: int):
    name = name[:7]
    try:
        headIndex = self.sharedMainList.index(None)
    except ValueError:
        return False
    else:
        self.sharedMainList[headIndex] = name
        self.sharedLists[name] = (ShareableList(sequence=[None for i in range(size)], name=name))

def registerSharedVariable(self, name: str, size: int):
    name = name[:7]
    try:
        headIndex = self.sharedMainList.index(None)
    except ValueError:
        return False
    else:
        self.sharedMainList[headIndex] = name
        self.sharedLists[name] = SharedMemory(name=name, size=size)

def constructSharedList(self):
    for sharedElement in self.sharedMainList:
        if sharedElement is not None:
            self.sharedLists[sharedElement] = ShareableList(name=sharedElement)

def closeAllSharedObjects(self):
    for sharedElementName in self.sharedMainList:
        self.sharedLists[sharedElementName].shm.close()

K_UP = 1
K_DOWN = 2
K_LEFT = 3
K_RIGHT = 4
K_z = 5
K_s = 6
K_q = 7
K_d = 8
K_e = 9
K_a = 10
K_c = 12
K_SPACE = 11
K_ESCAPE = 0
K_RETURN = 13