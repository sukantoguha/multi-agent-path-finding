import pygame
import Utils.constants as cons

class Pod:

    def __init__(self, x,y,index):
        self.position_x = x
        self.position_y = y
        self.index = index
        self.assigned = None
        self.original_x = x
        self.original_y = y

    def display(self, screen, offset_x, offset_y):
        screen.fill(cons.PAINT['p'], [cons.cell_to_position(self.position_x,offset_x) + 1,
                                 cons.cell_to_position(self.position_y,offset_y) + 1, cons.CELL_SIZE -2, cons.CELL_SIZE - 2])

        cons.display_agent_label(self.position_x, self.position_y, offset_x, offset_y, self.index, screen)
