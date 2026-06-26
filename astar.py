import heapq
import math


# ------------------------------------------------
# Euclidean Heuristic
# ------------------------------------------------

def heuristic(a, b):

    return math.sqrt(

        (a[0] - b[0]) ** 2 +

        (a[1] - b[1]) ** 2

    )


# ------------------------------------------------
# A* Planner
# grid values:
# 0      -> free
# 1/255  -> obstacle
# 2-254  -> traversal cost
# ------------------------------------------------

def astar(grid, start, goal):

    rows = len(grid)
    cols = len(grid[0])

    open_set = []

    heapq.heappush(

        open_set,

        (

            0,

            start

        )

    )

    came_from = {}

    g_score = {

        start: 0

    }

    closed = set()

    # 8-connected motion

    directions = [

        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),

        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1)

    ]

    while open_set:

        current = heapq.heappop(

            open_set

        )[1]

        if current in closed:
            continue

        closed.add(current)

        # -------------------------

        if current == goal:

            path = []

            while current in came_from:

                path.append(current)

                current = came_from[current]

            path.append(start)

            path.reverse()

            return path

        # -------------------------

        row, col = current

        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if nr < 0 or nr >= rows:
                continue

            if nc < 0 or nc >= cols:
                continue

            cell = grid[nr][nc]

            # blocked

            if cell == 1 or cell >= 220:
                continue

            neighbor = (

                nr,

                nc

            )

            # diagonal cost

            if abs(dr) + abs(dc) == 2:

                move_cost = 1.414

            else:

                move_cost = 1.0

            # inflation penalty

            obstacle_cost = cell / 255.0

            tentative_g = (

                g_score[current]

                +

                move_cost

                +

                obstacle_cost

            )

            if (

                neighbor not in g_score

                or

                tentative_g < g_score[neighbor]

            ):

                g_score[neighbor] = tentative_g

                came_from[neighbor] = current

                f_score = (

                    tentative_g

                    +

                    heuristic(

                        neighbor,

                        goal

                    )

                )

                heapq.heappush(

                    open_set,

                    (

                        f_score,

                        neighbor

                    )

                )

    return []