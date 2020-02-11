import re

print("calc")
print("type 'quit' to exit")

prev = 0
run = True


def Perfom_math():
    global run
    global prev
    equation = ""
    if prev == 0:

        equation = input("type equation")
    else:
        equation = input(str(prev))

    if equation == "quit":
        print("goodbye")
        run = False
    else:
        equation = re.sub('[a-zA-Z,;:" "]', " ", equation)
        if prev == 0:
            prev = eval(equation)
        else:
            prev = eval(str(prev) + equation)


while run:
    Perfom_math()
