from shareLib import *
from pygame import Clock
import project
from physic_object import *
from game.game import *


class PHYSIC:
    def __init__(self):
        self.sharedMainList = ShareableList(name='MainList', sequence=[None for i in range(256)])
        self.all_objects = {}
        self.clock = Clock()
        self.sharedKey = ShareableList(name='sharedKey', sequence=[False for i in range(14)])

        self.camera = CAMERA()
        self.cameraShared = ShareableList(sequence=[self.camera.coordinates[0],self.camera.coordinates[1],self.camera.coordinates[2],
                                                    self.camera.front_vec.x,self.camera.front_vec.y,self.camera.front_vec.z,
                                                    self.camera.up_vec.x,self.camera.up_vec.y,self.camera.up_vec.z,
                                                    self.camera.right_vec.x,self.camera.right_vec.y,self.camera.right_vec.z],
                                          name='CameraList')

        self.something_changed = ShareableList(name='somethingChanged', sequence=[True])

        self.run = True
        self.parseAndCreateObjects()
        self.main()

    def main(self):
        timer = 0
        while self.run:
            timeSinceLastFrame = self.clock.tick(project.fpsLimit)
            self.processKey()
            self.sendCamera()
            #self.sendObjects()

            #__________game__________
            lst_objects_to_be_drew = game()
            #__________game__________

    def parseAndCreateObjects(self):
        for object_to_be_created in project.objects:
            self.all_objects[object_to_be_created] = OBJECT_BASE(coordinates=project.objects[object_to_be_created]['coordinates'])

    def processAnimation(self):
        pass

    def sendCamera(self):
        #print(self.camera)
        self.cameraShared[0] = self.camera.coordinates[0]
        self.cameraShared[1] = self.camera.coordinates[1]
        self.cameraShared[2] = self.camera.coordinates[2]
        self.cameraShared[3] = self.camera.front_vec.x
        self.cameraShared[4] = self.camera.front_vec.y
        self.cameraShared[5] = self.camera.front_vec.z
        self.cameraShared[6] = self.camera.up_vec.x
        self.cameraShared[7] = self.camera.up_vec.y
        self.cameraShared[8] = self.camera.up_vec.z
        self.cameraShared[9] = self.camera.right_vec.x
        self.cameraShared[10] = self.camera.right_vec.y
        self.cameraShared[11] = self.camera.right_vec.z

    #def sendObjects(self):
    #    for object in self.all_objects:


    def processKey(self):
        if self.sharedKey[K_ESCAPE]:
            self.run = False
            
        if self.sharedKey[K_UP]:
            self.camera.moveForward(locked_axe=project.lockedAxe)

        if self.sharedKey[K_DOWN]:
            self.camera.moveBackward(locked_axe=project.lockedAxe)

        if self.sharedKey[K_LEFT]:
            self.camera.moveLeft(locked_axe=project.lockedAxe)

        if self.sharedKey[K_RIGHT]:
            self.camera.moveRight(locked_axe=project.lockedAxe)

        if self.sharedKey[K_c]:
            self.camera.moveDown(locked_axe=project.lockedAxe)

        if self.sharedKey[K_SPACE]:
            self.camera.moveUp(locked_axe=project.lockedAxe)

        if self.sharedKey[K_z]:
            self.camera.addPitch(1)

        if self.sharedKey[K_s]:
            self.camera.addPitch(-1)

        if self.sharedKey[K_q]:
            self.camera.addYaw(1)

        if self.sharedKey[K_d]:
            self.camera.addYaw(-1)

        if self.sharedKey[K_a]:
            self.camera.addRoll(-1)

        if self.sharedKey[K_e]:
            self.camera.addRoll(1)

        if self.sharedKey[K_RETURN]:
            self.camera.reset()


physic = PHYSIC()