# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 11:39:48 2020

@author: WebDev
"""

'''
#this is a mutable data structure, means, can be changed
scientist=[{'name':'ada lovelace', 'field':'math', 'born':1815, 'nobel': False},
           {'name':'emmy noether', 'field':'math', 'born':1882, 'nobel': False}
           ]
'''

# immutable data structures
import collections
# import pprint to print more readable
from pprint import pprint

Scientists = collections.namedtuple('Scientists', [
    'name',
    'field',
    'born',
    'nobel', ])

ada = Scientists(name='ada lovelace', field='math', born=1885, nobel=False)

# making a tuple, tuple is an immutable data type
scientists = (
    Scientists(name='ada lovelace', field='math', born=1885, nobel=False),
    Scientists(name='marie curie', field='physics', born=1867, nobel=True),
    Scientists(name='Vera rubin', field='astronomy', born=1928, nobel=True)
)

# pprint(scientists)

# lambda func takes an x and return x when x.name is true
filtered = filter(lambda x: x.nobel is True, scientists)
print(filtered)
for f in filtered:
    pprint(f.name)

# make an immutable filtered
filterimmut = tuple(filter(lambda x: x.nobel is True, scientists))

# same thing but using list comprehension
lists = tuple([x for x in scientists if x.nobel == True])
pprint(lists)

'''
or 
lists=tuple(x for x in scientists if x.nobel == True)
'''

# map function, takes a function and applies over an iterator,
names_and_ages = tuple(map(lambda x: {'name': x.name, 'age': 2020 - x.born}, scientists))
pprint(names_and_ages)

#ANOTHER listcomprehension or 'generator'
pprint(tuple({'name':y.name, 'age':2020-y.born} for y in scientists))

#reduce func
from functools import reduce
total_age=reduce(lambda acc, val: acc + val['age'], names_and_ages, 0)
print(total_age)

import collections
def reducer(acc, val):
    acc[val.field].append(val.name)
    return acc

scientists_by_fields=reduce(reducer, scientists, collections.defaultdict(list))
pprint(scientists_by_fields)

