# import the pygame module, so you can use it
import pygame
import os
#import Utils
from Utils.map import map as mp
from Utils.Display import Display as dis
import Utils.constants as C
from Utils.Agents.Robot import RobotNoCarry
import random


# define a main function
def main():
    # map file
    current_dir = os.path.dirname(__file__)
    #scenario = 'Warehouse-1.map' # Scenario to run ## Given map
    #scenario = 'arena2-1.map' # Scenario to run ## Q#1
    #scenario = 'Warehouse-MAPF-2.map' # Scenario to run ## Q#2
    scenario = 'lak303d-MAPF-2.map' #Scenario to run ## Q#3
    map_path = os.path.join(current_dir, 'scenarios/' + scenario)
    #RobotNoCarry.ma_planner = 'maA*'  # Change to 'CBS' when running CBS
    RobotNoCarry.ma_planner = 'CBS' ## Q#3
    map = mp(map_path)   ##calling map constructor.

    #print("map : ", map)
    print("map.height : ", map.height)
    print("map.width : ", map.width)
    C.CELL_SIZE = max(int(500/map.height),1)
    #print("C.CELL_SIZE : ", C.CELL_SIZE)
    display = dis(map)
    display.update_screen()
    random.seed(2018)
    display.run()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()