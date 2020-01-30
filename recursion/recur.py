from functools import lru_cache

def factorial(n):
    if n==1:
        return 1
    return n*factorial(n-1)


houses = ["jack's", "tommy's", "mark's", "paul's", "james's", "chris's"]


def deliver_presents_recyrsivly(houses):
    if len(houses) == 1:
        print("deliver present to ", houses[0])
    else:
        mid=len(houses)//2
        first_half=houses[:mid]
        sec_half=houses[mid:]
        deliver_presents_recyrsivly(first_half)
        deliver_presents_recyrsivly(sec_half)

@lru_cache(maxsize= None)
def fibbionacci_rec_optimized(n):
    print('fibbonacci_rec_optimized called with', n)
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibbionacci_rec_optimized(n-1)+fibbionacci_rec_optimized(n-2)


def fibbionacci_rec(n):
    print('fibbonacci_rec_optimized called with', n)
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibbionacci_rec(n-1)+fibbionacci_rec(n-2)


