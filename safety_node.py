import math


class SafetyNode:

    def __init__(self, drone, obstacles, width=800, height=600):

        self.drone = drone
        self.obstacles = obstacles

        self.width = width
        self.height = height

        self.warning_distance = 100
        self.emergency_distance = 45

    # ------------------------------------------------

    def nearest_obstacle_distance(self):

        minimum = float("inf")

        for obstacle in self.obstacles:

            ox = obstacle.x + obstacle.size / 2
            oy = obstacle.y + obstacle.size / 2

            distance = math.hypot(

                self.drone.x - ox,

                self.drone.y - oy

            )

            minimum = min(minimum, distance)

        return minimum

    # ------------------------------------------------

    def collision_risk(self):

        return (

            self.nearest_obstacle_distance()

            <

            self.warning_distance

        )

    # ------------------------------------------------

    def emergency_stop(self):

        return (

            self.nearest_obstacle_distance()

            <

            self.emergency_distance

        )

    # ------------------------------------------------

    def safe_speed(self):

        distance = self.nearest_obstacle_distance()

        if distance < self.emergency_distance:

            return 0

        if distance < self.warning_distance:

            ratio = (

                distance -

                self.emergency_distance

            ) / (

                self.warning_distance -

                self.emergency_distance

            )

            return max(20, 120 * ratio)

        return 120

    # ------------------------------------------------

    def boundary_risk(self):

        margin = 20

        if self.drone.x < margin:
            return True

        if self.drone.y < margin:
            return True

        if self.drone.x > self.width - margin:
            return True

        if self.drone.y > self.height - margin:
            return True

        return False

    # ------------------------------------------------

    def goal_reached(self, goal, cell_size):

        gx = goal[1] * cell_size + cell_size / 2
        gy = goal[0] * cell_size + cell_size / 2

        distance = math.hypot(

            self.drone.x - gx,

            self.drone.y - gy

        )

        return distance < 10

    # ------------------------------------------------

    def status(self):

        if self.emergency_stop():

            return "EMERGENCY STOP"

        if self.collision_risk():

            return "WARNING"

        if self.boundary_risk():

            return "BOUNDARY"

        return "SAFE"