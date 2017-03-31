import time
import sys

from termcolor import colored

def dfs(content, byte_keep, byte_del):
    fc = ''

    for i in range(0, len(content), byte_del + byte_keep):
        fcn = content[i:i + byte_keep]
        fc = '{}{}'.format(fc, fcn)

    return fc

def t1(content, byte_keep, byte_del):
    results = ''
    cb = bytes(content, encoding='ascii')
    cbw = bytes(dfs(content, byte_keep, byte_del), encoding='ascii')

    with open('t1', 'wb') as f:
        f.write(cb)

    with open('t1', 'r+b') as f:
        f.seek(0, 2)
        flen = f.tell()
        f.seek(0)

        del_max_count = int(flen / (byte_keep + byte_del))
        truncate_rem = 0
        for i in range(0, del_max_count):
            write_at = byte_keep * (i + 1)
            buff_from = (byte_keep + byte_del) * (i + 1)

            f.seek(buff_from)
            buff = f.read(byte_keep)

            results += f"{colored('P', 'yellow')}: l{flen} r{buff_from} w{write_at} {buff} p{f.tell()}\n"

            f.seek(write_at)
            f.write(buff)

            results += f"{colored('A', 'green')}: l{flen} r{buff_from} w{write_at} {buff} p{f.tell()}\n"


        f.seek(del_max_count * (byte_keep + byte_del) + byte_keep)
        rem = f.read()
        if len(rem) <= byte_del:
            truncate_rem += len(rem)

        f.truncate(flen - del_max_count * byte_del - truncate_rem)
        f.flush()
        f.close()

    with open('t1', 'rb') as f:
        cbr = f.read()
        txt = colored('ok', 'green')
        if cbr != cbw:
            txt = colored('nok', 'red')
            sys.stdout.write(results)

        print(f"{txt}: in:{cb} out:{cbr} want:{cbw} k:{byte_keep} d:{byte_del}")

def go(k, d):
    chars = []
    for i in range(ord('a'), ord('z')):
        chars.append(chr(i))

    for i in range(ord('0'), ord('9')):
        chars.append(chr(i))

    for i in range(0, len(chars)):
        t1(''.join(chars[0:i]), k, d)

go(3, 1)
go(3, 2)
go(4, 2)
go(4, 3)
go(2, 2)
go(2, 4)
