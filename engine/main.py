from OpenGL.GLU import *
import pygame
import engine.project as project
from engine.dot_obj_parser import *
from engine.object import *
from game.game import *
from engine.shareLib import ShareableList


class MAIN:
    def __init__(self):
        self.all_objects = {}
        self.all_debug_objects = []

        pygame.init()
        pygame.display.set_mode(project.display, pygame.DOUBLEBUF|pygame.OPENGL)
        glViewport(0,0, project.display[0], project.display[1])
        glMatrixMode(GL_PROJECTION)
        gluPerspective(project.fov, project.display[0]/project.display[1], project.near_plane, project.far_plane)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0,100/255,0,1)

        left_controller = ShareableList(name='left_controller', sequence=range(3))
        right_controller = ShareableList(name='right_controller', sequence=range(3))

        left_controller = Controller(color=(255, 0, 0), pos=[0, 0, 10])
        right_controller = Controller(color=(0, 0, 255), pos=[0, 0, 10])

        block_1 = Block(color=(0, 255, 0), pos=[0,-3,-20])
        block_2 = Block(color=(0, 255, 0), pos=[0,-3,-20])
        block_3 = Block(color=(0, 255, 0), pos=[0,-3,-20])
        block_4 = Block(color=(0, 255, 0), pos=[0,-3,-20])

        self.object_lst = [left_controller, right_controller, block_1, block_2, block_3, block_4]

        self.camera = CAMERA()
        self.clock = pygame.time.Clock()
        self.run = True

        self.lst_to_be_drew = [True for i in range(6)]

        self.parseAndCreateObjects()
        self.createDebugAxes()
        self.main()

    def parseAndCreateObjects(self):
        for object_to_be_created in project.objects:
            object_file = OBJ_FILE(project.objects[object_to_be_created]['path'])
            try:
                object_file.parseFile()# Cache system not faster yet
            except FileNotFoundError:
                print(object_file.filePath, "Not Found")
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
                self.camera.coordinates[0], self.camera.coordinates[1], self.camera.coordinates[2],
                self.camera.front_vec.x + self.camera.coordinates[0], self.camera.front_vec.y + self.camera.coordinates[1], self.camera.front_vec.z + self.camera.coordinates[2],
                self.camera.up_vec.x, self.camera.up_vec.y, self.camera.up_vec.z
            )

            # __________game__________
            self.lst_to_be_drew, self.object_lst = game(self.lst_to_be_drew, self.object_lst)
            # __________game__________

            #______Change to_be_drew attribute________
            for i in range(len(self.lst_to_be_drew)):
                self.all_objects[project.liste_nom_objet[i//3]].to_be_drew = self.lst_to_be_drew[i]
            #_________________________________________

            #_______Change object coordinates---------
            for i in range(len(self.object_lst)):
                self.all_objects[project.liste_nom_objet[i]].coordinates = self.object_lst[i].pos
            #_________________________________________

            #______________Draw all objects___________
            for object in self.all_objects:
                if self.all_objects[object].to_be_drew:
                    self.all_objects[object].draw()
            #_________________________________________

            #______________Draw all debug_____________
            for object in self.all_debug_objects:
                if object.to_be_drew:
                    object.draw()
            #_________________________________________

            pygame.display.flip()
            #print(self.clock.get_fps())
            #self.somethingChanged[0]=False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()

            self.processKey()

    def processKey(self):
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_ESCAPE]:
            self.run = False
            pygame.quit()

        if keyPressed[pygame.K_UP]:
            self.camera.moveForward(locked_axe=project.lockedAxe)

        if keyPressed[pygame.K_DOWN]:
            self.camera.moveBackward(locked_axe=project.lockedAxe)

        if keyPressed[pygame.K_LEFT]:
            self.camera.moveLeft(locked_axe=project.lockedAxe)

        if keyPressed[pygame.K_RIGHT]:
            self.camera.moveRight(locked_axe=project.lockedAxe)

        if keyPressed[pygame.K_c]:
            self.camera.moveDown(locked_axe=project.lockedAxe)

        if keyPressed[pygame.K_SPACE]:
            self.camera.moveUp(locked_axe=project.lockedAxe)

        if keyPressed[pygame.K_z]:
            self.camera.addPitch(1)

        if keyPressed[pygame.K_s]:
            self.camera.addPitch(-1)

        if keyPressed[pygame.K_q]:
            self.camera.addYaw(1)

        if keyPressed[pygame.K_d]:
            self.camera.addYaw(-1)

        if keyPressed[pygame.K_a]:
            self.camera.addRoll(-1)

        if keyPressed[pygame.K_e]:
            self.camera.addRoll(1)

        if keyPressed[pygame.K_RETURN]:
            self.camera.reset()

main = MAIN()