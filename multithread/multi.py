#!/usr/bin/python3

import _thread
import time

def TimeFunc(thread, delay):
    count=0
    while count<5:
        time.sleep(1)
        count+=1
        print(f'{thread}:{time.ctime(time.time())}')

try:
    _thread.start_new_thread(TimeFunc, ("thread number one", 1))
    _thread.start_new_thread(TimeFunc, ("thread number two", 2))
except:
    print('error occured\n',
          'unable to initiate thread')

while 1:
    pass