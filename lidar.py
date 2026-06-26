import math

class Lidar:
    def __init__(self, obstacles, max_range=120, num_rays=36):
        self.obstacles = obstacles
        self.max_range = max_range
        self.num_rays = num_rays

    def scan(self, x, y):

        points = []

        angle_step = 2 * math.pi / self.num_rays

        for i in range(self.num_rays):

            angle = i * angle_step

            for r in range(0, self.max_range, 5):

                px = x + r * math.cos(angle)
                py = y + r * math.sin(angle)

                hit = False

                for o in self.obstacles:
                    if math.hypot(px - o.x, py - o.y) < o.size / 2:
                        hit = True
                        break

                if hit:
                    points.append((px, py))
                    break

        return points