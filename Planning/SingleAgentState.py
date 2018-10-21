import Utils.constants as cons
from Utils.constants import Action, NAV_ACTIONS


class SingleAgentState:
    #https://www.geeksforgeeks.org/a-search-algorithm/
    def manhattan_distance(self):
        h = (abs(self.robot.position_x  - self.robot.goal_x) + 
            abs(self.robot.position_y - self.robot.goal_y))/(cons.SPEED_LIMIT)

        return h

    def __init__(self, p, robot, g, action):
        self.robot = robot
        self.p = p
        self.g = g
        self.h = self.manhattan_distance() # TODO: Your job - Set a better heuristic value # previously it was 0.
        self.action = action

    def expand(self):
        successors = []
        for action in Action:
            if action.value not in NAV_ACTIONS:
                continue  # Lift, drop, and process are not part of the path planning
            child_robot = self.robot.copy()
            child_robot.plan = [action, action]
            try:
                occupies = child_robot.step()
            except ValueError:
                continue  # Ignore illegal actions
            if child_robot.warehouse.are_open_cells(occupies[0], self.robot.carry): 
                #successors.append(SingleAgentState(self, child_robot, self.g + 1, self.h, action))
                successors.append(SingleAgentState(self, child_robot, self.g + 1, action))
        return successors

    def get_plan(self, plan):
        if self.p is not None:
            plan.append(self.action)
            self.p.get_plan(plan)
        return

    def is_goal(self):
        return self.robot.at_goal()

    def __eq__(self, other):
        return self.robot == other.robot

    def __hash__(self):
        return hash(self.robot)

    def __lt__(self, other):
         return self.g + self.h < other.g + other.h

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return self.g + self.h <= other.g + other.h

    def __str__(self):
        return "%d,%d" %(self.robot.position_x, self.robot.position_y)