```
gdisk -> 512M, EF00
gdisk -> +512M, 8300
gdisk -> ALL, 8300,

mkfs.fat -F32 /dev/diskp1
mkfs.ext2 /dev/diskp2
cryptsetup luksFormat /dev/diskp3

cryptsetup luksOpen --allow-discards /dev/diskp3 arch_luks
pvcreate /dev/mapper/arch_luks
vgcreate arch /dev/mapper/arch_luks
lvcreate -L30G arch -n root
mkfs.ext4 /dev/mapper/arch-root
```

```
mount /dev/mapper/arch-root /mnt
mkdir /mnt/boot
mount /dev/diskp2 /mnt/boot
mkdir /mnt/boot/efi
mount /dev/diskp1 /mnt/boot/efi

pacstrap /mnt base base-devel cryptsetup powertop cpupower tmux grub

genfstab /mnt >> /mnt/etc/fstab

arch-chroot /mnt
```

#### \*tab

`/etc/crypttab.initramfs`

```
luks_arch /dev/diskp3 none luks,discard
```

`/etc/fstab`

 * `noatime`

#### `/etc/mkinitcpio.conf`

```bash
MODULES=(i915 iwlwifi)

HOOKS=(base systemd autodetect modconf keyboard sd-vconsole block sd-encrypt sd-lvm2 filesystems fsck)

COMPRESSION="cat"
```

#### GRUB

`/etc/default/grub`

```bash
GRUB_TIMEOUT=3
GRUB_CMDLINE_LINUX_DEFAULT="quiet root=/dev/mapper/arch-root"
```

```
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=archlinux
efibootmgr -v
grub-mkconfig -o /boot/grub/grub.cfg
```

#### Misc

```bash
echo mothma > /etc/hostname

cat > /etc/hosts << EOF
127.0.0.1 localhost mothma
::1       localhost mothma
EOF

localectl set-x11-keymap fr pc105 bepo
localectl set-keymap fr-bepo
```

#### Packages

```
pacman -S i3-wm i3lock i3status nitrogen xterm dmenu rofi lightdm lightdm-gtk-greeter pulseaudio firefox libva-intel-driver xorg-xinit arandr xrandr redshift python-gobject python-xdg gnome-themes-extra pavucontrol chromium konsole ttf-fira-code ttf-fira-mono ttf-liberation ttf-droid ttf-dejavu networkmanager network-manager-applet networkmanager-openvpn docker lxc dnsmasq gnome-keyring vim tmux xorg-server
```

#### User

```
useradd -m florent
usermod -a -G sudo,network,users florent
```


#### Final

```
mkinitcpio -p linux
exit
```

```
reboot
```
