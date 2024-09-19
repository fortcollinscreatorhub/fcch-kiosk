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
wget https://www.fortcollinscreatorhub.org/rpi-packages/fcch-kiosk_6_all.deb
sudo apt install ./fcch-kiosk_6_all.deb
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

# Overscan compensation

There are 3 different time periods and places to account for display rotation:

1) During early Linux boot, before the main display driver is loaded.

This can be controlled via the following options in `/boot/config.txt`.
However, they don't seem to work, at least when display rotation is enabled:

```
disable_overscan=0
overscan_top=-32
overscan_bottom=-32
overscan_left=-32
overscan_right=-32
```

Note that these overscan values are not the same units as the values described
in the next section. I'm not sure what the units are.

2) During Linux console text display.

This can be controlled by editing `/boot/cmdline.txt` to add the following
option to the end of the command-line:

```
video=HDMI-A-1:D,margin_left=32,margin_right=32,margin_top=32,margin_bottom=32
```

Edit the margin values as appropriate for your display. These units are
probably physical display pixels.

3) During execution of the fcch-kiosk application.

This configuration automatically follows the margin values specified in
`/boot/cmdline.txt`.

# Display rotation

There are 3 different time periods and places to account for display rotation:

1) During early Linux boot, before the main display driver is loaded.

This can be controlled editing `/boot/config.txt` to add option
`display_rotate`. However, the firmware appears to parse `/boot/cmdline.txt`
and automatically adapt, so editing `/boot/config.txt` is not necessary.

2) During Linux console text display.

This can be controlled by editing `/boot/cmdline.txt` to add the following
option to the end of the command-line:

No rotation (of the physical display device):
```
fbcon=rotate:0
```

Rotation 90 CCW / 270 CW:
```
fbcon=rotate:1
```

Rotation 180 CCW / 180 CW:
```
fbcon=rotate:2
```

Rotation 270 CCW / 90 CW:
```
fbcon=rotate:3
```

3) During execution of the fcch-kiosk application.

This configuration automatically follows the rotation value specified in
`/boot/cmdline.txt`, or whatever FB rotation is applied to VT7 when the
application starts.
