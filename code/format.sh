#!/bin/bash
format_ssh_key=""
format_hostname="padme"

format_arch_repo='http://mir.archlinux.fr/$repo/os/$arch'
format_device="$1"
format_locale="en_GB.UTF-8 UTF-8"
format_keymap="fr-bepo"
format_packages="base efibootmgr grub vim tmux btrfs-progs dosfstools openssh"

format_s_efi=256
format_s_boot=512

if [ "${format_device}" = "" ]; then
	echo "missing device on first parameter"
	exit 1
fi

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
    mount ${format_device}1 /mnt/boot/efi || exit 1

echo "Server = ${format_arch_repo}" > /etc/pacman.d/mirrorlist
pacstrap /mnt ${format_packages} || exit 1
echo "Server = ${format_arch_repo}" > /mnt/etc/pacman.d/mirrorlist
arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot/efi/ --bootloader-id=arch_grub --recheck || exit 1

genfstab -U /mnt | sed 's/relatime/noatime/g' > /mnt/etc/fstab || exit 1

echo "KEYMAP=${format_keymap}" > /mnt/etc/vconsole.conf
echo "${format_locale}" >> /mnt/etc/locale.gen
echo "en_US.UTF-8 UTF-8" >> /mnt/etc/locale.gen
echo "${format_hostname}" > /mnt/etc/hostname
sed -i /mnt/etc/hosts -e 's/localhost$/localhost ${format_hostname}/g'
grub_cmdline_linux="root=UUID=$(lsblk -rno UUID ${format_device}3) net.ifnames=0"
sed -e "s/GRUB_CMDLINE_LINUX=.*/GRUB_CMDLINE_LINUX=\"${grub_cmdline_linux}\"/" -i /mnt/etc/default/grub
mkdir /mnt/root/.ssh && chmod 700 /mnt/root/.ssh && echo "${format_ssh_key}" > /mnt/root/.ssh/authorized_keys && chmod 600 /mnt/root/.ssh/authorized_keys
cat > /mnt/etc/systemd/network/eth0.network << EOF
[Match]
Name=eth0

[Network]
DHCP=yes
EOF

cat > /mnt/preboot.sh << EOF
#!/bin/sh
locale-gen

mkinitcpio -p linux

grub-mkconfig -o /boot/grub/grub.cfg

systemctl enable sshd
systemctl enable systemd-networkd
EOF

chmod +x /mnt/preboot.sh && \
    arch-chroot /mnt /preboot.sh && \
    sync && \
    umount -R /mnt
