def Farey(n: int) -> None:
    print("Suite de Farey d'indice : ", n)
    print("0/1 ", end="")
    a, b = 0, 1
    c, d = 1, n
    while c < n:
        z = (n + b) // d
        e = z * c - a
        f = z * d - b
        a = c
        c = e
        b = d
        d = f
        print(f"{a}/{b} ", end="")

Farey(7)
