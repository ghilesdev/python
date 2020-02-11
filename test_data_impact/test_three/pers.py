def persistance(n):
    length = len(str(n))
    r = 1
    if length > 1:
        n = list(str(n))
        for i in range(len(n)):
            r = r * n[i]
        length = len(str(r))
        persistance(r)
    return length


print(persistance(65))
