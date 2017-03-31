#!/usr/bin/env python

# Python >= 3.6.0

import io
import sys
import argparse

from termcolor import colored

TEST_BYTES = []

def init_chars():
    for i in range(ord('a'), ord('z')):
        TEST_BYTES.append(chr(i))

    for i in range(ord('0'), ord('9')):
        TEST_BYTES.append(chr(i))

def gen_input():
    for i in range(0, len(TEST_BYTES)):
        content = ''.join(TEST_BYTES[0:i])
        yield bytes(content, encoding='ascii')

def gen_test(cbi, k, d):
    """
    Do the same thing as inplace_del, but with a much simpler and safer algo: copy data.
    Intended for tests only.
    """
    cbt = io.BytesIO()

    for i in range(0, len(cbi), d + k):
        cbtn = cbi[i:i + k]
        cbt.write(cbtn)

    cbt.seek(0)
    return cbt.read()

def inplace_del(f, k, d):
    """
    f: file or anything acting as a binary file (BytesIO...)
    k: keep k bytes
    d: delete d bytes each k bytes

    for k = 2 and d = 2, available scenarios:
        content = [k][k][d][d]|[k][k][d] no remaining data to keep, but truncate must be ajusted
            flen = 7
            rem  = 0
        content = [k][k][d][d][k][k][d][d]| still no remaining data to keep, truncate is accurate
            flen = 8
            rem  = 0
        content = [k][k][d][d][k][k][d][d]|[k] remaining data to keep.
            flen = 0
            rem  = 1

    Loop over (each "full" set of keep) + 1. +1 to keep any remaining data.
    At the end, go to the last set position + keep.
    If data remains, it's garbage and data length is used to truncate.
    """

    pos_bak = f.tell()
    f.seek(0, 2)
    flen = f.tell()
    f.seek(pos_bak)

    del_max_count = int(flen / (k + d))
    truncate_rem = 0
    p = 0

    for i in range(0, del_max_count):
        write_at = k * (i + 1)
        buff_from = (k + d) * (i + 1)

        f.seek(buff_from)
        buff = f.read(k)

        f.seek(write_at)
        f.write(buff)

        pn = int((write_at + k) * 100 / flen)
        if p != pn:
            print('{}%'.format(p))
            p = pn

    f.seek(del_max_count * (k + d) + k)
    rem = f.read()
    if len(rem) <= d:
        truncate_rem += len(rem)

    f.truncate(flen - del_max_count * d - truncate_rem)

def test_inplace_del(cbi, k, d):
    cbw = gen_test(cbi, k, d)

    f = io.BytesIO(cbi)
    f.seek(0)

    inplace_del(f, k, d)

    f.seek(0)
    cbr = f.read()

    txt = colored('ok', 'green')
    output = sys.stdout

    if cbr != cbw:
        txt = colored('nok', 'red')
        output = sys.stderr

    output.write(f"{txt}: in:{cbi} out:{cbr} want:{cbw} k:{k} d:{d}\n")

def test_inputs_kd(k, d):
    for inp in gen_input():
        test_inplace_del(inp, k, d)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='tests')
    parser.add_argument('-f', dest='fpath')
    args = parser.parse_args()

    if args.fpath:
        with open(args.fpath, 'r+b') as f:
            inplace_del(f, int(args.tests.split(':')[0]), int(args.tests.split(':')[1]))

    if args.tests:
        init_chars()
        test_inputs_kd(3, 1)
        test_inputs_kd(3, 2)
        test_inputs_kd(4, 2)
        test_inputs_kd(4, 3)
        test_inputs_kd(2, 2)
        test_inputs_kd(2, 4)
        test_inputs_kd(2, 3)
        test_inputs_kd(1, 3)