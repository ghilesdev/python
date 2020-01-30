
import multiprocessing
import time
import os




def transform(x):
    time.sleep(1)
    print(f'\nprocessing {os.getpid()} record {x["name"]}')
    result = {'name': x["name"], 'age': 2020 - x["born"]}
    print(f'\ndone processing {os.getpid()} record {x["name"]}')
    return result



if __name__ == '__main__':
    multiprocessing.freeze_support()
    import collections
    import time
    from pprint import pprint


    # import pprint to print more readable
    Scientists = collections.namedtuple('Scientists', [
        'name',
        'field',
        'born',
        'nobel', ])

    # making a tuple, tuple is an immutable data type
    scientists = (
        Scientists(name='ada lovelace', field='math', born=1885, nobel=False),
        Scientists(name='marie curie', field='physics', born=1867, nobel=True),
        Scientists(name='Vera rubin', field='astronomy', born=1928, nobel=True),
        Scientists(name='Tu youyou', field='chemistry', born=1930, nobel=True)
    )

    scientists = [
        {"name" : 'ada lovelace', "field" : 'math', "born"  : 1885, "nobel" : False},
        {"name": 'marie', "field": 'physics', "born": 1867, "nobel": True},
        {"name": 'Vera rubin', "field": 'astronomy', "born": 1928, "nobel": True},
        {"name": 'aTu youyou', "field": 'chemistry', "born": 1930, "nobel": True}

    ]

    pprint(scientists)
    start = time.time()

    # initiating multiprocessing object
    pool = multiprocessing.Pool(4)
    names_and_ages = pool.map(transform, scientists)
    end = time.time()

    print(f'time to complete: {end - start:.2f} secs')
    pprint(names_and_ages)
