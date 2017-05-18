#!/usr/bin/env python

"""
import microbench
microbench.bench_
"""

import time


def bench_len_vs_try():
    """
    Test if array contains at least one element.
    """
    arr_len = 10000
    tries = 1000000
    t = [x for x in range(0, arr_len)]

    t1 = time.time()
    for i in range(0, tries):
        a = len(t)
    print('len(): {}'.format(time.time() - t1))

    t1 = time.time()
    for i in range(0, tries):
        try:
            a = t[0]
        except IndexError:
            pass
    print('try -> no exception: {}'.format(time.time() - t1))

    t1 = time.time()
    for i in range(0, tries):
        try:
            a = t[arr_len]
        except IndexError:
            pass
    print('try -> exception: {}'.format(time.time() - t1))


def main():
    bench_len_vs_try()

if __name__ == '__main__':
    main()
