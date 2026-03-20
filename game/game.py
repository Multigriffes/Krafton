from engine.dot_obj_parser import OBJ_FILE
from engine.shareLib import ShareableList
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

    def auto_move(self):
        pass


class Controller(Objet):
    def __init__(self, color:tuple, pos:list):
        super().__init__(color, pos)


def game():
    pos_lst = ShareableList(name='pos_lst')
    left_controller = Controller(color=(255,0,0), pos=eval(pos_lst[0]))
    right_controller = Controller(color=(0, 0, 255), pos=eval(pos_lst[1]))