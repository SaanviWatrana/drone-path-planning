import math


class Controller:

    def __init__(self, drone, obstacles):

        self.drone = drone
        self.obstacles = obstacles

        self.path = []
        self.index = 0

        # Motion limits
        self.max_speed = 150.0
        self.max_acceleration = 300.0

        # Waypoint switching distance
        self.goal_radius = 10

        self.vx = 0.0
        self.vy = 0.0

        self.last_x = drone.x
        self.last_y = drone.y

        self.stuck_timer = 0

    # ------------------------------------------------

    def set_path(self, path):

        self.path = path if path else []
        self.index = 0

    # ------------------------------------------------

    def current_target(self):

        if len(self.path) == 0:
            return None

        if self.index >= len(self.path):
            return None

        row, col = self.path[self.index]

        x = col * self.drone.cell_size + self.drone.cell_size / 2
        y = row * self.drone.cell_size + self.drone.cell_size / 2

        return x, y

    # ------------------------------------------------

    def obstacle_force(self):

        fx = 0.0
        fy = 0.0

        emergency = False

        for obstacle in self.obstacles:

            ox = obstacle.x + obstacle.size / 2
            oy = obstacle.y + obstacle.size / 2

            dx = self.drone.x - ox
            dy = self.drone.y - oy

            distance = math.hypot(dx, dy)

            if distance < obstacle.size / 2 + 10:
                emergency = True

            if 0 < distance < 90:

                strength = 3500 / ((distance + 1) ** 2)

                fx += dx * strength
                fy += dy * strength

        return fx, fy, emergency

    # ------------------------------------------------

    def predicted_obstacle_force(self, predictions):

        fx = 0.0
        fy = 0.0

        if predictions is None:
            return fx, fy

        for obstacle in predictions:

            for index, future in enumerate(obstacle):

                ox, oy, size = future

                dx = self.drone.x - ox
                dy = self.drone.y - oy

                distance = math.hypot(dx, dy)

                if 0 < distance < 120:

                    weight = 1.0 / (index + 1)

                    strength = weight * 2500 / ((distance + 1) ** 2)

                    fx += dx * strength
                    fy += dy * strength

        return fx, fy

    # ------------------------------------------------

    def update(self, dt, predictions=None):

        target = self.current_target()

        if target is None:

            self.vx *= 0.90
            self.vy *= 0.90

            self.drone.x += self.vx * dt
            self.drone.y += self.vy * dt

            return

        tx, ty = target

        dx = tx - self.drone.x
        dy = ty - self.drone.y

        distance = math.hypot(dx, dy)

        # waypoint reached

        if distance < self.goal_radius:

            self.index += 1
            return

        dx /= (distance + 1e-6)
        dy /= (distance + 1e-6)

        # smooth speed profile

        desired_speed = min(

            self.max_speed,

            40 + distance * 1.3

        )

        desired_vx = dx * desired_speed
        desired_vy = dy * desired_speed

        # current obstacle avoidance

        rx, ry, emergency = self.obstacle_force()

        if emergency:

            self.vx = 0
            self.vy = 0

            return

        # future obstacle avoidance

        pfx, pfy = self.predicted_obstacle_force(predictions)

        rx += pfx
        ry += pfy

        desired_vx += rx
        desired_vy += ry

        # acceleration limit

        ax = desired_vx - self.vx
        ay = desired_vy - self.vy

        acceleration = math.hypot(ax, ay)

        if acceleration > self.max_acceleration:

            scale = self.max_acceleration / acceleration

            ax *= scale
            ay *= scale

        self.vx += ax * dt
        self.vy += ay * dt

        # speed clamp

        speed = math.hypot(self.vx, self.vy)

        if speed > self.max_speed:

            scale = self.max_speed / speed

            self.vx *= scale
            self.vy *= scale

        self.drone.x += self.vx * dt
        self.drone.y += self.vy * dt

        # stuck detection

        moved = math.hypot(

            self.drone.x - self.last_x,

            self.drone.y - self.last_y

        )

        if moved < 0.3:

            self.stuck_timer += dt

        else:

            self.stuck_timer = 0

        self.last_x = self.drone.x
        self.last_y = self.drone.y

    # ------------------------------------------------

    def is_stuck(self):

        return self.stuck_timer > 2.0