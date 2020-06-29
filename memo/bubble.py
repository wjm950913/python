def bubble(arr):
    arrlength = len(arr)
    for j in range(arrlength - 1, 0, -1):
        for i in range(j):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return arr


if __name__ == '__main__':
    arr = [3, 45, 7, 8, 934, 3]
    res = bubble(arr)
    print(res)
