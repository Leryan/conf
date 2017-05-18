#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import argparse

DATE_FORMAT=r'%Y/%m/%d %H:%M:%S'

def dateToTimestamp(dateformat, date):
    return int(time.mktime(datetime.datetime.strptime(date, dateformat).timetuple()))


def timestampToDate(dateformat, timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime(dateformat)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=int, help='timestamp')
    parser.add_argument('-d', type=str, help='date')
    parser.add_argument('-f', type=str, help='format')

    args = parser.parse_args()

    if not args.f:
        df = DATE_FORMAT
    else:
        df = args.f

    if args.t is not None:
        print(timestampToDate(df, args.t))
    elif args.d is not None:
        print(dateToTimestamp(df, args.d))
    else:
        parser.error('-t or -d')
