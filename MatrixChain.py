# MatrixChain.py
def matrix_chain_order(p):
    # p is the array of dimensions where matrix i has dimensions p[i-1] x p[i]
    n = len(p) - 1   # number of matrices

    # dp[i][j] = minimum number of multiplications to multiply matrices i to j
    dp = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    # s[i][j] = index at which we split the chain for optimal cost (used to print order)
    s = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    # chain_length is the number of matrices being multiplied together
    for chain_length in range(2, n + 1):
        for i in range(1, n - chain_length + 2):
            j = i + chain_length - 1
            dp[i][j] = float('inf')

            # try every possible split point k
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + p[i - 1] * p[k] * p[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    s[i][j] = k   # store the split point

    return dp[1][n], s


# ======================= Main =======================
def main():
    n = int(input("Enter number of matrices: "))
    p = list(map(int, input(f"Enter {n + 1} dimensions:\n").split()))

    min_cost, s = matrix_chain_order(p)   # unpack the tuple
    print("\nMinimum Multiplications =", min_cost)

if __name__ == "__main__":
    main()
