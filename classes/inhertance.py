class person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print("{} is {}".format(self.name, self.age))


class baby(person):
    def __init__(self, food):
        self.food = food
        print(f"baby eats {food}")


mike = baby("banana")
mike.speak()
