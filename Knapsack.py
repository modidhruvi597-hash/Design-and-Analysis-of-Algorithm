# Knapsack.py
# 0/1 Knapsack using Dynamic Programming
# Time Complexity:
# Best Case    : O(n * W)
# Average Case : O(n * W)
# Worst Case   : O(n * W)
# Space Complexity:
# O(n * W)
# Where:
# n = Number of items
# W = Maximum capacity of knapsack
def knapsack(weights, values, capacity, n):
    # Create a 2D DP table with (n+1) rows and (capacity+1) columns
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(0, capacity + 1):
            if weights[i - 1] <= w:
                 dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]],
                                dp[i - 1][w])
            else:
                # Item can't fit, so exclude it
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity], dp

# ======================= Main =======================
def main():
    n = int(input("Enter number of items: "))

    wt = list(map(int, input("Enter weights:\n").split()))
    val = list(map(int, input("Enter values:\n").split()))

    W = int(input("Enter knapsack capacity: "))

    print("\nMaximum Profit =", knapsack(wt, val, n, W))


if __name__ == "__main__":
    main()