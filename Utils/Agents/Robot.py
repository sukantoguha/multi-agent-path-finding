import time
import pygame

import Utils.constants as cons
from Utils.constants import Action
from Planning.BestFirstSearch import BestFirstSearch as bfs
from Utils.Agents.JobManager import Task
from Planning.SingleAgentState import SingleAgentState as state

class Robot:

    def __init__(self, x,y,index, warehouse, job_manager):
        self.position_x = x
        self.position_y = y
        self.index = index
        self.goal_x = -1
        self.goal_y = -1
        self.heading = 'N'
        self.velocity = 0
        self.carry = None
        self.warehouse = warehouse
        self.plan = [Action.no_op]
        self.job_manager = job_manager
        self.constraint = [] #added
        self.occupies = [] #added

    def copy(self):
        cpy = Robot(self.position_x, self.position_y, self.index, self.warehouse, None)
        cpy.heading = self.heading
        cpy.velocity = self.velocity
        cpy.carry = self.carry
        cpy.goal_x = self.goal_x
        cpy.goal_y = self.goal_y
        return cpy

    def goal_copy(self):
        cpy = Robot(self.goal_x, self.goal_y, self.index, self.warehouse, None)
        cpy.heading = None
        cpy.velocity = 0
        cpy.carry = None
        return cpy

    def display(self, screen, offset_x, offset_y):
        image_path = "Figures/"
        image_path += self.heading
        image_path += ".png"
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (cons.CELL_SIZE, cons.CELL_SIZE))

        screen.blit(image, [cons.cell_to_position(self.position_x, offset_x), cons.cell_to_position(self.position_y,
                                                                                                    offset_y)])
        cons.display_agent_label(self.position_x, self.position_y, offset_x, offset_y, self.index, screen)

    def cbs_step(self):  
        occupies_cells = []
        occupies_edges = []

        if self.heading == 'N':
            #print("N")
            for dy in range(1, self.velocity + 1):
                #print("self.position_x : ", self.position_x)
                #print("self.position_y : ", self.position_y)
                occupies_cells.append([self.position_x, self.position_y - dy])
                occupies_edges.append([self.position_x, self.position_y - dy, 'S'])
            self.position_y -= self.velocity
        elif self.heading == 'S':
            #print("S")
            for dy in range(1, self.velocity + 1):
                #print("self.position_x : ", self.position_x)
                #print("self.position_y : ", self.position_y)
                occupies_cells.append([self.position_x, self.position_y + dy])
                occupies_edges.append([self.position_x, self.position_y + dy, 'N'])
            self.position_y += self.velocity
        elif self.heading == 'E':
            #print("E")
            for dx in range(1, self.velocity + 1):
                #print("self.position_x : ", self.position_x)
                #print("self.position_y : ", self.position_y)
                occupies_cells.append([self.position_x + dx, self.position_y])
                occupies_edges.append([self.position_x + dx, self.position_y, 'W'])
            self.position_x += self.velocity
        elif self.heading == 'W':
            #print("W")
            for dx in range(1, self.velocity + 1):
                #print("self.position_x : ", self.position_x)
                #print("self.position_y : ", self.position_y)
                occupies_cells.append([self.position_x - dx, self.position_y])
                occupies_edges.append([self.position_x - dx, self.position_y, 'E'])
            self.position_x -= self.velocity
        if self.velocity == 0:
            #print("velocy =0")
            #print("self.position_x : ", self.position_x)
            #print("self.position_y : ", self.position_y)
            occupies_cells.append([self.position_x,self.position_y])

        if self.carry is not None:
            print("carry is not None")
            self.carry.position_x = self.position_x
            self.carry.position_y = self.position_y
        return occupies_cells, occupies_edges


    def step(self):  

        if len(self.plan) == 1:
            self.plan_task()
        self.perform_action(Action(self.plan.pop()))
        occupies_cells = []
        occupies_edges = []

        if self.heading == 'N':
            #print("N")
            for dy in range(1, self.velocity + 1):
                #print("self.position_x : ", self.position_x)
                #print("self.position_y : ", self.position_y)
                occupies_cells.append([self.position_x, self.position_y - dy])
                occupies_edges.append([self.position_x, self.position_y - dy, 'S'])
            self.position_y -= self.velocity
        elif self.heading == 'S':
            #print("S")
            for dy in range(1, self.velocity + 1):
                #print("self.position_x : ", self.position_x)
                #print("self.position_y : ", self.position_y)
                occupies_cells.append([self.position_x, self.position_y + dy])
                occupies_edges.append([self.position_x, self.position_y + dy, 'N'])
            self.position_y += self.velocity
        elif self.heading == 'E':
            #print("E")
            for dx in range(1, self.velocity + 1):
                #print("self.position_x : ", self.position_x)
                #print("self.position_y : ", self.position_y)
                occupies_cells.append([self.position_x + dx, self.position_y])
                occupies_edges.append([self.position_x + dx, self.position_y, 'W'])
            self.position_x += self.velocity
        elif self.heading == 'W':
            #print("W")
            for dx in range(1, self.velocity + 1):
                #print("self.position_x : ", self.position_x)
                #print("self.position_y : ", self.position_y)
                occupies_cells.append([self.position_x - dx, self.position_y])
                occupies_edges.append([self.position_x - dx, self.position_y, 'E'])
            self.position_x -= self.velocity
        if self.velocity == 0:
            #print("velocy =0")
            #print("self.position_x : ", self.position_x)
            #print("self.position_y : ", self.position_y)
            occupies_cells.append([self.position_x,self.position_y])

        if self.carry is not None:
            print("carry is not None")
            self.carry.position_x = self.position_x
            self.carry.position_y = self.position_y
        return occupies_cells, occupies_edges

    def perform_action(self, action):
        if str.startswith(action.name,"turn"):
            if self.velocity != 0:
                raise ValueError('Robot %d can\'t turn while in motion' % self.index)
        if action.name == "turn_north":
            self.heading = 'N'
        elif action.name == "turn_east":
            self.heading = 'E'
        elif action.name == "turn_south":
            self.heading = 'S'
        elif action.name == "turn_west":
            self.heading = 'W'
        elif action.name == "accelerate":
            self.velocity += 1
            if self.velocity > cons.SPEED_LIMIT:
                raise ValueError('Robot %d (velocity %d) can\'t exceed the speed limit (%d cells per timestep)' %
                                 (self.index, self.velocity, cons.SPEED_LIMIT))
        elif action.name == "decelerate":
            self.velocity -= 1
            if self.velocity < 0:
                raise ValueError('Robot %d can\'t decelerate from velocity of zero' % self.index)
        elif action.name == "lift":
            self.carry = self.warehouse.get_pod(self.position_x,self.position_y)
            if self.velocity != 0:
                raise ValueError('Robot %d can\'t lift while in motion' % self.index)
            if self.carry is None:
                raise ValueError('There is no pod to be lift at the current location of Robot %d' % self.index)
            if self.carry.assigned != self:
                raise ValueError('Robot %d cannot mount Pod %d, it is not assigned to it' % (self.index,
                                                                                             self.carry.index))
        elif action.name == "drop":
            if self.carry is None:
                raise ValueError('Robot %d is not carrying any pod, can\'t perform drop' % self.index)
            if self.velocity != 0:
                raise ValueError('Robot %d can\'t drop while in motion' % self.index)
            self.carry.assigned = None
            self.carry = None
        elif action.name == "process":
            self.perform_process()
        elif action.name == "no_op":
            return
        else:
            raise ValueError('Robot %d - invalid action' % self.index)

    def perform_process(self):
        if self.carry is None:
            raise ValueError('Robot %d is not carrying any pod, can\'t perform process' % self.index)
        station = self.warehouse.get_station(self.position_x,self.position_y)
        if station is None:
            raise ValueError('Robot %d can\'t process, no station at current location' % self.index)
        station.process = True

    ###is not being used###
    def manual_control(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.perform_action(Action.turn_north)
        elif pressed[pygame.K_RIGHT]:
            self.perform_action(Action.turn_east)
        elif pressed[pygame.K_DOWN]:
            self.perform_action(Action.turn_south)
        elif pressed[pygame.K_LEFT]:
            self.perform_action(Action.turn_west)
        elif pressed[pygame.K_RIGHTBRACKET]:
            self.perform_action(Action.accelerate)
        elif pressed[pygame.K_LEFTBRACKET]:
            self.perform_action(Action.decelerate)
        elif pressed[pygame.K_1]:
            self.perform_action(Action.lift)
        elif pressed[pygame.K_2]:
            self.perform_action(Action.drop)
        time.sleep(0.05)

    def plan_path(self):
        self.plan.clear()
        start_time = time.clock()
        start = state(None,self.copy(),0,-1)
 
        self.plan = bfs.plan(start)

    def plan_task(self):
        # The last action remaining in the plan field represents the task that was just performed
        if self.plan[0] == Action.no_op: # The robot is idle
            self.goal_x, self.goal_y = self.job_manager.assign_task(self, Task.pick)
            self.plan_path()
            lift = [Action.lift,Action.lift]
            self.plan = lift + self.plan
        elif self.plan[0] == Action.lift: # The robot just mounted its assigned pod
            self.goal_x, self.goal_y = self.job_manager.assign_task(self, Task.deliver)
            self.plan_path()
            process = [Action.process,Action.process,Action.process,Action.process,Action.process,Action.process]
            self.plan = process + self.plan
        elif self.plan[0] == Action.process: # The robot finished delivering the pod
            self.goal_x, self.goal_y = self.job_manager.assign_task(self, Task.store)
            self.plan_path()
            drop = [Action.no_op, Action.drop]
            self.plan = drop + self.plan

    def is_valid_plan(self):
        return self.warehouse.is_valid(self)

    def at_goal(self):
        return self.position_x == self.goal_x and self.position_y == self.goal_y and self.velocity == 0


    def __eq__(self, other):
        if self.position_x != other.position_x:
            return False
        elif self.position_y != other.position_y:
            return False
        elif self.index != other.index:
            return False
        elif self.velocity != other.velocity:
            return False
        elif self.heading is None or other.heading is None: # Goal state has heading = None since heading is not
            # important
            return True
        elif self.heading != other.heading:
            return False
        else:
            return True

    def __hash__(self):
        return hash(str(self.position_x) + str(self.position_y) + str(self.index) + self.heading + str(self.velocity))


class RobotNoCarry(Robot):

    ma_planner = 'maA*'

    def __init__(self, x,y,index, warehouse, job_manager):
        Robot.__init__(self,x,y,index, warehouse, job_manager)


    def plan_task(self):
        self.warehouse.assign_non_carying_robots()
        self.warehouse.multiagent_plan(self.ma_planner)

    def assign_goal(self):
        new_goal_x, new_goal_y = self.job_manager.assign_task(self, Task.deliver)
        while not self.warehouse.is_unique_goal(new_goal_x,new_goal_y):
            new_goal_x, new_goal_y = self.job_manager.assign_task(self, Task.deliver)
        self.goal_x = new_goal_x
        self.goal_y = new_goal_y

    def perform_process(self):
        station = self.warehouse.get_station(self.position_x,self.position_y)
        if station is None:
            raise ValueError('Robot %d can\'t process, no station at current location' % self.index)
        station.process = True

