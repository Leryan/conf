#!/bin/sh
systemctl stop lightdm
echo "0000:01:00.0" > /sys/bus/pci/drivers/vfio-pci/unbind
echo "0000:01:00.1" > /sys/bus/pci/drivers/vfio-pci/unbind
#echo "0000:00:1f.3" > /sys/bus/pci/drivers/vfio-pci/unbind
echo 1 > /sys/bus/pci/devices/0000:01:00.0/remove
echo 1 > /sys/bus/pci/devices/0000:01:00.1/remove
#echo 1 > /sys/bus/pci/devices/0000:00:1f.3/remove
echo 1 > /sys/bus/pci/rescan

if [ ! "$(lsmod|grep nvidia)" = "" ]; then
    rmmod nvidia_drm
    rmmod nvidia_modeset
    rmmod nvidia
fi

modprobe nvidia_drm
#modprobe snd_hda_intel
sysctl vm.nr_hugepages=0
systemctl restart lightdm
