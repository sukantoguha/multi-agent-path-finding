import pygame
import Utils.constants as cons


class Station:


    def __init__(self, x,y,index):
        self.position_x = x
        self.position_y = y
        self.index = index
        self.process = False

    def display(self, screen, offset_x, offset_y):
        color = cons.PAINT['S']
        if self.process:
            color = cons.PAINT['PROCESS']
            self.process = False
        screen.fill(color, [cons.cell_to_position(self.position_x,offset_x),
                                 cons.cell_to_position(self.position_y,offset_y), cons.CELL_SIZE, cons.CELL_SIZE])
        cons.display_agent_label(self.position_x, self.position_y, offset_x, offset_y, self.index, screen)