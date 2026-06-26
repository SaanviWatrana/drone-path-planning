import math


class ObstaclePredictor:

    def __init__(self,
                 prediction_time=1.5,
                 prediction_steps=5):

        # seconds into future
        self.prediction_time = prediction_time

        # number of future samples
        self.prediction_steps = prediction_steps

    # -------------------------------------------------

    def predict(self, obstacles):

        predicted_obstacles = []

        dt = self.prediction_time / self.prediction_steps

        for obstacle in obstacles:

            future_positions = []

            future_x = obstacle.x
            future_y = obstacle.y

            vx = obstacle.vx
            vy = obstacle.vy

            for _ in range(self.prediction_steps):

                future_x += vx * dt
                future_y += vy * dt

                future_positions.append(

                    (
                        future_x,
                        future_y,
                        obstacle.size
                    )

                )

            predicted_obstacles.append(future_positions)

        return predicted_obstacles

    # -------------------------------------------------

    def nearest_prediction(self,
                           drone_x,
                           drone_y,
                           predictions):

        minimum_distance = float("inf")

        nearest = None

        for obstacle in predictions:

            for x, y, size in obstacle:

                distance = math.hypot(

                    drone_x - x,

                    drone_y - y

                )

                if distance < minimum_distance:

                    minimum_distance = distance

                    nearest = (x, y, size)

        return nearest, minimum_distance