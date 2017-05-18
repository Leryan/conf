#!/usr/bin/env python

# wget https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.10.7.tar.xz
# tar xf linux-4.10.7.tar.xz
# find linux-4.10.7 -type f > flist
# python charcount.py -cms # or only -cm to get counters

import argparse
import encodings
import json
import operator
import os
import sys
import time

from queue import Empty as EmptyQueue
from multiprocessing import Pool, Manager, Queue, Process

def get_encs():
    encs = ['utf-8', 'ascii']
    return encs

ENCS = get_encs()
BLANK_CHARS = ["\n", "\t", "\r", " ", " "] # last is unbreakable space

def count_chars(chars):
    char_count = {}
    tuple_count = {}
    prev_char = None

    for char in chars:
        char = char.lower()
        if char in BLANK_CHARS:
            prev_char = None
            next

        if char == ' ':
            prev_char = None
            next

        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

        if prev_char is not None and char not in BLANK_CHARS:
            char_tuple = f'{prev_char}{char}'

            if char_tuple in tuple_count:
                tuple_count[char_tuple] += 1
            else:
                tuple_count[char_tuple] = 1

            prev_char = char

        elif prev_char is None and char not in BLANK_CHARS:
            prev_char = char

        else:
            prev_char = None

    return char_count, tuple_count

def merge_char_count(left, right):
    merged = {}
    chars = list(left.keys())
    chars.extend(list(right.keys()))

    chars = list(set(chars))

    for k in chars:
        if k in right and k in left:
            merged[k] = left[k] + right[k]
        elif k in right:
            merged[k] = right[k]
        elif k in left:
            merged[k] = left[k]

    return merged

def sort_res(ffile):
    with open(ffile, 'r') as fjres:
        res = json.loads(fjres.read())

    list_sorted = sorted(res.items(), key=operator.itemgetter(1))

    for sl in list_sorted:
        print('{}: {}'.format(sl[0], sl[1]))

def count_file_chars(queue, resultsq):
    print(f'Worker {os.getpid()} started')
    try:
        while not queue.empty():
            ffile = queue.get_nowait()
            char_count = {}
            tuple_count = {}
            for enc in ENCS:
                with open(ffile, 'r', encoding=enc) as fhffile:
                    try:
                        file_content = fhffile.read()
                        count_result = count_chars(file_content)
                        char_count = merge_char_count(char_count, count_result[0])
                        tuple_count = merge_char_count(tuple_count, count_result[1])

                        resultsq.put_nowait([char_count, tuple_count, []])

                        break

                    except ValueError as ex:
                        pass
    except EmptyQueue:
        pass

    print(f'Worker {os.getpid()} finished')

def process_results(queue, resultsq):
    cc = {}
    tc = {}
    failed_files = []

    print(f'Worker {os.getpid()} started')

    try:
        while not queue.empty():
            results = queue.get_nowait()

            for r in results:
                cr = r[0]
                tr = r[1]
                failed_files.extend(r[2])

                cc = merge_char_count(cc, cr)
                tc = merge_char_count(tc, tr)
    except EmptyQueue:
        pass

    resultsq.put_nowait((cc, tc, failed_files))

    print(f'Worker {os.getpid()} finished')

def variable_amount(l, n):
    """
    Return a list of n lists of unkwown size.
    """
    lf = []
    s = int(len(l) / n)

    for i in range(0, n * s, s):
        lf.append(l[i:i+s])

    if n * s < len(l):
        for i in range(n * s, len(l)):
            j = i % n
            lf[j].append(l[i])

    return lf

def fixed_amount(l, n):
    """
    Return a list of:
        unknown amount of:
            lists of n elements.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

def start_wait(plist):
    for p in plist:
        p.start()

    for p in plist:
        p.join()

def do_count(args):
    manager = Manager()
    queue = manager.Queue()
    results = manager.Queue()
    processes = []

    with open(args.flist, 'r') as fhflist:
        flist = map(str.strip, fhflist.readlines())
        flist = [f for f in flist if f[0] != '#']

    for f in flist:
        queue.put(f)

    for i in range(0, args.workers):
        processes.append(Process(target=count_file_chars, args=(queue, results)))

    t_count_start = time.time()
    start_wait(processes)
    t_count = time.time() - t_count_start

    try:
        res = []
        while not results.empty():
            res.append(results.get())
    except EmptyQueue:
        pass

    with open(f'{args.flist}.merge.json', 'w') as f:
        f.write(json.dumps(res))

    return t_count

def do_merge(args):
    with open(f'{args.flist}.merge.json', 'r') as f:
            print('loading counters...')
            res = json.loads(f.read())

    manager = Manager()
    queue = manager.Queue()
    results = manager.Queue()
    processes = []

    for i in range(0, len(res), args.batch_len):
        batch = res[i:i+args.batch_len]
        queue.put_nowait(batch)

    for i in range(0, args.workers):
        processes.append(Process(target=process_results, args=(queue, results)))

    t_merge_start = time.time()
    start_wait(processes)
    try:
        res = []
        while not results.empty():
            res.append(results.get())
    except EmptyQueue:
        pass

    cc = {}
    tc = {}
    failed_files = []

    for r in res:
        cc = merge_char_count(cc, r[0])
        tc = merge_char_count(tc, r[1])
        failed_files.extend(r[2])

    return cc, tc, failed_files, time.time() - t_merge_start

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', action='store_true')
    parser.add_argument('-m', '--merge', action='store_true')
    parser.add_argument('-s', '--sort', action='store_true')
    parser.add_argument('-w', '--workers', default=os.cpu_count(), help='number of workers', type=int)
    parser.add_argument('-b', '--batch-len', default=100, type=int)
    parser.add_argument('-f', '--flist', default='flist')

    args = parser.parse_args()

    if args.count:
        optime = do_count(args)

        print(f'count time: {optime}')

    if args.merge:
        cc, tc, failed_files, optime = do_merge(args)

        with open(f'{args.flist}.char.json', 'w') as fc:
            fc.write(json.dumps(cc))

        with open(f'{args.flist}.tuple.json', 'w') as ft:
            ft.write(json.dumps(tc))

        with open(f'{args.flist}.failed', 'w') as ff:
            for failed_file in failed_files:
                ff.write(f"{failed_file}\n")

        print(f'merge time: {optime}')

    if args.sort:
        sort_res(f'{args.flist}.char.json')
        sort_res(f'{args.flist}.tuple.json')

if __name__ == '__main__':
    main()
