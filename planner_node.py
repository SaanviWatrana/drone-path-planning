from astar import astar
from path_smoother import smooth_path


class PlannerNode:

    def __init__(self, costmap):

        self.costmap = costmap

        self.last_start = None
        self.last_goal = None
        self.last_path = []

    # -------------------------------------------------

    def build_costmap(

        self,

        obstacles,

        predictions,

        cell_size

    ):

        self.costmap.reset()

        # Current obstacles

        for obstacle in obstacles:

            row = int(

                obstacle.y // cell_size

            )

            col = int(

                obstacle.x // cell_size

            )

            self.costmap.add_obstacle(

                row,

                col,

                inflation_radius=2

            )

        # Predicted obstacles

        self.costmap.add_predicted_obstacles(

            predictions,

            cell_size

        )

    # -------------------------------------------------

    def compute(

        self,

        start,

        goal,

        obstacles,

        predictions,

        cell_size

    ):

        # Return cached path if possible

        if (

            start == self.last_start

            and

            goal == self.last_goal

            and

            len(self.last_path) > 0

        ):

            return self.last_path

        # Build dynamic costmap

        self.build_costmap(

            obstacles,

            predictions,

            cell_size

        )

        planning_grid = self.costmap.get_grid()

        path = astar(

            planning_grid,

            start,

            goal

        )

        # Smooth path

        path = smooth_path(

            planning_grid,

            path

        )

        self.last_start = start
        self.last_goal = goal
        self.last_path = path

        return path