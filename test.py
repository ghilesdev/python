print("hello aghiles")
# cost=input('enter the cost')
# print("the price is :"+cost)

birthdate = "20/10/1994"
birthdate_split = birthdate.split("/")
[dd, mm, yyyy] = birthdate_split
print("day: " + dd + " month: " + mm + " year: " + yyyy)
# dictionary:
{"name": "aghiles", "age": 25, "hobby": "code"}
{"name": "aghiles", "age": 25, "hobby": "code"}["age"]
sorted([1, 5, 2])


def my_func(*people):
    for person in people:
        print("this person is ", person)


my_func("aghiles", "david", "moh")
