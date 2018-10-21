import pygame
import Utils.constants as cons
from Utils.Agents.Robot import Robot, RobotNoCarry
from Utils.Agents.Pod import Pod
from Utils.Agents.Station import Station

class map:

    def __init__(self, path_to_file):
        file = open(path_to_file, 'r')
        y=0
        for line in file:
            if line.startswith( 'type' ):
                continue
            elif line.startswith( 'height' ):
                self.height = int(line[6:])
                continue
            elif line.startswith( 'width' ):
                self.width = int(line[5:])
                continue
            elif line.startswith( 'map' ):
                self.grid = [[] for i in range(self.height)]
                continue
            elif len(line) > 0:
                self.grid[y] = list(line)
                y += 1

    # Get robots, pods, and packing stations
    def get_agents(self, warehouse):
        agents = [[] for i in range(3)]
        robot_index = 0
        pod_index = 0
        station_index = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 'R':
                    agents[0].append(Robot(x,y,robot_index,warehouse,cons.JOB_MANAGER))
                    robot_index += 1
                    self.grid[y][x] = '.'
                elif self.grid[y][x] == 'P':
                    agents[1].append(Pod(x,y,pod_index))
                    pod_index += 1
                    #self.grid[y][x] = '.'
                elif self.grid[y][x] == 'S':
                    agents[2].append(Station(x,y,station_index))
                    station_index += 1
                    self.grid[y][x] = '.'
                elif self.grid[y][x] == 'r':
                    agents[0].append(RobotNoCarry(x,y,robot_index,warehouse,cons.JOB_MANAGER))
                    robot_index += 1
                    self.grid[y][x] = '.'
        return agents

    def display(self, screen, offset_x, offset_y):
        for y in range(self.height):
            for x in range(self.width):
                screen.fill(cons.PAINT[self.grid[y][x]], [cons.cell_to_position(x,offset_x),
                                 cons.cell_to_position(y,offset_y), cons.CELL_SIZE, cons.CELL_SIZE])

