# Gentoo

Everything here will be done in root.

## chroot / LXC

```bash
mkdir -p /var/lib/lxc/94-gentoo/rootfs
lvcreate linux -n lxc_94_gentoo -L50GB
mkfs.ext4 /dev/linux/lxc_94_gentoo
mount /dev/linux/lxc_94_gentoo /var/lib/lxc/94-gentoo/rootfs
```

Set LXC configuration

```bash
cat > /var/lib/lxc/94-gentoo/config << EOF
lxc.devttydir = lxc
lxc.tty = 4
lxc.pts = 1024
lxc.kmsg = 0

lxc.mount.auto = proc:mixed sys:ro

lxc.hook.clone = /usr/share/lxc/hooks/clonehostname

lxc.cap.drop = mac_admin mac_override
lxc.cap.drop = sys_module sys_nice sys_pacct
lxc.cap.drop = sys_rawio sys_time

# Control Group devices: all denied except those whitelisted
lxc.cgroup.devices.deny = a
# Allow any mknod (but not reading/writing the node)
lxc.cgroup.devices.allow = c *:* m
lxc.cgroup.devices.allow = b *:* m
## /dev/null
lxc.cgroup.devices.allow = c 1:3 rwm
## /dev/zero
lxc.cgroup.devices.allow = c 1:5 rwm
## /dev/full
lxc.cgroup.devices.allow = c 1:7 rwm
## /dev/tty
lxc.cgroup.devices.allow = c 5:0 rwm
## /dev/random
lxc.cgroup.devices.allow = c 1:8 rwm
## /dev/urandom
lxc.cgroup.devices.allow = c 1:9 rwm
## /dev/tty[1-4] ptys and lxc console
lxc.cgroup.devices.allow = c 136:* rwm
## /dev/ptmx pty master
lxc.cgroup.devices.allow = c 5:2 rwm

# Blacklist some syscalls which are not safe in privileged
# containers
lxc.seccomp = /usr/share/lxc/config/common.seccomp

lxc.arch = x86_64

lxc.autodev = 1

# NOT GENERIC #
lxc.utsname = 94-gentoo
lxc.rootfs = /var/lib/lxc/94-gentoo/rootfs
lxc.network.type = veth
lxc.network.flags = up
lxc.network.link = br-test
lxc.network.name = eth0
# /NOT GENERIC #
EOF
```

Get a stage3 archive from http://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64/

```bash
wget http://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64/stage3-amd64-20150730.tar.bz2
tar xpf stage3-amd64-20150730.tar.bz2 -C /var/lib/lxc/94-gentoo/rootfs
```

A few steps are required:

1. Choose a mirror from https://www.gentoo.org/downloads/mirrors/
1. Put that mirror URL in `/etc/portage/make.conf` like this: `GENTOO_MIRRORS="GENTOO_MIRRORS="URL1 URL2 ..."`
1. Copy resolv.conf: `cat /etc/resolv.conf > /var/lib/lxc/94-gentoo/rootfs/etc/resolv.conf`

Then we can chroot to our new gentoo base system and change the root password:

```bash
chroot /var/lib/lxc/94-gentoo/rootfs /bin/bash
source /etc/profile
passwd root
```

If you want a simple chroot, mount-bind some filesystems:

```bash
mount -t proc proc /var/lib/lxc/94-gentoo/rootfs/proc
mount --rbind /sys /var/lib/lxc/94-gentoo/rootfs/sys
mount --make-rslave /var/lib/lxc/94-gentoo/rootfs/sys
mount --rbind /dev /var/lib/lxc/94-gentoo/rootfs/dev
mount --make-rslave /var/lib/lxc/94-gentoo/rootfs/dev
```

And if you use LXC, just start it:

```bash
lxc-start -n 94-gentoo -d
lxc-console -n 94-gentoo
# press enter once, enter root.
# setup your network by hand, is there isn't any DHCP client.
```

Sources:

 * https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Base#Chrooting

## Base install

From here, your system is ready to use. But there isn't much to do with it... So we'll add some configurations and softwares, then rebuild the _entire_ system to ensure everything is truly optimized. Isn't gentoo for that purpose? :)

Basically, Gentoo works with a bunch of variables, stored into `/etc/portage/make.conf`, but not only.

The main variable is the `USE` variable. It's a list of space-separated values, like this:

```bash
USE="amd64 X aspell openssl ..."
```

### Portage / USE flags and other flags

First we need an up-to-date `portage` tree.

```bash
emerge-webrsync
```

Personally, I always start from an "empty" profile so I can tune my system for each use. This needs an extra "start" time as you will discover missing functionalities as you use your system. But once you have your uses, you know exactly and definitely what you have.

Start by listing all available profiles. Here is the result on my system:

```bash
root# eselect profile list
Available profile symlink targets:
  [1]   default/linux/amd64/13.0 *
  [2]   default/linux/amd64/13.0/selinux
  [3]   default/linux/amd64/13.0/desktop
  [4]   default/linux/amd64/13.0/desktop/gnome
  [5]   default/linux/amd64/13.0/desktop/gnome/systemd
  [6]   default/linux/amd64/13.0/desktop/kde
  [7]   default/linux/amd64/13.0/desktop/kde/systemd
  [8]   default/linux/amd64/13.0/desktop/plasma
  [9]   default/linux/amd64/13.0/desktop/plasma/systemd
  [10]  default/linux/amd64/13.0/developer
  [11]  default/linux/amd64/13.0/no-multilib
  [12]  default/linux/amd64/13.0/systemd
  [13]  default/linux/amd64/13.0/x32
  [14]  hardened/linux/amd64
  [15]  hardened/linux/amd64/selinux
  [16]  hardened/linux/amd64/no-multilib
  [17]  hardened/linux/amd64/no-multilib/selinux
  [18]  hardened/linux/amd64/x32
  [19]  hardened/linux/musl/amd64
  [20]  default/linux/uclibc/amd64
  [21]  hardened/linux/uclibc/amd64
```

If you want to setup your system for `systemd`, choose 12° profile:

```bash
eselect profile set 12
```

If you're curious about what these profiles do, have a look in `/usr/portage/profiles/*` and `/usr/portage/profiles/use.desc`.

From here, i'll assume you choose profile 1: all defaults. You can list current USE flags:

```bash
emerge --info | grep "^USE"
```

You can see many other variables. You can just play with them as you want and put them into `/etc/portage/make.conf`.

### Configure Portage repositories the new way

The new way is to setup `/etc/portage/repos.conf/<repo>.conf` files. Here is the main file for gentoo repository:

```bash
mkdir /etc/portage/repos.conf
cat > /etc/portage/repos.conf/gentoo.conf << EOF
[DEFAULT]
main-repo = gentoo

[gentoo]
location = /usr/portage
sync-type = rsync
sync-uri = rsync://rsync.gentoo.org/gentoo-portage
auto-sync = yes
EOF
```

### systemd

If you want systemd, follow these instructions: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Base#Optional:_Using_systemd


### Use some USE and make a make.conf

Here are some of my use flags and other variables at the time I write these lines:

```bash
USE="bindist mmx sse sse2 -kde -qt4 ssse3 sse4_1 sse4_2 sse4 sse3 cryptsetup pulseaudio ffmpeg -libav alsa-plugin jack x264 xft dbus xinerama systemd jpeg vaapi X x265 openssl directfb fbcon vpx libass flac samba png gnome-keyring icu spell aspell"
PORTDIR="/usr/portage"
DISTDIR="${PORTDIR}/distfiles"
PKGDIR="${PORTDIR}/packages"
MAKEOPTS="-j2"
GENTOO_MIRRORS="http://gentoo.mirrors.ovh.net/gentoo-distfiles/"
INPUT_DEVICES="evdev synaptics"
LINGUAS="en_US en_GB fr"
VIDEO_CARDS="intel vesa"
ACCEPT_LICENSE="*"
RUBY_TARGETS="ruby19 ruby20 ruby21"
CPU_FLAGS_X86="avx mmx mmxext popcnt sse sse2 sse3 sse4_1 sse4_2 ssse3"
```

Well, explain a bit:

 * USE: the main flags. I want PulseAudio, ffmpeg, vaapi (intel video cards) and other stuff… and as my processor supports sse* and ssse*, I enable them here.
 * PORTDIR: the main folder of the portage tree.
 * MAKEOPTS: every parameters you may want to pass to the `make` command when `emerge` will build your softwares. Here, `-j2` for two parallels build processes.
 * GENTOO_MIRRORS: see above.
 * INPUT_DEVICES: i want to use the `evdev` and `synaptics` drivers for X.org.
 * LINGUAS: as I'm french, I want this language, but keep english as well.
 * VIDEO_CARDS: this computer runs with an Intel i915 card, and keep vesa for security.
 * ACCEPT_LICENSE: i don't care what license the software is.
 * RUBY_TARGETS: ruby versions I allow on my system.
 * CPU_FLAGS_X86: as this machine is an X86, I want the best CPU flags. See below.

### CPU_FLAGS_X86 and CFLAGS

Before doing anything, if you want to build your softwares to be able to use your cpu's capabilities, emerge and run this tool:

```bash
root# emerge -a app-portage/cpuinfo2cpuflags
root# cpuinfo2cpuflags-x86
CPU_FLAGS_X86="aes avx mmx mmxext popcnt sse sse2 sse3 sse4_1 sse4_2 ssse3"
```

If you think these informations are correct, put the whole line into `/etc/portage/make.conf`. Check `/proc/cpuinfo`. Beware this can break your system.

I also set `-march=native` in the `CFLAGS` variable. But some ebuilds, such as `ffmpeg` looks at `CPU_FLAGS_X86` before building.

### Building in TMPFS

If you have a lot of RAM, you can speed up your build, as of keeping safe your SSD disk or not doing too much I/Os on your hard drive.

This doesn't apply for a chroot or LXC. You will need to manually mount the tmpfs from your host, if chroot, and from LXC configuration, if LXC.

Here is the extra configuration line for LXC (first get the uid and gid of portage: `grep portage /etc/passwd`):

```
echo 'lxc.mount.entry = tmpfs var/tmp/portage tmpfs size=6G,uid=250,gid=250,mode=0755 0 0' >> /var/lib/lxc/94-gentoo/config
# restart your container, re-setup your network.
```

Here are the steps:

1. Create a TMPFS directory for portage
1. Tell portage to build packages on it. Or don't tell it, just mount tmpfs on its default TMPDIR.
1. Tell portage not to build some packages on it with an `env` configuration and a list of packages.

Depending on how much RAM you have, building everything in RAM could not be a good idea. Large packages such as LibreOffice, Firefox, Chromium or GCC may need up to/more than 4GB of RAM!

For me, I give 6GB of TMPFS and I can build firefox in RAM. Isn't that cool?

```bash
# Create and mount the tmpfs
echo 'tmpfs		/var/tmp/portage		tmpfs	size=6G,uid=portage,gid=portage,mode=775,noatime	0 0' >> /etc/fstab
mount /var/tmp/portage

# Setup the no-tmpfs environment
mkdir /var/tmp/portage-notmpfs
mkdir /etc/portage/env/
echo 'PORTAGE_TMPDIR="/var/tmp/portage-notmpfs"' > /etc/portage/env/notmpfs.conf
chown portage:portage /var/tmp/portage-notmpfs
chmod 755 /var/tmp/portage-notmpfs

# Here is the list of big packages
cat > /etc/portage/package.env << EOF
app-office/libreoffice notmpfs.conf
mail-client/thunderbird notmpfs.conf
www-client/chromium notmpfs.conf
www-client/firefox notmpfs.conf
EOF
```

As I said, I do build firefox in RAM, but here you have the lines for not doing that.

Sources:

 * https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Base#Configuring_portage
 * https://wiki.gentoo.org/wiki//etc/portage/repos.conf
 * https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Base#Optional:_Using_systemd
 * https://www.gentoo.org/support/news-items/2015-01-28-cpu_flags_x86-introduction.html
 * https://wiki.gentoo.org/wiki/Portage_TMPDIR_on_tmpfs
 * man lxc.container.conf

### Extend your system, cool tools

First, you'll need to search packages (I should say ebuilds, but I don't care), get informations about their uses, enable or disable flags…

But, yes, how will you build those packages? Here is a self-describing command:

```bash
emerge --ask category/ebuild
# --ask can be shortened with -a
```

Here are the three main tools I use every-time:

 * equery: install app-portage/gentoolkit
 * euse: install app-portage/gentoolkit
 * eix: install app-portage/eix

Look at https://github.com/Leryan/gentoo-config#other-tools for explanations.
