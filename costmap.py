import math


class CostMap:

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols

        self.cost = [

            [0 for _ in range(cols)]

            for _ in range(rows)

        ]

    # ------------------------------------------------

    def reset(self):

        self.cost = [

            [0 for _ in range(self.cols)]

            for _ in range(self.rows)

        ]

    # ------------------------------------------------

    def add_obstacle(

        self,

        row,

        col,

        inflation_radius=2,

        obstacle_cost=255

    ):

        for r in range(

            row - inflation_radius,

            row + inflation_radius + 1

        ):

            for c in range(

                col - inflation_radius,

                col + inflation_radius + 1

            ):

                if 0 <= r < self.rows and 0 <= c < self.cols:

                    distance = math.sqrt(

                        (r - row) ** 2 +

                        (c - col) ** 2

                    )

                    if distance <= inflation_radius:

                        if distance == 0:

                            self.cost[r][c] = obstacle_cost

                        else:

                            value = int(

                                obstacle_cost *

                                (1 - distance /

                                 (inflation_radius + 1))

                            )

                            self.cost[r][c] = max(

                                self.cost[r][c],

                                value

                            )

    # ------------------------------------------------

    def add_predicted_obstacles(

        self,

        predictions,

        cell_size

    ):

        for obstacle in predictions:

            total = len(obstacle)

            for index, future in enumerate(obstacle):

                x, y, size = future

                row = int(y // cell_size)
                col = int(x // cell_size)

                if not (

                    0 <= row < self.rows and

                    0 <= col < self.cols

                ):

                    continue

                # Near future gets higher cost

                inflation = max(

                    1,

                    3 - index // 2

                )

                cost = max(

                    100,

                    255 - index * 35

                )

                self.add_obstacle(

                    row,

                    col,

                    inflation_radius=inflation,

                    obstacle_cost=cost

                )

    # ------------------------------------------------

    def is_blocked(

        self,

        row,

        col

    ):

        return self.cost[row][col] >= 220

    # ------------------------------------------------

    def get_cost(

        self,

        row,

        col

    ):

        return self.cost[row][col]

    # ------------------------------------------------

    def get_grid(self):

        grid = [

            [0 for _ in range(self.cols)]

            for _ in range(self.rows)

        ]

        for r in range(self.rows):

            for c in range(self.cols):

                if self.cost[r][c] >= 220:

                    grid[r][c] = 1

        return grid