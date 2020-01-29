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

#immutable data structures
import collections
Scientistes=collections.namedtuple('Scientists', [
        'name', 
        'field', 
        'born', 
        'nobel',])


