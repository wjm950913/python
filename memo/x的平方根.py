"""
 计算并返回 x 的平方根，其中 x 是非负整数。
 由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。
"""


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


print(mySqrt(7))
