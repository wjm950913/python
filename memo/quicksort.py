def quicksort(arr):
    arrlength = len(arr)
    if arrlength < 2:
        return arr
    mid = arr[arrlength // 2]
    arr.remove(mid)
    left, right = [], []
    for i in arr:
        if i < mid:
            left.append(i)
        else:
            right.append(i)
    return quicksort(left) + [mid] + quicksort(right)


if __name__ == '__main__':
    arr = [3, 45, 7, 8, 934, 3]
    res = quicksort(arr)
    print(res)
