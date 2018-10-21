from Utils.constants import Action, NAV_ACTIONS
import Utils.constants as C
from Planning.BestFirstSearch import BestFirstSearch as bfs
from Planning.SingleAgentState import SingleAgentState 
from heapq import heappush, heappop
from Planning.CBSSingleAgentState import CBSSingleAgentState 
import sys

conflict=0

class CBS_State:

    def __init__(self, robots, g, constraint, predecessor, plans, all_agent_occupy, min, sum):
        self.robots = robots # All robots to be planned
        self.g = sum  # The total travel time over all robots
        self.h = 0  # Don't attempt to find an admissible heuristic for CBS. Just leave it as zero.
        # setting a heuristic for CBS is not trivial (you can come talk with me about it)

        self.p = predecessor  # The state which generated this step, 'None' for root
        self.constraint = constraint  # The constraint generated from the conflict found in the predecessor.
        # In order to get all constraints for this node, go along the predecessors until the root and collect
        # all constraints

        self.plans = plans  # The plans affiliated with this node. The plan for one agent needs to be updated (the
        # agent for which the new constraint applies to). g value must be updated accordingly.
        self.timeline=min
        self.occupied=all_agent_occupy

    '''
    def sic_computation(self):
        cbsstate = CBSSingleAgentState(None,self.agents[0], 0, -1)
        sum=0
        for i in self.robots[0]:
            sum+= cbsstate.sic(i)
        return sum


    def plan_computation(self):
        ma_plan=[]
        for i in self.robots[0]:
            sum+= cbsstate.sic(i)
            #ma_plan.append(cbsstate.plan(i))
            each_agent_plan = cbsstate.plan(i)
            ma_plan.append(each_agent_plan)


    def time_computation(self, plans):
        max=0
        #Determining the timstamp by computing maximum length of path.
        for i in self.plans:
            if max < len(i):
                max = len(i)
        return max
    '''

    def required_computation(self, all_agent_occupy, ma_plan):
        cbsstate = CBSSingleAgentState(None,self.agents[0], 0, -1)
        for i in self.robots:
            occupies=[]
            sum+= cbsstate.sic(i)
            each_agent_plan = cbsstate.plan(i)
            i.plan = each_agent_plan

            #==== Generating path for each agent ====
            length = len(each_agent_plan)-1

            while length >=0:
                each_action = each_agent_plan[length]
                i.perform_action(each_action)
                occ = i.cbs_step()
                occupies.append(C.cell_to_index(occ[0][0][0], occ[0][0][1], width))
            
                length-=1
            i.occupies = occupies
            all_agent_occupy.append(occupies)  #contains list of list of all the agents coordinate position.
            ma_plan.append(each_agent_plan)

            '''
            max=0
            #Determining the timstamp by computing maximum length of path.
            for i in ma_plan:
                if max < len(i):
                    max = len(i)
            '''
            max=0
            #Determining the timstamp by computing maximum length of path.
            for i in ma_plan:
                if max < len(i):
                    max = len(i)

        return sum, max

    def compare(self, occu1, occu2):
        min_len=0
        l1 = len(occu1)
        l2 = len(occu2)
        if l1 < l2:
            min_len = l1
        else: min_len = l2
        i=0
        j=0
        k=0
        while i < min_len:
            if(occu1[j] == occu2[k]):
                return occu1[j]
            else:
                j+=1
                k+=1
            i+=1
        return -1

    # Generate all valid successors
    def expand(self):
        successors = []
        conflict_state=0
        time=0
        child_robot1=None
        child_robot2=None

        colliding_robots=set()
        #conflict_information= {}
        #info = []
        robot_robot_collision={}
        robot_time_collision={}
        robot_position_collision={}

        for time in self.timeline:
            for robo1 in self.robots:
                child_robot1 = robo1.copy()
                for robo2 in self.robots:
                    child_robot2 = robo2.copy()
                    if(child_robot1 == child_robot2):
                        continue
                    else:
                        conflict_state = self.compare(child_robot1.occupies, child_robot2.occupies)

                        if(conflict_state != -1):
                            colliding_robots.add(child_robot1)
                            colliding_robots.add(child_robot2)
                            #info.append(time)
                            #info.append(conflict_state)
                            #info.append(child_robot2)
                            #conflict_information[child_robot1] = info
                            robot_robot_collision[child_robot1]=child_robot2
                            robot_time_collision[child_robot1]=time
                            robot_position_collision[child_robot1]=conflict_state

            if colliding_robots != None:
                break

        for i in colliding_robots:
            all_agent_occupy = []
            ma_plan = []
            i.constraint.append(conflict_information[i])
            sum, max = required_computation(all_agent_occupy, ma_plan)
            successors.append(CBS_State(self, self.robots, sum, [] , self, ma_plan, all_agent_occupy, max, sum))  
            #robots, g, constraint, predecessor, plans, all_agent_occupy, max, sum

        return successors

    # Return a list of list of actions
    # actions[i] points to a list of actions for robot i. actions[i][0] is the last action to be performed
    # actions[i][len(actions[i]) - 1] is the first (next) action to be performed.
    def get_plan(self, plan):
        if self.p is not None:
            plan.append(self.action)
            self.p.get_plan(plan)
        return

    # Return True if this is the goal state
    def is_goal(self):  
        # Todo: Your job
        if conflict == 0:
            return True
        else:
            return False
        #raise NotImplementedError


    # The following comparators are needed for the open and closed lists (used by Best-First Search)
    def __eq__(self, other):
        # Todo: Your job
        for x in range(len(self.robots)):
            if self.robots[x] != other.robots[x]:
                return False
        return True
        #raise NotImplementedError

    def __lt__(self, other):
        # Todo: Your job
        return self.g + self.h < other.g + other.h
        #raise NotImplementedError

    def __ge__(self, other):
        # Todo: Your job
        return not self < other
        #raise NotImplementedError

    # Hash function needed for the closed list. For efficiency try to produce unique values for unique states
    def __hash__(self):
        # Todo: Your job
        ans = 0
        for r in self.robots:
            ans += hash(r)
        return ans
        #raise NotImplementedError

    # Name the state for easy debugging
    def __str__(self):
        # Todo: Your job
        ans = ''
        for r in self.robots:
            ans += "Robot[%d]-(%d,%d,%s,%d) " %(r.index,r.position_x, r.position_y, r.heading, r.velocity)
        return ans
        #raise NotImplementedError