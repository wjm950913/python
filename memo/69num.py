def maximum69Number(num: int) -> int:
    return int(str(num).replace('6', '9', 1))

print(maximum69Number(9966))
