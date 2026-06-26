def line_of_sight(grid, p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    steps = max(abs(x2 - x1), abs(y2 - y1))

    if steps == 0:
        return True

    for i in range(steps + 1):
        t = i / steps

        x = int(x1 + (x2 - x1) * t)
        y = int(y1 + (y2 - y1) * t)

        if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
            return False

        if grid[y][x] == 1:
            return False

    return True


def smooth_path(grid, path):
    if not path:
        return []

    # ❗ DO NOT over-smooth small paths
    if len(path) < 5:
        return path

    new_path = [path[0]]
    i = 0

    while i < len(path) - 1:

        j = len(path) - 1

        # ensure at least 1 intermediate node is preserved
        while j > i + 2:
            if line_of_sight(grid, path[i], path[j]):
                break
            j -= 1

        new_path.append(path[j])
        i = j

    return new_path