class JobManagerRandom:

    @staticmethod
    def assign_task(robot, task):
        if task == Task.pick:
            # Assign unassigned pod
            pod = robot.warehouse.random_unassigned_pod()
            pod.assigned = robot
            return pod.position_x, pod.position_y
        elif task == Task.deliver:
            # assign station
            station = robot.warehouse.random_station()
            return station.position_x, station.position_y
        elif task == Task.store:
            # Assign stowage location
            pod = robot.carry
            return pod.original_x, pod.original_y



import enum
# creating enumerations for robot's tasks
class Task(enum.Enum):
    pick = 0
    deliver = 1
    store = 3