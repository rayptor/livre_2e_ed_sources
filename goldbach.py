def premier(n: int) -> bool:
    return n >= 3 and all(n % i for i in range(2, int(n**0.5) + 1))

def goldbach(n: int) -> tuple[int, int]:
    return next((i, n - i) for i in range(2, n // 2 + 1) if premier(i) and premier(n - i))

print(goldbach(1789736254084))
