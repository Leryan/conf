#!/usr/bin/env bash

python inplacedel.py -t -s 0 > /dev/null

if [ ! "$?" = "0" ]; then
    echo "tests NOK"
    exit 1
else
    echo "tests OK"
fi

# create a 32MB file
dd if=/dev/urandom of=inplacedel.testfile.orig bs=1024 count=$((1024*32))

rm -rf inplacedel.testfile && cp inplacedel.testfile.orig inplacedel.testfile
ts1=$(date +%s)
python inplacedel.py -f inplacedel.testfile -c $((1024*1024*10)) -s '2:2'
ts2=$(date +%s)
echo -n "chunked1: "
md5sum inplacedel.testfile
echo "time: $(($ts2-$ts1))"

rm -rf inplacedel.testfile && cp inplacedel.testfile.orig inplacedel.testfile
ts1=$(date +%s)
python inplacedel.py -f inplacedel.testfile -c $((1024*1024*10*2)) -s '2:2'
ts2=$(date +%s)
echo -n "chunked2: "
md5sum inplacedel.testfile
echo "time: $(($ts2-$ts1))"

rm -rf inplacedel.testfile && cp inplacedel.testfile.orig inplacedel.testfile
ts1=$(date +%s)
python inplacedel.py -f inplacedel.testfile -s '2:2'
ts2=$(date +%s)
echo -n "ref:      "
md5sum inplacedel.testfile
echo "time: $(($ts2-$ts1))"

rm -rf inplacedel.testfile inplacedel.testfile.orig
