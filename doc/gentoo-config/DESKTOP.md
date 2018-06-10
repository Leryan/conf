# Desktop configuration

We should USE `X` by default and disable it when needed. I personnaly dont want gtk/qt enabled by default, so a manage myself what I want.

### xdg-open

Some programs rely on some programs in `xdg-utils`, like `xdg-open` to choose the correct program for your URL or file. Here, set Firefox as default web browser:

```bash
xdg-mime default firefox.desktop x-scheme-handler/http
xdg-mime default firefox.desktop x-scheme-handler/https
xdg-mime default firefox.desktop text/html
```

Another command should work for full Desktop Environments like KDE, GNOME, XFCE… but I use i3-wm:

```bash
xdg-settings set default-web-browser firefox.desktop
```
