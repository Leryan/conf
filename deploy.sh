#!/bin/sh
workdir=$(readlink -e $(dirname ${0}))
python deploy.py --deploy-from ${workdir}/user

cd st
make clean && make && sudo make install
