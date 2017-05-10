#!/bin/sh
gcc -O0 -DFROM_MAIN -DALLOC_IN_PLACE -DBUILD_TYPE='"O0.main.inplace"' cpucache.c -o cpucache && ./cpucache
echo
gcc -O0 -DFROM_MAIN -DBUILD_TYPE='"O0.main.out"' cpucache.c -o cpucache && ./cpucache
echo
gcc -O2 -DFROM_MAIN -DALLOC_IN_PLACE -DBUILD_TYPE='"O2.main.inplace"' cpucache.c -o cpucache && ./cpucache
echo
gcc -O2 -DFROM_MAIN -DBUILD_TYPE='"O2.main.out"' cpucache.c -o cpucache && ./cpucache
echo
gcc -O3 -DFROM_MAIN -DALLOC_IN_PLACE -DBUILD_TYPE='"O3.main.inplace"' cpucache.c -o cpucache && ./cpucache
echo
gcc -O3 -DFROM_MAIN -DBUILD_TYPE='"O3.main.out"' cpucache.c -o cpucache && ./cpucache
