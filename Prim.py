# Prim's Algorithm - Very Simple Version
# Prim's Algorithm (Minimum Spanning Tree)

# Time Complexity:
# Best Case    : O(V^2)
# Average Case : O(V^2)
# Worst Case   : O(V^2)

# Space Complexity:
# O(V)


# Note:
# Finds the Minimum Spanning Tree (MST) of a
# connected weighted graph.
# =========================================================

n = int(input("Enter number of vertices: "))

print("Enter Cost Adjacency Matrix:")
cost = []
for i in range(n):
    row = list(map(int, input().split()))
    cost.append(row)

visited = [0] * n
visited[0] = 1     # start from vertex 0
total = 0

print("Edges in Minimum Spanning Tree:")

for k in range(n - 1):
    min = 9999
    x = 0
    y = 0

    for i in range(n):
        for j in range(n):
            if visited[i] == 1 and visited[j] == 0 and cost[i][j] != 0:
                if cost[i][j] < min:
                    min = cost[i][j]
                    x = i
                    y = j

    print(x, "-->", y, " Cost =", min)
    visited[y] = 1
    total = total + min

print("Minimum Cost =", total)