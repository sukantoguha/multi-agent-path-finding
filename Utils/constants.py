import pygame
from Utils.Agents.JobManager import JobManagerRandom
import enum

# Colors in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0,128,0)
DARK_GREEN = (0,100,0)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (255,255,0)
SILVER = (192,192,192)

# Display zoom
CELL_SIZE = 20

# Fonts for labels
pygame.font.init()
FONT_TIMER = pygame.font.Font(None, 20, bold=False)
FONT_AGENT =  pygame.font.Font(None, int(CELL_SIZE * 0.5), bold=True)

# Display colors
PAINT = {'@': BLACK, 'T': DARK_GREEN, '.': WHITE, 'W': BLUE, 'S': SILVER, 'p': YELLOW, 'P': SILVER, 'R': ORANGE, 'PROCESS': GREEN}
STATIC_FEATURES = ['@','T', '.', 'W']


# Screen update rate
STEPS_PER_SCREEN = 1

# Robot's speed limit (cells per step)
SPEED_LIMIT = 2

# Default job manager policy
JOB_MANAGER = JobManagerRandom()

# creating enumerations for robot's actions
class Action(enum.Enum):
    turn_north = 0
    turn_east = 1
    turn_south = 2
    turn_west = 3
    accelerate = 4
    decelerate = 5
    lift = 6
    drop = 7
    no_op = 8
    process = 9

# Robot's actions that are applicable for navigation
NAV_ACTIONS = [0,1,2,3,4,5,8]


def cell_to_position(index, offset):
        return index * CELL_SIZE + offset

def cell_to_index(x,y,width):
        return x + y * width

def edge_to_index(pos_x,pos_y,heading, width, height):
        # Since edges are undirected we only consider S, E directions, (x,y,N) becomes (x,y-1,S)
        if heading == 'W':
            pos_x -= 1
            heading = 'E'
        elif heading == 'N':
            pos_y -= 1
            heading = 'S'
        ans = cell_to_index(pos_x,pos_y,width)
        if heading == 'S':
            ans += 2 * width * height
        return ans


def display_agent_label(position_x, position_y, offset_x, offset_y, index, screen):
    label = FONT_AGENT.render(str(index), True, BLACK,WHITE)
    screen.blit(label, (cell_to_position(position_x, offset_x) + CELL_SIZE/2 - label.get_width() / 2
                            ,cell_to_position(position_y, offset_y) + CELL_SIZE/2 - label.get_height() / 2))