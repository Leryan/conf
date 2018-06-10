#!/bin/sh
if [ ! "$(lsmod | grep r8169)" = "" ]; then
	rmmod r8169
	sleep 2
	modprobe r8169
fi
