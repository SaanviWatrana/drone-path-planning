import pygame
import math

from drone import Drone
from obstacle import Obstacle
from controller import Controller
from lidar import Lidar
from perception import Perception
from slam import SLAMMap
from safety_node import SafetyNode
from planner_node import PlannerNode
from robot_core import RobotCore
from astar import astar
from costmap import CostMap
from obstacle_predictor import ObstaclePredictor

pygame.init()

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 1200,750
CELL_SIZE = 10

ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Robotics Stack")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
WHITE = (245, 245, 245)
GRAY = (200, 200, 200)
BLUE = (0, 120, 255)
GREEN = (0, 200, 0)
RED = (220, 50, 50)
YELLOW = (255, 220, 0)
PURPLE = (160, 80, 255)

# ---------------- DRONE ----------------
drone = Drone(40, 40, CELL_SIZE)

# ---------------- OBSTACLES ----------------
obstacles = [
    Obstacle(240, 200, CELL_SIZE),
    Obstacle(280, 200, CELL_SIZE),
    Obstacle(320, 200, CELL_SIZE),
    Obstacle(240, 200, CELL_SIZE),
    Obstacle(280, 200, CELL_SIZE),
    Obstacle(320, 200, CELL_SIZE),
    Obstacle(240, 200, CELL_SIZE),
    Obstacle(280, 200, CELL_SIZE),
    Obstacle(320, 200, CELL_SIZE),
    Obstacle(240, 200, CELL_SIZE),
    Obstacle(280, 200, CELL_SIZE),
    Obstacle(320, 200, CELL_SIZE),
    Obstacle(240, 200, CELL_SIZE),
    Obstacle(280, 200, CELL_SIZE),
    Obstacle(320, 200, CELL_SIZE),
    Obstacle(240, 200, CELL_SIZE),
    Obstacle(320, 200, CELL_SIZE),
    Obstacle(240, 200, CELL_SIZE),
    Obstacle(280, 200, CELL_SIZE),
    Obstacle(320, 200, CELL_SIZE),
    Obstacle(240, 200, CELL_SIZE)

]


# ---------------- GRID ----------------
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# static obstacle cells
grid[5][6] = 1
grid[5][7] = 1
grid[5][8] = 1

# ---------------- MODULES ----------------
perception = Perception(ROWS, COLS)
slam = SLAMMap(ROWS, COLS)
lidar = Lidar(obstacles)
predictor = ObstaclePredictor()

costmap = CostMap(ROWS, COLS)
planner = PlannerNode(costmap)

safety = SafetyNode(drone, obstacles, WIDTH, HEIGHT)
controller = Controller(drone, obstacles)

core = RobotCore(
    perception,
    planner,
    controller,
    safety,
    slam,
    lidar,
    predictor,
    drone,
    obstacles,
    CELL_SIZE
)

goal = (65, 100)
running = True

while running:

    dt = clock.tick(60) / 1000.0

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move obstacles
    for o in obstacles:
        o.update(dt, WIDTH, HEIGHT)

    # ---------------- CORE UPDATE ----------------
    core.step(dt, goal)

    # ---------------- GET DATA ----------------
    path = core.current_path
    predictions = core.predictions

    # ---------------- DRAW ----------------
    screen.fill(WHITE)

    # Grid
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # Path
    for r, c in path:
        pygame.draw.rect(
            screen,
            YELLOW,
            (c * CELL_SIZE + 5, r * CELL_SIZE + 5,
             CELL_SIZE - 10, CELL_SIZE - 10)
        )

    # Predicted obstacles
    for obs in predictions:
        for x, y, size in obs:
            pygame.draw.circle(screen, PURPLE, (int(x), int(y)), 4)

    # Obstacles
    for o in obstacles:
        o.draw(screen)

    # Start
    pygame.draw.circle(screen, GREEN, (40, 40), 8)

    # Goal
    gx = goal[1] * CELL_SIZE + CELL_SIZE // 2
    gy = goal[0] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, RED, (gx, gy), 10)

    # Drone
    pygame.draw.circle(screen, BLUE, (int(drone.x), int(drone.y)), 10)
        # ---------------- DEBUG ----------------
    font = pygame.font.SysFont("Arial", 18)

    status = safety.status()
    txt1 = font.render(f"Status: {status}", True, (0, 0, 0))
    txt2 = font.render(f"Path Length: {len(path)}", True, (0, 0, 0))
    txt3 = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 0, 0))

    screen.blit(txt1, (10, 10))
    screen.blit(txt2, (10, 30))
    screen.blit(txt3, (10, 50))

    pygame.display.flip()

pygame.quit()