#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#ifndef LINES
#define LINES 10000
#endif

#ifndef COLUMNS
#define COLUMNS 64 * 1024 // L1 cache size on i3-3110M
#endif

#ifndef BUILD_TYPE
#define BUILD_TYPE "default"
#endif

void cache_hit(uint8_t **t) {
    uint64_t i = 0, j = 0;

    for(j = 0; j < LINES; ++j) {
        for(i = 0; i < COLUMNS; ++i) {
            t[j][i] = 255;
        }
    }
}

void cache_miss(uint8_t **t) {
    uint64_t i = 0, j = 0;

    for(i = 0; i < COLUMNS; ++i) {
        for(j = 0; j < LINES; ++j) {
            t[j][i] = 0;
        }
    }
}

// parce que je kiff le C...
void init_array(uint8_t ***t) {
    uint64_t j = 0;

    *t = calloc(LINES, sizeof(uint8_t *));
    for(j = 0; j < LINES; ++j) {
        (*t)[j] = calloc(COLUMNS, sizeof(uint8_t));
    }
}

#ifdef FROM_MAIN
int main(void) {
#else
void bench(void) {
#endif
    uint8_t **t = NULL;
    uint64_t j = 0;
    clock_t t_begin;
    clock_t t_end;
    clock_t t1, t2;

    printf("build type: %s\n", BUILD_TYPE);
#ifdef ALLOC_IN_PLACE
    t = calloc(LINES, sizeof(uint8_t *));
    for(j = 0; j < LINES; ++j) {
        t[j] = calloc(COLUMNS, sizeof(uint8_t));
    }
#else
    init_array(&t);
#endif

    /* cache hit */
    t_begin = clock();
    cache_hit(t);
    t_end = clock();

    t1 = t_end - t_begin;
    printf("cache hit time:  %.2lf\n", (t1) / (double)CLOCKS_PER_SEC);
    /* */

    /* cache miss */
    t_begin = clock();
    cache_miss(t);
    t_end = clock();

    t2 = t_end - t_begin;
    printf("cache miss time: %.2lf\n", (t2) / (double)CLOCKS_PER_SEC);
    /* */

    printf("run time factor: %.2lf\n", ((double)t2)/((double)t1));

    for(j = 0; j < LINES; ++j) {
        free(t[j]);
    }
    free(t);
#ifndef FROM_MAIN
}
#endif

#ifndef FROM_MAIN
int main(void) {
    bench();
#endif

    return EXIT_SUCCESS;
}
