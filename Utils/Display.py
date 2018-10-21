import pygame
import Utils.constants as cons
from Utils.Warehouse import Warehouse
from time import sleep


class Display:

    def __init__(self, map):
        self.background_colour = cons.BLACK
        self.time_elapsed = 0
        self.offset_x = 0
        self.offset_y = 0
        self.clicked = False
        self.warehouse = Warehouse(map)
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("Figures/logo512x512.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Multiagen Pathfinding")
        # create a surface on screen that has the size of 240 x 180
        self.screen = pygame.display.set_mode((1180,710))



    def update_screen(self):
        self.screen.fill(self.background_colour)
        self.warehouse.display(self.screen, self.offset_x, self.offset_y)
        #sleep(0.05)
        timer = cons.FONT_TIMER.render("{0:.1f}".format(self.time_elapsed), True, cons.BLACK,cons.WHITE)
        self.screen.blit(timer, (10,10))
        pygame.display.flip()

    def run(self):
        while self.process_event():
            if self.time_elapsed % cons.STEPS_PER_SCREEN == 0:
                #self.warehouse.agents[0][0].manual_control()
                self.warehouse.step()
                self.update_screen()

            #self.perform_step()
            self.time_elapsed += 1
        #print("self.time_elapsed : ", self.time_elapsed)

    def process_event(self):
        if self.clicked:
            dx,dy = pygame.mouse.get_rel()
            self.offset_x += dx
            self.offset_y += dy
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.dict['button'] == 4:
                        if cons.CELL_SIZE < 40:
                            cons.CELL_SIZE += 1
                            cons.FONT_AGENT = pygame.font.Font(None, int(cons.CELL_SIZE * 0.5), bold=True)
                            self.offset_x -= cons.CELL_SIZE/2
                            self.offset_y -= cons.CELL_SIZE/2
                    elif event.dict['button'] == 5:
                        if cons.CELL_SIZE > 1:
                            cons.CELL_SIZE -= 1
                            cons.FONT_AGENT = pygame.font.Font(None, int(cons.CELL_SIZE * 0.5), bold=True)
                            self.offset_x += cons.CELL_SIZE/2
                            self.offset_y += cons.CELL_SIZE/2
                    elif event.dict['button'] == 1:
                        self.clicked = True
                        pygame.mouse.get_rel()
                        x, y = pygame.mouse.get_pos()
                        #print (C.position_to_cell(C.to_millimiter(x, self.offset_x),C.to_millimiter(y, self.offset_y)))
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.dict['button'] == 1:
                        self.clicked = False
        return True