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
        super().__init__(color, pos)

    def get_size(self):
        return self.size

    def auto_move(self):
        self.pos = (self.pos[0] + self.size, self.pos[1] + self.size, self.pos[2] + self.size) # a modifier apres test


class Controller(Objet):
    def __init__(self, color:tuple, pos:list):
        super().__init__(color, pos)
        self.size = 100

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
    lst_to_be_drew = ShareableList(name='ToBeDrewList')
    left_controller = Controller(color=(255,0,0), pos=[pos_lst[LEFT_CONTROLLER], pos_lst[LEFT_CONTROLLER+1], pos_lst[LEFT_CONTROLLER+2]])
    right_controller = Controller(color=(0, 0, 255), pos=[pos_lst[RIGHT_CONTROLLER], pos_lst[RIGHT_CONTROLLER+1], pos_lst[RIGHT_CONTROLLER+2]])
    block_1 = Block(color=(0,255,0), pos=[pos_lst[BLOCK_1], pos_lst[BLOCK_1+1], pos_lst[BLOCK_1+2]])
    block_2 = Block(color=(0,255,0), pos=[pos_lst[BLOCK_2], pos_lst[BLOCK_2+1], pos_lst[BLOCK_2+2]])
    block_3 = Block(color=(0, 255, 0), pos=[pos_lst[BLOCK_3], pos_lst[BLOCK_3+1], pos_lst[BLOCK_3+2]])
    block_4 = Block(color=(0, 255, 0), pos=[pos_lst[BLOCK_4], pos_lst[BLOCK_4+1], pos_lst[BLOCK_4+2]])

    block_lst = [block_1, block_2, block_3, block_4]

    for i, object in enumerate(block_lst):
        if left_controller.detect_collision(object):
            lst_to_be_drew[i] = False

    for i, object in enumerate(block_lst):
        if right_controller.detect_collision(object):
            lst_to_be_drew[i] = False