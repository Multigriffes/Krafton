class Block:
    def __init__(self, color:tuple, pos:lst, obj=None):
        self.color = color
        self.pos = pos
        self.size = 100
        self.obj = obj

    def get_color(self):
        return self.color
    
    def get_pos(self):
        return self.pos
    
    def get_size(self):
        return self.size
    
    def get_obj(self):
        return self.obj

    def detect_collision(self, object_pos_lst:list)->bool:
        x, y,  z = self.pos
        size = self.size
        
        for pos in object_pos_lst:
            x_in = x-size/2 <= pos[0] <= x+size/2
            y_in = y-size/2 <= pos[1] <= y+size/2
            z_in = z-size/2 <= pos[2] <= z+size/2
            
            if x_in and y_in and z_in:
                return True
            
        return False
    
    def move(self, translation:tuple):
        self.pos[0] += translation(0)
        self.pos[1] += translation(1)
        self.pos[2] += translation(2)