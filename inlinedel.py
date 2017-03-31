import time
import sys

from termcolor import colored

def gen_input():
    chars = []
    for i in range(ord('a'), ord('z')):
        chars.append(chr(i))

    for i in range(ord('0'), ord('9')):
        chars.append(chr(i))

    for i in range(0, len(chars)):
        yield ''.join(chars[0:i])

def gen_test(content, k, d):
    fc = ''

    for i in range(0, len(content), d + k):
        fcn = content[i:i + k]
        fc = '{}{}'.format(fc, fcn)

    return fc

def inline_del(k, d):
    """
    k: keep k bytes
    d: delete d bytes each k bytes

    for k = 2 and d = 2, available scenarios:
        content = [k][k][d][d]|[k][k][d] no remaining data to keep, but truncate must be ajusted
            flen = 7
            rem  = 0
        content = [k][k][d][d][k][k][d][d]| still no remaining data to keep, truncate is accurate
            flen = 8
            rem  = 0
        content = [k][k][d][d][k][k][d][d]|[k] remaining data to keep
            flen = 0
            rem  = 1

    Loop over (each "full" set of keep) + 1 possible set.
    At the end, go to the last set position + keep.
    If data remains, it's garbage and data length is used to truncate.
    """
    results = ''

    with open('t1', 'r+b') as f:
        f.seek(0, 2)
        flen = f.tell()
        f.seek(0)

        del_max_count = int(flen / (k + d))
        truncate_rem = 0
        for i in range(0, del_max_count):
            write_at = k * (i + 1)
            buff_from = (k + d) * (i + 1)

            f.seek(buff_from)
            buff = f.read(k)

            results += f"{colored('P', 'yellow')}: l{flen} r{buff_from} w{write_at} {buff} p{f.tell()}\n"

            f.seek(write_at)
            f.write(buff)

            results += f"{colored('A', 'green')}: l{flen} r{buff_from} w{write_at} {buff} p{f.tell()}\n"

        f.seek(del_max_count * (k + d) + k)
        rem = f.read()
        if len(rem) <= d:
            truncate_rem += len(rem)

        f.truncate(flen - del_max_count * d - truncate_rem)
        f.flush()
        f.close()

        return results

def test_inline_del(content, k, d):
    cb = bytes(content, encoding='ascii')
    cbw = bytes(gen_test(content, k, d), encoding='ascii')

    with open('t1', 'wb') as f:
        f.write(cb)

    results = inline_del(k, d)

    with open('t1', 'rb') as f:
        cbr = f.read()

        txt = colored('ok', 'green')
        output = sys.stdout

        if cbr != cbw:
            txt = colored('nok', 'red')
            output = sys.stderr
            sys.stderr.write(results)

        output.write(f"{txt}: in:{cb} out:{cbr} want:{cbw} k:{k} d:{d}\n")

def test_inputs_kd(k, d):
    for inp in gen_input():
        test_inline_del(inp, k, d)

if __name__ == '__main__':
    test_inputs_kd(3, 1)
    test_inputs_kd(3, 2)
    test_inputs_kd(4, 2)
    test_inputs_kd(4, 3)
    test_inputs_kd(2, 2)
    test_inputs_kd(2, 4)
    test_inputs_kd(2, 3)
    test_inputs_kd(1, 3)
