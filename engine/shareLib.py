from multiprocessing.shared_memory import ShareableList
def registerSharedList(self, name: str, size: int):
    name = name[:7]
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
        self.sharedLists[sharedElementName].shm.close()