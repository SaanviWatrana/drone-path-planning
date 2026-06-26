import math

class ControllerNode:
    def __init__(self, drone, obstacles, bus=None, drone_id=0):
        self.drone = drone
        self.obstacles = obstacles

        self.bus = bus
        self.id = drone_id

        self.path = []
        self.index = 0

        self.vx = 0
        self.vy = 0
        self.max_speed = 120

    def set_path(self, path):
        self.path = path or []
        self.index = 0

        # publish if ROS mode
        if self.bus:
            self.bus.publish_path(self.id, self.path)

    def load_path(self):
        if self.bus:
            self.path = self.bus.get_path(self.id)

    def step(self, dt):

        if not self.path and self.bus:
            self.load_path()

        if not self.path or self.index >= len(self.path):
            return

        r, c = self.path[self.index]

        tx = c * self.drone.cell_size + self.drone.cell_size / 2
        ty = r * self.drone.cell_size + self.drone.cell_size / 2

        dx = tx - self.drone.x
        dy = ty - self.drone.y

        dist = math.hypot(dx, dy)

        if dist < 8:
            self.index += 1
            return

        dx /= (dist + 1e-6)
        dy /= (dist + 1e-6)

        vx = dx * self.max_speed
        vy = dy * self.max_speed

        # obstacle avoidance
        for o in self.obstacles:
            ox = self.drone.x - o.x
            oy = self.drone.y - o.y
            d = math.hypot(ox, oy)

            if 0 < d < 60:
                vx += ox * 40 / (d + 1)
                vy += oy * 40 / (d + 1)

        self.vx = 0.85 * self.vx + 0.15 * vx
        self.vy = 0.85 * self.vy + 0.15 * vy

        self.drone.x += self.vx * dt
        self.drone.y += self.vy * dt