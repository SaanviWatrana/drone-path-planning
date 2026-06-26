class RobotCore:

    def __init__(

        self,

        perception,

        planner,

        controller,

        safety,

        slam,

        lidar,

        predictor,

        drone,

        obstacles,

        cell_size

    ):

        self.perception = perception
        self.planner = planner
        self.controller = controller
        self.safety = safety
        self.slam = slam
        self.lidar = lidar
        self.predictor = predictor

        self.drone = drone
        self.obstacles = obstacles

        self.cell_size = cell_size

        self.current_path = []

        self.predictions = []

        self.goal = None

        self.need_replan = True

        self.replan_timer = 0.0
        self.replan_interval = 0.5

    # -------------------------------------------------

    def get_robot_cell(self):

        row = int(

            self.drone.y //

            self.cell_size

        )

        col = int(

            self.drone.x //

            self.cell_size

        )

        return (

            row,

            col

        )

    # -------------------------------------------------

    def update_sensors(self):

        lidar_points = self.lidar.scan(

            self.drone.x,

            self.drone.y

        )

        self.perception.update(

            lidar_points,

            self.cell_size

        )

        self.slam.update(

            lidar_points,

            self.cell_size

        )

    # -------------------------------------------------

    def update_predictions(self):

        self.predictions = self.predictor.predict(

            self.obstacles

        )

    # -------------------------------------------------

    def path_is_valid(self):

        if len(self.current_path) == 0:

            return False

        for row, col in self.current_path:

            for obstacle in self.obstacles:

                obstacle_row = int(

                    obstacle.y //

                    self.cell_size

                )

                obstacle_col = int(

                    obstacle.x //

                    self.cell_size

                )

                if (

                    abs(row - obstacle_row) <= 1

                    and

                    abs(col - obstacle_col) <= 1

                ):

                    return False

        return True

    # -------------------------------------------------

    def compute_new_path(self):

        start = self.get_robot_cell()

        path = self.planner.compute(

            start=start,

            goal=self.goal,

            obstacles=self.obstacles,

            predictions=self.predictions,

            cell_size=self.cell_size

        )

        if path:

            self.current_path = path

            self.controller.set_path(path)

            self.need_replan = False

    # -------------------------------------------------

    def step(

        self,

        dt,

        goal

    ):

        self.goal = goal

        # ---------------------------------

        # Sensor update

        self.update_sensors()

        # ---------------------------------

        # Obstacle prediction

        self.update_predictions()

        # ---------------------------------

        # Safety monitoring

        if self.safety.collision_risk():

            self.need_replan = True

        # ---------------------------------

        # Validate path

        if not self.path_is_valid():

            self.need_replan = True

        # ---------------------------------

        # Controller stuck

        if self.controller.is_stuck():

            self.need_replan = True

        # ---------------------------------

        # Timed replanning

        self.replan_timer += dt

        if (

            self.need_replan

            and

            self.replan_timer >= self.replan_interval

        ):

            self.compute_new_path()

            self.replan_timer = 0.0

        # ---------------------------------

        # Motion update

        self.controller.update(

            dt,

            self.predictions

        )