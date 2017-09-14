#!/usr/bin/env bash
cd $(dirname $0)

images=$(ls | grep -Ev "\.(png|sh)$")

for img in ${images}; do
    if [ ! -f ${img}.png ]; then
        echo "converting ${img}"
        convert ${img} ${img}.png
    fi
done
