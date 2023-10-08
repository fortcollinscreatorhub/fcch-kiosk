# Development

On an x86 Linux PC (e.g. running Ubuntu 22.04):

```shell
cd fcch-kiosk/
dpkg-buildpackage -us -uc && \
    scp ../fcch-kiosk_1_all.deb  swarren@192.168.63.192:/tmp && \
    ssh swarren@192.168.63.192 sudo dpkg -i /tmp/fcch-kiosk_1_all.deb
```

Once testing is comlete, upload the package to
https://www.fortcollinscreatorhub.org/rpi-packages/fcch-kiosk_1_all.deb
.
