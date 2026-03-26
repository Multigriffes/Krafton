from math import cos, radians, sin
from multiprocessing.shared_memory import ShareableList
from shareLib import *
from dot_obj_parser import *
from render_object import *
from OpenGL.GLU import *
from OpenGL.GL import *
import pygame
import project


class RENDERER:
    def __init__(self):
        self.sharedMainList = ShareableList(name='MainList')
        self.all_objects = {}
        self.all_debug_objects = []
        self.cameraSharedList = ShareableList(name='CameraList')
        self.sharedKey = ShareableList(name='sharedKey')
        self.somethingChanged = ShareableList(name='somethingChanged')
        self.sharedToBeDrew = ShareableList(name='ToBeDrew', sequence=[True for i in range(6)])

        pygame.init()
        pygame.display.set_mode(project.display, pygame.DOUBLEBUF|pygame.OPENGL)
        glViewport(0,0, project.display[0], project.display[1])
        glMatrixMode(GL_PROJECTION)
        gluPerspective(project.fov, project.display[0]/project.display[1], project.near_plane, project.far_plane)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0,100/255,0,1)

        self.clock = pygame.time.Clock()
        self.run = True

        self.parseAndCreateObjects()
        self.createDebugAxes()

        self.main()

    def parseAndCreateObjects(self):
        for object_to_be_created in project.objects:
            object_file = OBJ_FILE(project.objects[object_to_be_created]['path'])
            try:
                object_file.parseFile()# Cache system not faster yet
            except FileNotFoundError:
                print("Not Found")
            else:
                match project.objects[object_to_be_created]['type']:
                    case 'Faces':
                        my_object=FACES(to_be_drew=True,vertices=object_file.vertices,quads=object_file.quads,triangles=object_file.triangles,normals=object_file.normals,coordinates=project.objects[object_to_be_created]['coordinates'])
                        self.all_objects[object_to_be_created] = my_object
                    case 'Vertices':
                        my_object=VERTICES(to_be_drew=True,vertices=object_file.vertices,normals=object_file.normals,coordinates=object_to_be_created['coordinates'])
                        self.all_objects[object_to_be_created] = my_object
            finally:
                del object_file # Release some memory


    def sendInput(self):
        #print(self.sharedKey)
        keyPressed = pygame.key.get_pressed()
        self.sharedKey[K_ESCAPE] = keyPressed[pygame.K_ESCAPE]
        self.sharedKey[K_UP] = keyPressed[pygame.K_UP]
        self.sharedKey[K_DOWN] = keyPressed[pygame.K_DOWN]
        self.sharedKey[K_LEFT] = keyPressed[pygame.K_LEFT]
        self.sharedKey[K_RIGHT] = keyPressed[pygame.K_RIGHT]

        self.sharedKey[K_z] = keyPressed[pygame.K_z]
        self.sharedKey[K_s] = keyPressed[pygame.K_s]
        self.sharedKey[K_q] = keyPressed[pygame.K_q]
        self.sharedKey[K_d] = keyPressed[pygame.K_d]
        self.sharedKey[K_e] = keyPressed[pygame.K_e]
        self.sharedKey[K_a] = keyPressed[pygame.K_a]

        self.sharedKey[K_SPACE] = keyPressed[pygame.K_SPACE]
        self.sharedKey[K_c] = keyPressed[pygame.K_c]

        self.sharedKey[K_RETURN] = keyPressed[pygame.K_RETURN]

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
            #if self.somethingChanged[0]:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            gluLookAt(
                self.cameraSharedList[0], self.cameraSharedList[1], self.cameraSharedList[2],
                self.cameraSharedList[0] + self.cameraSharedList[3], self.cameraSharedList[1] + self.cameraSharedList[4], self.cameraSharedList[2] + self.cameraSharedList[5],
                self.cameraSharedList[6], self.cameraSharedList[7], self.cameraSharedList[8]
            )

            #______Change to_be_drew attribute________
            for i in range(len(self.sharedToBeDrew)):
                self.all_objects[project.liste_nom_objet[i]] = self.sharedToBeDrew[i]
            #_________________________________________

            #______________Draw all objects___________
            for object in self.all_objects:
                if self.all_objects[object].to_be_drew:
                    self.all_objects[object].draw()
            #__________________________________________

            #______________Draw all debug___________
            for object in self.all_debug_objects:
                if object.to_be_drew:
                    object.draw()
            #__________________________________________

            pygame.display.flip()
            #print(self.clock.get_fps())
            #self.somethingChanged[0]=False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()

            self.sendInput()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.run = False
                pygame.quit()


render = RENDERER()