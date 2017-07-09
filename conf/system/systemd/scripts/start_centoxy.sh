#!/bin/sh

centoxy="centoxy239"

if [ ! "$(ps faux|grep \"lxc*centoxy\"|grep -v grep)" = "" ]; then
    echo "already running"
    exit 1
fi
echo "ramfs"
mkdir /mnt/ram_centoxy
mount -t tmpfs -o size=300M,mode=777 tmpfs /mnt/ram_centoxy/ || exit 1
echo "mount"
mount /dev/mapper/linux-lxc_${centoxy} /var/lib/lxc/${centoxy}
mount -o bind /home/wrk/doc/depots/g/capensis/oxylane/hpanywhere /var/lib/lxc/${centoxy}/rootfs/usr/local/centreon/www/modules/hpanywhere-git/
echo "copy mysql"
cp -ar /var/lib/lxc/${centoxy}/rootfs/var/lib/mysql /mnt/ram_centoxy/ || exit 1
mount -o bind /mnt/ram_centoxy/mysql/ /var/lib/lxc/${centoxy}/rootfs/var/lib/mysql/ || exit 1
echo "start"
lxc-start -n ${centoxy} -d
