# Factorial.py
import time

# Iterative Method
# Time Complexity
# Best Case    : o(n)
# Average Case : o(n)
# Worst Case   : o(n)
# Space Complexity
# o(1)
def iterative_factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Recursive Method
# Time Complexity:
# Best Case    : O(n)
# Average Case : O(n)
# Worst Case   : O(n)
# Space Complexity:
# O(n)
def recursive_factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * recursive_factorial(n - 1)


# ======================= Main =======================
def main():
    n = int(input("Enter a number: "))

    print("\nFactorial Methods")
    print("1. Iterative Method")
    print("2. Recursive Method")

    choice = int(input("\nEnter your choice: "))

    if choice == 1:
        ans = iterative_factorial(n)
        print(f"\nFactorial = {ans}")

    elif choice == 2:
        ans = recursive_factorial(n)
        print(f"\nFactorial = {ans}")

    else:
        print("Invalid Choice")


if __name__ == "__main__":
    main()