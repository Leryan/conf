#!/bin/bash
format_ssh_key=""
format_hostname=""

format_arch_repo='http://mir.archlinux.fr/$repo/os/$arch'
format_device="/dev/sda"
format_locale="en_GB.UTF-8"
format_keymap="fr-bepo"
format_packages="base efibootmgr grub vim tmux btrfs-progs dosfstools openssh"

format_s_efi=256
format_s_boot=512

parted -s ${format_device} \
    unit B \
    mklabel gpt \
    mkpart primary 0% ${format_s_efi}MiB \
    mkpart primary ${format_s_efi}MiB $((${format_s_efi}+${format_s_boot}))MiB \
    mkpart primary $((${format_s_efi}+${format_s_boot}))MiB 100% || exit 1

sync && partprobe ${format_device} || exit 1

(
echo t
echo 1
echo 1
echo w
) | fdisk ${format_device} || exit 1

sync && partprobe ${format_device} || exit 1

mkfs.vfat -F32 ${format_device}1 || exit 1
mkfs.ext2 -F ${format_device}2 || exit 1
mkfs.btrfs -f ${format_device}3 || exit 1

mount ${format_device}3 /mnt && \
    btrfs subvol create /mnt/archlinux && \
    btrfs subvol create /mnt/home || exit 1

umount /mnt && \
    mount ${format_device}3 -o subvol=archlinux /mnt && \
    mkdir /mnt/home && \
    mount ${format_device}3 -o subvol=home /mnt/home || exit 1

mkdir -p /mnt/boot/ && \
    mount ${format_device}2 /mnt/boot && \
    mkdir /mnt/boot/efi && \
    mount ${format_device}1 /mnt/boot/efi && \

echo ${format_arch_repo} > /etc/pacman.d/mirrorlist
pacstrap /mnt ${format_packages} || exit 1
echo ${format_arch_repo} > /mnt/etc/pacman.d/mirrorlist
arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot/efi/ --bootloader-id=arch_grub --recheck

eval $(blkid -o udev ${format_device}3)
echo "UUID=${ID_FS_UUID}  /   ${ID_FS_TYPE} rw,noatime,ssd,space_cache,subvol=archlinux 0 0" > /mnt/etc/fstab

echo "UUID=${ID_FS_UUID}  /home   ${ID_FS_TYPE} rw,noatime,ssd,space_cache,subvol=home 0 0" >>/mnt/etc/fstab

eval $(blkid -o udev ${format_device}2)
echo "UUID=${ID_FS_UUID}  /boot/ ${ID_FS_TYPE}  rw,block_validity 0 0" >> /mnt/etc/fstab

eval $(blkid -o udev ${format_device}1)
echo "UUID=${ID_FS_UUID}  /boot/efi/ ${ID_FS_TYPE}  rw 0 0" >> /mnt/etc/fstab

genfstab /mnt | grep efivars >> /mnt/etc/fstab

eval $(blkid -o udev ${format_device}3)
cat > /mnt/preboot.sh << EOF
#!/bin/sh
mkdir /root/.ssh && chmod 700 /root/.ssh && echo "${format_ssh_key}" > /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys

echo "KEYMAP=${format_keymap}" > /etc/vconsole.conf
echo "${format_locale}" >> /etc/locale.gen
echo "en_US.UTF-8" >> /etc/locale.gen
locale-gen

echo "${format_hostname}" > /etc/hostname
sed -i /etc/hosts -e 's/localhost$/localhost ${format_hostname}/g'

grub_cmdline_linux="root=UUID=${ID_FS_UUID}"
sed -e 's/GRUB_CMDLINE_LINUX=.*/GRUB_CMDLINE_LINUX=${grub_cmdline_linux}/' -i /etc/default/grub
grub-mkconfig -o /boot/grub/grub.cfg

systemctl enable sshd
systemctl enable systemd-networkd

mkinitcpio -p linux
EOF

chmod +x /mnt/preboot.sh

arch-chroot /mnt /preboot.sh

cat > /mnt/etc/systemd/eth0.network << EOF
[Match]
Name=eth0

[Network]
DHCP=yes
EOF

sync && umount -R /mnt && reboot
