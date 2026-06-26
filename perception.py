class Perception:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.map = [[0 for _ in range(cols)] for _ in range(rows)]

    def update(self, lidar_points, cell_size):

        # reset local map each cycle (robot only knows current view)
        self.map = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for px, py in lidar_points:

            r = int(py // cell_size)
            c = int(px // cell_size)

            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.map[r][c] = 255  # obstacle detected

    def get_costmap(self):
        return self.map
    def get_grid(self):
        return self.map
    