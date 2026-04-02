from engine.shareLib import ShareableList
from game.game_parameters import *

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

    def auto_move(self):
        self.pos = (self.pos[0], self.pos[1], self.pos[2] -1) # a modifier apres test


class Controller(Objet):
    def __init__(self, color:tuple, pos:list):
        super().__init__(color, pos)
        self.size = 100

    def detect_collision(self, object: Objet) -> bool:
        x, y, z = self.pos
        size = self.size
        x_object, y_object, z_object = object.get_pos()

        x_in = x - size / 2 <= x_object <= x + size / 2
        y_in = y - size / 2 <= y_object <= y + size / 2
        z_in = z - size / 2 <= z_object <= z + size / 2

        if x_in and y_in and z_in:
            return True

        return False

def pos_object_to_str(pos:list):
    return str(pos)

def pos_object_to_lst(pos:str):
    return eval(pos)

def game(lst_to_be_drew:list, object_list:list):

    '''
    for i, object in enumerate(object_list[2:]):
        if object_list[LEFT_CONTROLLER].detect_collision(object):
            lst_to_be_drew[i] = False

    for i, object in enumerate(object_list[2:]):
        if object_list[RIGHT_CONTROLLER].detect_collision(object):
            lst_to_be_drew[i] = False
    '''

    for block in object_list[2:]:
        block.auto_move()

    return lst_to_be_drew, object_list