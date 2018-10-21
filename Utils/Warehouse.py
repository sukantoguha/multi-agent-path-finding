from Utils.CollisionDetection import CollisionDetection, CollisionDetectionEdge
from Planning.MultiagentState import MultiagentState
from Planning.CBS_State import CBS_State
from Planning.BestFirstSearch import BestFirstSearch
from Utils.Agents.Robot import RobotNoCarry
from Planning.SingleAgentState import SingleAgentState as state
from Planning.CBSSingleAgentState import CBSSingleAgentState 
from Utils.constants import Action
import random
import time
import Utils.constants as cons
import Utils.constants as C
import re
import sys


class Warehouse:

    def __init__(self, map):
        self.map = map
        self.agents = map.get_agents(self)
        self.reservations_robots = CollisionDetection(self.map.height, self.map.width)
        self.reservations_pods = CollisionDetection(self.map.height, self.map.width)

    def display(self, screen, offset_x, offset_y):
        self.map.display(screen, offset_x, offset_y)
        for agent_type in self.agents:
            for agent in agent_type:
                agent.display(screen, offset_x, offset_y)

    def get_pod(self, at_x, at_y):
        for pod in self.agents[1]:
            if pod.position_x == at_x and pod.position_y == at_y:
                return pod
        return None

    def get_station(self, at_x, at_y):
        for station in self.agents[2]:
            if station.position_x == at_x and station.position_y == at_y:
                return station
        return None

    def step(self):
        self.step(self.agents[0])

    def step(self):
        cell_record_robots = CollisionDetection(self.map.height, self.map.width)
        edge_record_robots = CollisionDetectionEdge(self.map.height, self.map.width)
        cell_record_pods = CollisionDetection(self.map.height, self.map.width)
        for r in self.agents[0]:
            occupied = r.step()
            for coordinate in occupied[0]:
                cell_record_robots.add(coordinate[0],coordinate[1])
                if r.carry is not None:
                    cell_record_pods.add(coordinate[0],coordinate[1])
            for edge in occupied[1]:
                edge_record_robots.add(edge[0], edge[1], edge[2])
        
        for p in self.agents[1]:
            if p.assigned is None:
                cell_record_pods.add(p.position_x, p.position_y)
            elif p.assigned.carry is None:
                cell_record_pods.add(p.position_x, p.position_y)

        #print("cell_record_robots : ", cell_record_robots)
        #print("edge_record_robots : ", edge_record_robots)
        #print("cell_record_pods : ", cell_record_pods)

    def are_open_cells(self,cells, mounted):
        for cell in cells:
            if cell[0] < 0 or cell[1] < 0:
                return False
            if len(self.map.grid) <= cell[1]:
                return False
            if len(self.map.grid[cell[1]]) <= cell[0]:
                return False
            if mounted:
                if mounted.original_x == cell[0] and mounted.original_y == cell[1]:
                    return True
                if self.map.grid[cell[1]][cell[0]] != '.':
                    return False
            elif self.map.grid[cell[1]][cell[0]] != 'P' and self.map.grid[cell[1]][cell[0]] != '.':
                return False
        return True

    def random_unassigned_pod(self):  #Just check
        pod = random.choice(self.agents[1])
        flag=0

        for i in range(len(self.agents[1])):
            pod = self.agents[1][i]
            if pod.assigned:continue
            else:
                flag=1
                break
        if flag==1:
            return pod

        '''
        while pod.assigned: # TODO check that unassigned pods exist #Theirs
            pod = random.choice(self.agents[1])
        return pod
        '''

    def random_station(self):
        return random.choice(self.agents[2])

    def is_unique_goal(self,x,y):
        for r in self.agents[0]:
            if r.goal_x == x and r.goal_y == y:
                return False
        return True

    def multiagent_plan(self, planner):
        ma_plan=[]
        all_agent_occupy=[]
        sum=0
        start_time = time.clock()
        if planner == 'maA*':
            root = MultiagentState(None,self.agents[0],0, None)
        elif planner == 'CBS':
            cbsstate = CBSSingleAgentState(None,self.agents[0], 0, -1) #state(None,self.copy(),0,-1)            
            height = self.map.height
            width = self.map.width

            for i in self.agents[0]:
                occupies=[]
                sum+= cbsstate.sic(i)
                #ma_plan.append(cbsstate.plan(i))
                each_agent_plan = cbsstate.plan(i)
                #print("each_agent_plan : ", each_agent_plan)
                i.plan = each_agent_plan

                #==== Generating path for each agent ====
                #for each_agent_plan in ma_plan:  
                length = len(each_agent_plan)-1

                #print("length : ", length)
                while length >=0:
                    each_action = each_agent_plan[length]
                    #print("each_action : ", each_action)

                    i.perform_action(each_action)
                    occ = i.cbs_step()
                    #print("occ[0][0] : ", occ[0][0])
                    #print("occ[0][0][0] : ", occ[0][0][0])
                    #print("occ[0][0][1] : ", occ[0][0][1])

                    #occupies.append(occ[0][0])
                    occupies.append(C.cell_to_index(occ[0][0][0], occ[0][0][1], width))
                    #print("occupies : ", occupies)

                    length-=1
                i.occupies = occupies
                all_agent_occupy.append(occupies)  #contains list of list of all the agents coordinate position.
                ma_plan.append(each_agent_plan)

            max = 0#INT_MAX#sys.maxint
            #Determining the timstamp by computing maximum length of path.
            for i in ma_plan:
                if max > len(i):
                    max = len(i)

            '''
            print("sum -- : ", sum)
            print("max -- : ", max)
            print("ma_plan -- : ", ma_plan)
            print("all_agent_occupy -- : ", all_agent_occupy)
            '''
            print("calling CBS_state: ")
            root = CBS_State(self.agents[0], 0, [], None,ma_plan, all_agent_occupy, max,  sum) #robots, g, constraint, predecessor, plans
            #print("root : ", root)

            '''
            for i in self.agents[0]:
                print("i.plan : ", i.plan)
                print("i.occupies : ", i.occupies)
            '''

        print("calling bfs on root of CBS : ")
        ma_plan = BestFirstSearch.plan(root) 
        #print("ma_plan : ", ma_plan)

        for x in range(len(ma_plan)):
            self.agents[0][x].plan = [Action.process,Action.process,Action.process,Action.process] + ma_plan[x]

    def assign_non_carying_robots(self):
        for rnc in self.agents[0]:
            if type(rnc) is RobotNoCarry:
                rnc.goal_x, rnc.goal_y = -1, -1
        for rnc in self.agents[0]:
            if type(rnc) is RobotNoCarry:
                rnc.assign_goal()
