# Graph Traversal using DFS and BFS
from collections import deque

# Depth First Search (DFS)

# Time Complexity:
# Best Case    : O(V + E)
# Average Case : O(V + E)
# Worst Case   : O(V + E)

# Space Complexity:
# O(V)

# Where:
# V = Number of Vertices
# E = Number of Edges

# ---- DFS Traversal ----
def dfs(graph, visited, v, n):
    visited[v] = True
    print(v, end=" ")

    for i in range(n):
        if graph[v][i] == 1 and not visited[i]:
            dfs(graph, visited, i, n)

# Breadth First Search (BFS)

# Time Complexity:
# Best Case    : O(V + E)
# Average Case : O(V + E)
# Worst Case   : O(V + E)

# Space Complexity:
# O(V)

# ---- BFS Traversal ----
def bfs(graph, visited, start, n):
    queue = deque([start])
    visited[start] = True

    while queue:
        v = queue.popleft()
        print(v, end=" ")

        for i in range(n):
            if graph[v][i] == 1 and not visited[i]:
                visited[i] = True
                queue.append(i)


# ---- Main Program ----
n = int(input("Enter number of vertices: "))

print("Enter Adjacency Matrix:")
graph = []
for _ in range(n):
    row = list(map(int, input().split()))
    graph.append(row)

start = int(input("Enter starting vertex: "))

print("\nDFS Traversal: ", end="")
dfs(graph, [False] * n, start, n)

print("\nBFS Traversal: ", end="")
bfs(graph, [False] * n, start, n)