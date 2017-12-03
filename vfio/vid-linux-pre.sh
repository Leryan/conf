#!/bin/sh
systemctl stop lightdm
echo "0000:01:00.0" > /sys/bus/pci/drivers/vfio-pci/unbind
echo "0000:01:00.1" > /sys/bus/pci/drivers/vfio-pci/unbind
echo 1 > /sys/bus/pci/devices/0000:01:00.0/remove
echo 1 > /sys/bus/pci/devices/0000:01:00.1/remove
echo 1 > /sys/bus/pci/rescan
rmmod nvidia_drm
rmmod nvidia_modeset
rmmod nvidia

modprobe nvidia_drm
sysctl vm.nr_hugepages=0
systemctl restart lightdm
