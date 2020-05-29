def bubble_short(arr):
    for angka in range(len(arr)-1):
        for num in range(0, len(arr)-angka-1):
            lower = arr[num]
            bigger = arr[num + 1]
            if arr[num] > arr[num + 1]:
                lower = arr[num + 1]
                bigger = arr[num]
            arr[num], arr[num + 1] = lower, bigger
    return arr

lst = [3, 1, 5, 6, 2, 4, 7, 8]