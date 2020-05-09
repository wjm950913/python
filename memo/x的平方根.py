def mySqrt(x):
    left, right = 0, x
    while left <= right:
        mid = left + (right - left) // 2
        mid_square = mid ** 2
        if mid_square == x:
            return mid
        elif mid_square > x:
            right = mid - 1
        else:
            left = mid + 1
    return min(left, right)


print(mySqrt(3))
