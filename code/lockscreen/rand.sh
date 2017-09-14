#!/usr/bin/env bash
cd $(dirname $0)

images=()
limages=$(ls *.png)
nimages=$(ls *.png|wc -l)

for img in $limages; do
    images+=($img)
done

imgnum=$((RANDOM % $nimages))

echo ${images[$imgnum]}
