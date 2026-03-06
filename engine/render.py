from multiprocessing.shared_memory import ShareableList

from engine.dot_obj_parser import *
from engine.opengl_3d_object import *
from OpenGL.GLU import *
from OpenGL.GL import *
import pygame
from engine import project



class RENDERER:
    def __init__(self):
        self.sharedMainList = ShareableList(name='MainList')
        self.sharedList= {}
        self.all_objects = []
        self.all_debug_objects = []
        self.cameraSharedList = ShareableList(name='CameraList')
        self.camera = {
            'coordinates': [self.cameraSharedList[0], self.cameraSharedList[1], self.cameraSharedList[2]],
            'front_vec': [self.cameraSharedList[3], self.cameraSharedList[4], self.cameraSharedList[5]],
            'up_vec': [self.cameraSharedList[6], self.cameraSharedList[7], self.cameraSharedList[8]],
            'right_vec': [self.cameraSharedList[9], self.cameraSharedList[10], self.cameraSharedList[11]]
        }

        pygame.init()
        pygame.display.set_mode(project.display, pygame.DOUBLEBUF|pygame.OPENGL)
        glViewport(0,0, project.display[0], project.display[1])
        glMatrixMode(GL_PROJECTION)
        gluPerspective(project.fov, project.display[0]/project.display[1], project.near_plane, project.far_plane)


        #glFrontFace(GL_CW)
        #glCullFace(GL_BACK)
        #glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0,100/255,0,1)

        #glEnable(GL_LIGHTING)
        #glEnable(GL_LIGHT0)

        self.clock = pygame.time.Clock()
        self.run = True

        self.parseAndCreateObjects()
        self.createDebugAxes()
        self.registerSharedList(name = 'sharedKey', size = 133)
        self.main()

    def parseAndCreateObjects(self):
        for object_to_be_created in project.objects:
            object_file = OBJ_FILE(object_to_be_created['path'])
            try:
                object_file.parse(force_parse=True)# Cache system not faster yet
            except FileNotFoundError:
                print("Not Found")
            else:
                match object_to_be_created['type']:
                    case 'Faces':
                        my_object=FACES(to_be_drew=True,vertices=object_file.vertices,quads=object_file.quads,triangles=object_file.triangles,normals=object_file.normals,coordinates=object_to_be_created['coordinates'])
                        self.all_objects.append(my_object)
                    case 'Vertices':
                        my_object=VERTICES(to_be_drew=True,vertices=object_file.vertices,normals=object_file.normals,coordinates=object_to_be_created['coordinates'])
                        self.all_objects.append(my_object)
            finally:
                del object_file # Release some memory

    def sendInput(self):
        keyPressed = pygame.key.get_pressed()
        for i in range(len(keyPressed)):
            self.sharedList['sharedKey'][i] = keyPressed[i]

    def registerSharedList(self, name: str, size: int):
        try:
            headIndex = self.sharedMainList.index(None)
        except ValueError:
            return False
        else:
            self.sharedMainList[headIndex] = name
            self.sharedList[name](ShareableList(sequence=[None for i in range(size)], name=name))

    def constructSharedList(self):
        for sharedElementName in self.sharedMainList:
            if sharedElementName is not None:
                self.sharedList[sharedElementName] = ShareableList(name=sharedElementName)

    def closeAllSharedObjects(self):
        for sharedElementName in self.sharedMainList:
            self.sharedList[sharedElementName].shm.close()


    def createDebugAxes(self):
        if project.debug_axes: # Création des axes en créant des lignes à deux points
            axe_x=AXES(to_be_drew=True,vertices=[[0, 0, 0], [1, 0, 0]], color=[1, 0, 0])
            axe_y=AXES(to_be_drew=True,vertices=[[0, 0, 0], [0, 1, 0]], color=[0, 1, 0])
            axe_z=AXES(to_be_drew=True,vertices=[[0, 0, 0], [0, 0, 1]], color=[0, 0, 1])
            self.all_debug_objects.append(axe_x)
            self.all_debug_objects.append(axe_y)
            self.all_debug_objects.append(axe_z)

        if project.debug_rotation_axes: # Création des axes de rotation à partir des sin et cos
            rotation_axe_x=ROTATION_AXES(to_be_drew=True,vertices=[(0.0, cos(radians(i)), sin(radians(i))) for i in range(0, 360, 1)], color=[1, 0, 0])
            rotation_axe_y=ROTATION_AXES(to_be_drew=True,vertices=[(cos(radians(i)), 0.0, sin(radians(i))) for i in range(0, 360, 1)], color=[0, 1, 0])
            rotation_axe_z=ROTATION_AXES(to_be_drew=True,vertices=[(cos(radians(i)), sin(radians(i)), 0.0) for i in range(0, 360, 1)], color=[0, 0, 1])
            self.all_debug_objects.append(rotation_axe_x)
            self.all_debug_objects.append(rotation_axe_y)
            self.all_debug_objects.append(rotation_axe_z)

    def main(self):
        while self.run:
            timeSinceLastFrame = self.clock.tick(project.fpsLimit)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            gluLookAt(
                self.camera['coordinates'][0], self.camera['coordinates'][1], self.camera['coordinates'][2],
                self.camera['coordinates'][0] + self.camera['front_vec'][0], self.camera['coordinates'][1] + self.camera['front_vec'][1], self.camera['coordinates'][2] + self.camera['front_vec'][2],
                self.camera['up_vec'][0], self.camera['up_vec'][1], self.camera['up_vec'][2]
            )

            #______________Draw all objects___________
            for object in self.all_objects:
                if object.to_be_drew:
                    object.draw()
            #__________________________________________


            #______________Draw all debug___________
            for object in self.all_debug_objects:
                if object.to_be_drew:
                    object.draw()
            #__________________________________________

            pygame.display.flip()


render = RENDERER()