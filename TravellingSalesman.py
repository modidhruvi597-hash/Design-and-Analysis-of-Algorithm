# Travelling Salesman Problem (TSP)

# Time Complexity:
# Best Case    : O(n!)
# Average Case : O(n!)
# Worst Case   : O(n!)
# Space Complexity:
# O(n)

# Where:
# n = Number of Cities

# Note:
# Uses Backtracking to find the minimum cost
# Hamiltonian Cycle.

from itertools import permutations

def tsp(dist):
    n = len(dist)
    cities = range(1, n)  # start from city 0

    best_cost = float('inf')
    best_path = None

    for order in permutations(cities):
        path = [0] + list(order) + [0]  # start and end at city 0
        cost = 0
        for i in range(len(path) - 1):
            cost += dist[path[i]][path[i + 1]]

        if cost < best_cost:
            best_cost = cost
            best_path = path

    return best_cost, best_path


# Distance matrix (dist[i][j] = distance from city i to city j)
dist = [
    [0,  10, 15, 20],
    [10, 0,  35, 25],
    [15, 35, 0,  30],
    [20, 25, 30, 0]
]

cost, path = tsp(dist)
print("Shortest route:", path)
print("Total distance:", cost)