# Floyd-Warshall Algorithm

# Time Complexity:
# Best Case    : O(V^3)
# Average Case : O(V^3)
# Worst Case   : O(V^3)
# Space Complexity:
# O(V^2)

# Where:
# V = Number of Vertices

# Note:
# Finds the shortest paths between all pairs
# of vertices in a weighted graph.
INF = float('inf')

def floyd_warshall(graph):
    n = len(graph)
    dist = [row[:] for row in graph]  # copy the graph

    for k in range(n):          # intermediate node
        for i in range(n):      # start node
            for j in range(n):  # end node
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


# Example graph (adjacency matrix)
# INF means no direct edge
graph = [
    [0,   3,   INF, 7],
    [8,   0,   2,   INF],
    [5,   INF, 0,   1],
    [2,   INF, INF, 0]
]

result = floyd_warshall(graph)

print("Shortest distances between every pair of nodes:")
for row in result:
    print(row)