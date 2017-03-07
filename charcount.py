#!/usr/bin/env python

import argparse
import encodings
import json
import operator

def get_encs():
    return encodings.aliases.aliases.values()

def count_chars(chars):
    char_count = {}
    tuple_count = {}
    prev_char = None

    for char in chars:
        if char in ["\n", "\t", "\r", " "]:
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

        if prev_char is not None and char not in ["\n", "\t", "\r", " "]:
            char_tuple = f'{prev_char}{char}'

            if char_tuple in tuple_count:
                tuple_count[char_tuple] += 1
            else:
                tuple_count[char_tuple] = 1
        elif char not in ["\n", "\t", "\r", " "]:
            prev_char = char

        else:
            prev_char = None

    return char_count, tuple_count

def merge_char_count(left, right):
    merged = {}
    chars = list(left.keys())
    chars.extend(list(right.keys()))

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

def count_file_chars():
    flist = []
    char_count = {}
    tuple_count = {}

    with open('flist', 'r') as fhflist:
        flist = map(str.strip, fhflist.readlines())

    encs = get_encs()
    encs = ['utf-8',]
    encs.extend(encs)

    for ffile in flist:
        print(f'processing file {ffile}')
        for enc in encs:
            with open(ffile, 'r', encoding=enc) as fhffile:
                try:
                    file_content = fhffile.read()
                    count_result = count_chars(file_content)
                    char_count = merge_char_count(char_count, count_result[0])
                    tuple_count = merge_char_count(tuple_count, count_result[1])

                except Exception:
                    break

    res0 = json.dumps(char_count)
    res1 = json.dumps(tuple_count)

    with open('char.res.json', 'w') as fres:
        fres.write(res0)

    with open('tuple.res.json', 'w') as fres:
        fres.write(res1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', action='store_true')
    parser.add_argument('-s', '--sort', action='store_true')

    args = parser.parse_args()

    if args.count:
        count_file_chars()
    if args.sort:
        sort_res('char.res.json')
        sort_res('tuple.res.json')

if __name__ == '__main__':
    main()
