# Installation instructions

This code probably only works on Raspberry Pi OS Lite 64-bit, e.g.:
`2023-10-10-raspios-bookworm-arm64-lite.img.xz`.

Download the base OS image from
[raspberrypi.com operating systems](`https://www.raspberrypi.com/software/operating-systems/`)
> Raspberry Pi OS (64-bit) > Raspberry Pi OS Lite.

Install the image on the Pi's SD card, e.g. using `dd` from Linux, or
[Raspberry Pi Imager](https://www.raspberrypi.com/software/).

Boot the Pi, with a keyboard and HDMI monitor connected, and create a default
user, e.g. user=fcch, password=fcch, when prompted. Log in as that user on the
console.

Run `sudo raspi-config` and:
* Set a machine name, e.g. `fcch-kiosk-main`.
* Configure WiFi network & password.
* Enable ssh for remote admin.

Update packages:

```shell
sudo apt update
sudo apt dist-upgrade
```

Reboot.

Install the fcch-kiosk package:

```shell
cd /tmp
wget https://www.fortcollinscreatorhub.org/rpi-packages/fcch-kiosk_1_all.deb
sudo apt install ./fcch-kiosk_1_all.deb
```

The kiosk display will automatically start; it will initially draw a black
screen for perhaps 30 seconds. Press Alt-F1 on the keyboard to get back to
your shell prompt VT, and Alt-F7 to get back to the kiosk VT. Switching VTs
back/forth will refresh the display's text/console content, but the kiosk
display may not redraw until it's time to display a new URL. Make sure to
check that the `apt install` completes OK, since it will complete long after
the signage display starts running.

You may want to reboot again to make sure the kiosk display works correctly
after a reboot.

Visit `http://fcch-kiosk-main.local/` to configure which URLs the kiosk should
display.
