import heapq
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


## Calculating euclidean distance from node to goal
def heuristic(node, goal):

    x1, y1, z1 = node
    x2, y2, z2 = goal

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2 +
        (z2 - z1) ** 2
    )


## for getting all neighbors of any node
def get_neighbors(node, grid_size):

    x, y, z = node

    directions = [
        (1, 0, 0),
        (-1, 0, 0),

        (0, 1, 0),
        (0, -1, 0),

        (0, 0, 1),
        (0, 0, -1),

        (0, 0, 0)      # WAIT
    ]

    neighbors = []

    for dx, dy, dz in directions:

        nx = x + dx
        ny = y + dy
        nz = z + dz

        if (
            0 <= nx < grid_size and
            0 <= ny < grid_size and
            0 <= nz < grid_size
        ):

            neighbors.append(
                (nx, ny, nz)
            )

    return neighbors

## Final path
def reconstruct_path(parent, current):

    path = [current]

    while current in parent:

        current = parent[current]
        path.append(current)

    path.reverse()

    return path

## Random weight assigned to some nodes
weights = {
    (39, 49, 19): 15,
    (26, 17, 30): 10,
    (19, 21, 15): 20,
    (10, 47, 33): 12,
    (26, 32, 22): 18,
    (42, 21, 32): 25,
    (12, 32, 24): 10,
    (33, 20, 32): 14,
    (46, 40, 20): 30,
    (10, 29, 15): 16
}


## A* algorithm for finding shortest distance between start adn goal also considering reserved and most weighted point
def astar(
        start,
        goal,
        grid_size,
        reserved=None,
        vel=1
):

    if reserved is None:
        reserved = set()

    dt = 1 / vel

    open_set = []

    heapq.heappush(
        open_set,
        (0, start, 0)
    )

    parent = {}

    g_score = {
        start: 0
    }

    f_score = {
        start:
        heuristic(start, goal)
    }

    while open_set:

        current_f, current, current_time = \
            heapq.heappop(open_set)

        if current == goal:

            return reconstruct_path(
                parent,
                current
            )

        for neighbor in get_neighbors(
                current,
                grid_size
        ):

            next_time = (
                current_time + dt
            )

            if (
                (neighbor, next_time)
                in reserved
            ):
                continue

            movement_cost = 1

            weight_cost = (
                weights.get(
                    neighbor,
                    0
                )
            )

            tentative_g = (
                    g_score[current]
                    + movement_cost
                    + weight_cost
            )

            if (
                    neighbor not in g_score
                    or
                    tentative_g <
                    g_score[neighbor]
            ):

                parent[neighbor] = current

                g_score[neighbor] = \
                    tentative_g

                f = (
                        tentative_g
                        +
                        heuristic(
                            neighbor,
                            goal
                        )
                )

                f_score[neighbor] = f

                heapq.heappush(
                    open_set,
                    (
                        f,
                        neighbor,
                        next_time
                    )
                )

    return None

## Reservation table function
def reserve_path(
        path,
        reserved,
        vel=1
):

    dt = 1 / vel

    time = 0

    for node in path:

        reserved.add(
            (node, time)
        )

        time += dt


## Agent 1
reserved = set()

path1 = astar(
    start=(0, 0, 0),
    goal=(98, 91, 20),
    grid_size=100,
    reserved=reserved,
    vel=1
)

reserve_path(
    path1,
    reserved,
    vel=1
)


## Agent 2
path2 = astar(
    start=(5, 5, 5),
    goal=(10, 99, 99),
    grid_size=100,
    reserved=reserved,
    vel=1
)

reserve_path(
    path2,
    reserved,
    vel=1
)


## Agent 3
path3 = astar(
    start=(1, 5, 8),
    goal=(95, 15, 90),
    grid_size=100,
    reserved=reserved,
    vel=1
)

reserve_path(
    path3,
    reserved,
    vel=1
)


## Printing all results
print("Agent 1 Path")
print(path1)

print()

print("Agent 2 Path")
print(path2)

print()

print("Agent 3 Path")
print(path3)

print("======================")
print(reserved)



## 3D Visualization
## creating figure
fig = plt.figure(figsize=(10, 10))

ax = fig.add_subplot(
    111, projection='3d'
)

## Firt plot weighted nodes
wx = []
wy = []
wz = []

for node in weights:

    x, y, z = node

    wx.append(x)
    wy.append(y)
    wz.append(z)

ax.scatter(
    wx,
    wy,
    wz,
    c='black',
    s=100,
    marker='s',
    label='Weighted Nodes'
)


## Function to plot a path
def plot_path(
        path,
        color,
        label
):

    x = []
    y = []
    z = []

    for node in path:

        xi, yi, zi = node

        x.append(xi)
        y.append(yi)
        z.append(zi)

    ax.plot(
        x,
        y,
        z,
        color=color,
        linewidth=3,
        label=label
    )

    ax.scatter(
        x[0],
        y[0],
        z[0],
        color=color,
        marker='o',
        s=100
    )

    ax.scatter(
        x[-1],
        y[-1],
        z[-1],
        color=color,
        marker='*',
        s=200
    )

plot_path(
    path1,
    'red',
    'Agent 1'
)

plot_path(
    path2,
    'blue',
    'Agent 2'
)

plot_path(
    path3,
    'green',
    'Agent 3'
)

## Labelling
ax.set_xlabel('X')

ax.set_ylabel('Y')

ax.set_zlabel('Z')

ax.set_title(
    '3D Multi-Agent Path Planning'
)

ax.legend()

plt.show()

