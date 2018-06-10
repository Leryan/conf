#!/bin/sh

centoxy="centoxy239"

while [ 1 ]; do
    if [ "$(lxc-ls --active|grep "centoxy"|grep -v grep)" = "" ]; then
        break;
    fi
    echo "waiting for shutdown..."
    sleep 1
done
sleep 2
echo "copy mysql"
umount /var/lib/lxc/${centoxy}/rootfs/var/lib/mysql/ || exit 1
rsync -acv --delete /mnt/ram_centoxy/mysql/* /var/lib/lxc/${centoxy}/rootfs/var/lib/mysql/ || exit 1
echo "umount"
umount /mnt/ram_centoxy
umount /var/lib/lxc/${centoxy}/rootfs/usr/local/centreon/www/modules/hpanywhere-git/
umount /var/lib/lxc/${centoxy}/
