import time
import random

# ---------- Bubble Sort ----------
# Time Complexity:
# Beat Case     : o(n)
# Average Case  : o(n^2)
# Worst Case    : o(n^2)
# space Complexity:
# o(1)
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# ---------- Selection Sort ----------
# Time Complexity:
# Beat Case     : o(n^2)
# Average Case  : o(n^2)
# Worst Case    : o(n^2)
# space Complexity:
# o(1)
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


# ---------- Insertion Sort ----------
# Time Complexity:
# Beat Case     : o(n)
# Average Case  : o(n^2)
# Worst Case    : o(n^2)
# space Complexity:
# o(1)
def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# ---------- Merge Sort ----------
# Time Complexity:
# Beat Case     : o(n log n)
# Average Case  : o(n log n)
# Worst Case    : o(n log n)
# space Complexity:
# o(n)
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------- Quick Sort ----------
# Time Complexity:
# Beat Case     : o(n log n)
# Average Case  : o(n log n)
# Worst Case    : o(n^2)
# space Complexity:
# o(log n) (Recursion Stack)
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


# ================== Display Function ==================
def print_array(arr):
    print("\nSorted Array:")
    print(*arr)


# ======================= Main =======================
def main():
    n = int(input("Enter number of elements: "))

    arr = list(map(int, input("Enter elements:\n").split()))

    print("\nSorting Algorithms")
    print("1. Bubble Sort")
    print("2. Selection Sort")
    print("3. Insertion Sort")
    print("4. Merge Sort")
    print("5. Quick Sort")

    choice = int(input("\nEnter your choice: "))

    if choice == 1:
        bubble_sort(arr)

    elif choice == 2:
        selection_sort(arr)

    elif choice == 3:
        insertion_sort(arr)

    elif choice == 4:
        merge_sort(arr, 0, n - 1)

    elif choice == 5:
        quick_sort(arr, 0, n - 1)

    else:
        print("Invalid Choice")
        return

    print_array(arr)


if __name__ == "__main__":
    main()