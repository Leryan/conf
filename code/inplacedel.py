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

    for i in range(0, del_max_count):
        write_at = k * (i + 1)
        buff_from = (k + d) * (i + 1)

        f.seek(buff_from)
        buff = f.read(k)

        f.seek(write_at)
        f.write(buff)

    f.seek(del_max_count * (k + d) + k)
    rem = f.read()
    if len(rem) <= d:
        truncate_rem += len(rem)

    f.truncate(flen - del_max_count * d - truncate_rem)

def inplace_del_chunks(f, k, d, csize=1024*1024*10):
    written = 0
    read_max = (k + d) * csize
    while True:

        cb = f.read(read_max)
        seek_next = f.tell()

        bio = io.BytesIO(cb)
        bio.seek(0)

        inplace_del(bio, k, d)

        bio.seek(0)
        wc = bio.read()

        f.seek(written)
        f.write(wc)
        f.seek(seek_next)

        written += len(wc)

        f.seek(seek_next)

        if len(cb) < read_max:
            break

    f.truncate(written)

def test_inplace_del(cbi, k, d):
    failed = False
    cbw = gen_test(cbi, k, d)

    f = io.BytesIO(cbi)
    f.seek(0)

    inplace_del(f, k, d)

    f.seek(0)
    cbr = f.read()

    txt = colored('ok', 'green')
    output = sys.stdout

    if cbr != cbw:
        failed = True
        txt = colored('nok', 'red')
        output = sys.stderr

    output.write(f"{txt}: in:{cbi} out:{cbr} want:{cbw} k:{k} d:{d}\n")
    return failed

def test_inplace_del_chunks(cbi, k, d):
    failed = False
    cbw = gen_test(cbi, k, d)

    f = io.BytesIO(cbi)
    f.seek(0)

    inplace_del_chunks(f, k, d, 2)

    f.seek(0)
    cbr = f.read()

    txt = colored('ok', 'green')
    output = sys.stdout

    if cbr != cbw:
        failed = True
        txt = colored('nok', 'red')
        output = sys.stderr

    output.write(f"{txt}: in:{cbi} out:{cbr} want:{cbw} k:{k} d:{d}\n")
    return failed

def test_inputs_kd(k, d):
    failed = False
    for inp in gen_input():
        failed = failed or test_inplace_del(inp, k, d)
        failed = failed or test_inplace_del_chunks(inp, k, d)

    return failed

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='tests', action='store_true')
    parser.add_argument('-f', dest='fpath')
    parser.add_argument('-c', dest='chunks', default=0, type=int)
    parser.add_argument('-s', dest='sizes', required=True)
    args = parser.parse_args()

    if args.fpath:
        k = int(args.sizes.split(':')[0])
        d = int(args.sizes.split(':')[1])

        with open(args.fpath, 'r+b') as f:
            if args.chunks == 0:
                inplace_del(f, k, d)
            else:
                inplace_del_chunks(f, k, d, args.chunks)

    elif args.tests:
        init_chars()
        failed = False
        failed = failed or test_inputs_kd(3, 1)
        failed = failed or test_inputs_kd(3, 2)
        failed = failed or test_inputs_kd(4, 2)
        failed = failed or test_inputs_kd(4, 3)
        failed = failed or test_inputs_kd(2, 2)
        failed = failed or test_inputs_kd(2, 4)
        failed = failed or test_inputs_kd(2, 3)
        failed = failed or test_inputs_kd(1, 3)
        failed = failed or test_inputs_kd(1, 8)
        failed = failed or test_inputs_kd(8, 1)

        if failed:
            sys.exit(1)
