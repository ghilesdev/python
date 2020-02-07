from .decorators import *

#from decorators_folder.decorators import *


@do_twice
def say_hello(name):
    print(f'hello {name}')

@timer
def waste_time(num):
    for _ in range(num):
        sum([i**2 for i in range(1000)])



@debug
def make_greeting(name, age=None):
    if age ==  None:
        return f'Howdy {name}'
    else:
        return f"whoa {name}, {age} already, you're growing up"


@slow_down
def countdown(num):
    if num<1:
        print('lift off!')
    else:
        print(num)
        countdown(num-1)

countdown(5)
