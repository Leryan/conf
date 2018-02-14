#!/bin/sh
systemctl stop lightdm

if [ ! "$(lsmod|grep nvidia)" = "" ]; then
    rmmod nvidia_drm || exit 1
    rmmod nvidia_modeset || exit 1
    rmmod nvidia || exit 1
fi

#if [ ! "$(lsmod|grep snd_hda_intel)" = "" ]; then
#    rmmod snd_hda_intel
#fi

echo "10de 13c2" > /sys/bus/pci/drivers/vfio-pci/new_id
echo "0000:01:00.0" > /sys/bus/pci/devices/0000\:01\:00.0/driver/unbind
echo "0000:01:00.0" > /sys/bus/pci/drivers/vfio-pci/bind
echo "10de 13c2" > /sys/bus/pci/drivers/vfio-pci/remove_id

echo "10de 0fbb" > /sys/bus/pci/drivers/vfio-pci/new_id
echo "0000:01:00.1" > /sys/bus/pci/devices/0000\:01\:00.1/driver/unbind
echo "0000:01:00.1" > /sys/bus/pci/drivers/vfio-pci/bind
echo "10de 0fbb" > /sys/bus/pci/drivers/vfio-pci/remove_id

#echo "8086 a170" > /sys/bus/pci/drivers/vfio-pci/new_id
#echo "0000:00:1f.3" > /sys/bus/pci/drivers/vfio-pci/bind
#echo "8086 a170" > /sys/bus/pci/drivers/vfio-pci/remove_id

sysctl vm.nr_hugepages=5120
systemctl restart lightdm
