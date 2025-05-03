def racine_cubique(n: int) -> int:
    positionBit = 60  # Pour 64 bits
    x = 0
    while positionBit >= 0:
        x <<= 1
        b = (3 * x**2 + 3 * x + 1) << positionBit
        if n >= b:
            n -= b
            x += 1
        positionBit -= 3
    return x

# Test
print(racine_cubique(793534114958941))
