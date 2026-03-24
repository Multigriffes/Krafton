from engine.shareLib import ShareableList
from game_parameters import *
from random import randint

class Objet:
    def __init__(self, color:tuple, pos:list):
        self.color = color
        self.pos = pos

    def get_color(self):
        return self.color
    
    def get_pos(self):
        return self.pos


class Block(Objet):
    def __init__(self, color:tuple, pos:list):
        self.size = 100
        super().__init__(color, pos)

    def get_size(self):
        return self.size

    def auto_move(self):
        self.pos = (self.pos[0] + self.size, self.pos[1] + self.size, self.pos[2] + self.size) # a modifier apres test


class Controller(Objet):
    def __init__(self, color:tuple, pos:list):
        super().__init__(color, pos)

    def detect_collision(self, object_pos_lst: list) -> bool:
        x, y, z = self.pos
        size = self.size

        for pos in object_pos_lst:
            x_in = x - size / 2 <= pos[0] <= x + size / 2
            y_in = y - size / 2 <= pos[1] <= y + size / 2
            z_in = z - size / 2 <= pos[2] <= z + size / 2

            if x_in and y_in and z_in:
                return True

        return False

def pos_object_to_str(pos:list):
    return str(pos)

def pos_object_to_lst(pos:str):
    return eval(pos)

def game():
    pos_lst = ShareableList(name='PosList')
    left_controller = Controller(color=(255,0,0), pos=eval(pos_lst[0])) #a modifier quand liste prete
    right_controller = Controller(color=(0, 0, 255), pos=eval(pos_lst[1])) # de même

    for i, object in enumerate(object_pos_lst):
        if left_controller.detect_collision(object):
            pos_lst[i] = None

    if right_controller.detect_collision():
        objects_to_be_drew['right_controller'] = False

    return lst_objects_to_be_drew