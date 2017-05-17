#!/usr/bin/env python

import time

def bench_len_vs_try():
    arr_len = 10000
    tries = 1000000
    t = [x for x in range(0, arr_len)]

    # Python 3.6.1: faster than try/except fail
    t1 = time.time()
    for i in range(0, tries):
      a = len(t)
    print(time.time() - t1)

    # Python 3.6.1: faster than len()
    t1 = time.time()
    for i in range(0, tries):
      try:
          a = t[arr_len]
      except IndexError:
          pass
    print(time.time() - t1)

    # Python 3.6.1: slowest
    t1 = time.time()
    for i in range(0, tries):
      try:
          a = t[arr_len]
      except IndexError:
          pass
    print(time.time() - t1)
