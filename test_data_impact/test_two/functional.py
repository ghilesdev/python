def calculate(params):
    sum = 0
    if len(params) > 1:
        for i in params:
            if type(i) == str:
                if len(i) < 2:
                    if ord(i) > 47 & ord(i) < 58:
                        sum += int(i)
    return sum


sum = calculate([585, "9", "1", "2", "hello"])
print(sum)
