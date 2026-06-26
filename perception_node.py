class PerceptionNode:
    def __init__(self, grid, obstacles):
        self.grid = grid
        self.obstacles = obstacles

    def get_grid(self):
        return self.grid

    def get_obstacles(self):
        return self.obstacles