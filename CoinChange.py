# Coin Change (Making change) using Dynamic Programming
# Time Complexity:
# Best Case    : o(n * Amount)
# Average Case : o(n * Amount)
# Worst Case   : o(n * Amount)
# Space Complexity
# o(Amount)
def making_change(coins, amount):
    # dp[i] will store minimum coins needed for amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  

    # Fill the dp table
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    if dp[amount] == float('inf'):
        return -1  
    else:
        return dp[amount]


# ---- Main Program ----
coins = [1, 2, 5]     # available coin denominations
amount = 11            # amount to make

result = making_change(coins, amount)

if result != -1:
    print(f"Minimum coins needed to make {amount}: {result}")
else:
    print(f"Cannot make {amount} with given coins")