#!/bin/sh
workdir=$(readlink -e $(dirname ${0}))
python deploy.py --deploy-from ${workdir}/user
