# Kruskal's Algorithm (Minimum Spanning Tree)

# Time Complexity:
# Best Case    : O(E log E)
# Average Case : O(E log E)
# Worst Case   : O(E log E)
# Space Complexity:
# O(V)

# Where:
# V = Number of Vertices
# E = Number of Edges

# Note:
# Finds the Minimum Spanning Tree (MST)
# using Greedy Approach.
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])   # path compression
    return parent[x]


def kruskal(n, edges):
    parent = list(range(n))
    mst = []
    total = 0

    # sort edges by weight
    edges.sort(key=lambda e: e[2])

    for u, v, w in edges:
        root_u = find(parent, u)
        root_v = find(parent, v)

        # add edge only if it doesn't form a cycle
        if root_u != root_v:
            parent[root_u] = root_v
            mst.append((u, v, w))
            total += w

    return mst, total


# n = number of nodes, edges = (u, v, weight)
n = 5
edges = [
    (0, 1, 2),
    (0, 3, 6),
    (1, 2, 3),
    (1, 3, 8),
    (1, 4, 5),
    (2, 4, 7),
]

mst, total = kruskal(n, edges)
print("Edges in MST:")
for u, v, w in mst:
    print(f"{u} - {v} (weight {w})")
print("Total weight:", total)