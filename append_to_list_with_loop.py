from random import randint
import sys


def create_data():
    l = list()
    for i in range(100000):
        l.append(randint(1, 10000000))
    return l


@profile
def proc():
    cnt = 0
    data = create_data()
    for i in range(100000):
        if randint(1, 10000000) in data:
            cnt += 1

if __name__ == '__main__':
    print(sys.argv[0])
    print(sys.version_info)
    # import timeit
    # print(timeit.timeit("proc()", setup="from __main__ import proc", number=3))
    [proc() for i in range(3)]
