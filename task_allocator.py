import math

class TaskAllocator:
    def __init__(self, drones, tasks):
        self.drones = drones
        self.tasks = tasks
        self.assignments = {}

    def distance(self, d, task):
        return math.hypot(d.x - task[0], d.y - task[1])

    def allocate(self):
        unassigned_tasks = self.tasks[:]
        self.assignments = {}

        used_drones = set()

        for task in unassigned_tasks:

            best_drone = None
            best_cost = float("inf")

            for d in self.drones:

                if d in used_drones:
                    continue

                cost = self.distance(d, task)

                if cost < best_cost:
                    best_cost = cost
                    best_drone = d

            if best_drone:
                self.assignments[best_drone] = task
                used_drones.add(best_drone)

        return self.assignments