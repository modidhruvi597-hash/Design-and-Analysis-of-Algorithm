# Searching.py
import time

# Linear Search
# Time Complexity
# Best Case     : o(!)
# Average Case  : o(n)
# Worst Case    : o(n)
# Space Complexity
# o(1)
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i  # index found
    return -1  # not found

# Binary Search (array must be sorted in ascending order)
# Time Complexity
# Best Case    : o(1)
# Average Case : o(log n)
# Worst Case   : o(log n)
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1  # not found


# ---------- Main ----------
def main():
    n = int(input("Enter number of elements: "))

    arr = list(map(int, input("Enter elements:\n").split()))

    key = int(input("Enter element to search: "))

    print("\nSearch Algorithms")
    print("1. Linear Search")
    print("2. Binary Search")

    choice = int(input("\nEnter your choice: "))

    if choice == 1:
        pos = linear_search(arr, key)

    elif choice == 2:
        pos = binary_search(arr, key)

    else:
        print("Invalid Choice")
        return

    if pos == -1:
        print("\nElement Not Found.")
    else:
        print(f"\nElement Found at Position {pos + 1}")


if __name__ == "__main__":
    main()