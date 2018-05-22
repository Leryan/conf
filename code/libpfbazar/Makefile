CC ?= cc
CFLAGS += -I./ -O2 -W -Wall
LDFLAGS=-lm -lncursesw -shared
all: pfbazar_complexe.c pfbazar_forme.c
	$(CC) $(CFLAGS) pfbazar_complexe.c pfbazar_forme.c -fPIC -o libpfbazar.so $(LDFLAGS)
