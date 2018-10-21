import Utils.constants as C

class CollisionDetection:

    def __init__(self, grid_height, grid_width):
        self.s = set()
        self.max_x = grid_width
        self.max_y = grid_height

    def add(self, pos_x, pos_y):
        if pos_x < 0 or pos_x > self.max_x or pos_y < 0 or pos_y > self.max_y:
            raise ValueError('Robot out of bounds at x=%d, y=%d' % (pos_x, pos_y))
        if (C.cell_to_index(pos_x,pos_y,self.max_x)) in self.s:
            raise ValueError('Collision at x=%d, y=%d' % (pos_x, pos_y))
        else:
            self.s.add(C.cell_to_index(pos_x,pos_y,self.max_x))



class CollisionDetectionEdge(CollisionDetection):

    def __init__(self, grid_height, grid_width):
        CollisionDetection.__init__(self,grid_height, grid_width)

    def add(self, pos_x, pos_y, heading):
        if pos_x < 0 or pos_x > self.max_x or pos_y < 0 or pos_y > self.max_y:
            raise ValueError('Robot out of bounds at x=%d, y=%d' % (pos_x, pos_y))
        if (C.edge_to_index(pos_x,pos_y,heading,self.max_x,self.max_y)) in self.s:
            raise ValueError('Collision at x=%d, y=%d, heading=%s' % (pos_x, pos_y, heading))
        else:
            self.s.add(C.edge_to_index(pos_x,pos_y,heading,self.max_x,self.max_y))
