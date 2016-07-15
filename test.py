def triangle():
    a = [1]
    while True:
        yield a
        a = [sum(i) for i in zip([0]+a, a+[0])]

n = 0
for t in triangle():
    print(t)
    n += 1
    if n == 10:
        break