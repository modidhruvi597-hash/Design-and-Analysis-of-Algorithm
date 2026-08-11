# Knapsack.py
# Time Complexity:
# Best Case    : o(n * w)
# Average Case : o(n * w)
# Worst Case   : o(n * w)
# Space Complexity:
# o(n * w)
#
# Where:
# n = Number of items
# W = Maximum capacity of knapsack
def knapsack(weights, values, capacity):
    n = len(weights)
    # dp[i][w] = max value using first i items with capacity w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]],
                                dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


# ---- Main Program ----
values = [60, 100, 120]     
weights = [10, 20, 30]      
capacity = 50               

result = knapsack(weights, values, capacity)
print(f"Maximum value that can be obtained: {result}")