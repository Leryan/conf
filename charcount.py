#!/usr/bin/env python

# wget https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.10.7.tar.xz
# tar xf linux-4.10.7.tar.xz
# find linux-4.10.7 -type f > flist
# python charcount.py -c -s -w ${CPUCOUNT_OR_SOMETHING_LIKE_THAT}

import argparse
import encodings
import json
import operator
import os
import sys

from multiprocessing import Pool

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

        else:
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

def count_file_chars(ffile):
    instance = os.getpid()

    char_count = {}
    tuple_count = {}

    print(f'processing file {ffile}')
    for enc in ENCS:
        with open(ffile, 'r', encoding=enc) as fhffile:
            try:
                file_content = fhffile.read()
                count_result = count_chars(file_content)
                char_count = merge_char_count(char_count, count_result[0])
                tuple_count = merge_char_count(tuple_count, count_result[1])

                return char_count, tuple_count, None

            except ValueError as ex:
                pass

    return {}, {}, ffile

def process_results(results):
    cc = {}
    tc = {}
    failed_files = []

    res_len = len(results)

    for i, r in enumerate(results):
        cr = r[0]
        tr = r[1]
        if r[2] is not None:
            failed_files.append(r[2])

        cc = merge_char_count(cc, cr)
        tc = merge_char_count(tc, tr)

    return cc, tc, failed_files

def list_chunks(chunks, llist):
    for i in range(0, len(llist), chunks):
        yield llist[i:i + chunks]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', action='store_true')
    parser.add_argument('-s', '--sort', action='store_true')
    parser.add_argument('-w', '--workers', required=True, help='number of workers', type=int)

    args = parser.parse_args()

    if args.count:
        with open('flist', 'r') as fhflist:
            flist = list(map(str.strip, fhflist.readlines()))

        with Pool(args.workers) as p:
            res = p.map(count_file_chars, flist)

        while True:
            print('processing results...')
            with Pool(args.workers) as p:
                res = p.map(process_results, list(list_chunks(args.workers, res)))

            print(len(res))
            if len(res) < args.workers:
                break

        res = process_results(res)

        cc = res[0]
        tc = res[1]
        failed_files = res[2]

        print('writing results')

        with open('char.res.json', 'w') as fc:
            fc.write(json.dumps(cc))

        with open('tuple.res.json', 'w') as ft:
            ft.write(json.dumps(tc))

        with open('flist.failed', 'w') as ff:
            for failed_file in failed_files:
                ff.write(f"{failed_file}\n")

    if args.sort:
        sort_res('char.res.json')
        sort_res('tuple.res.json')

if __name__ == '__main__':
    main()
