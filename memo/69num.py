"""
题意：给一个正整数，只包含9和6，仅改变其中一个数字，使其最大。
很简单，从高到低判断是否为9即可，如果是，则判断下一位，如果不是，则改成9，并返回。
"""


def maximum69Number(num: int) -> int:
    return int(str(num).replace('6', '9', 1))


print(maximum69Number(9966))
