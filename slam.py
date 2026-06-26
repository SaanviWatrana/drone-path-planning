class SLAMMap:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        # -1 = unknown, 0 = free, 255 = occupied
        self.map = [[-1 for _ in range(cols)] for _ in range(rows)]

    def update(self, lidar_points, cell_size):

        for x, y in lidar_points:

            r = int(y // cell_size)
            c = int(x // cell_size)

            if 0 <= r < self.rows and 0 <= c < self.cols:

                # mark as occupied
                self.map[r][c] = 255

    def mark_free(self, x, y, cell_size):

        r = int(y // cell_size)
        c = int(x // cell_size)

        if 0 <= r < self.rows and 0 <= c < self.cols:
            if self.map[r][c] == -1:
                self.map[r][c] = 0

    def get_map(self):
        return self.map