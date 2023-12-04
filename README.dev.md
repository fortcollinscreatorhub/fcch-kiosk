# Development

On an x86 Linux PC (e.g. running Ubuntu 22.04):

```shell
cd fcch-kiosk/
dpkg-buildpackage -us -uc && \
    scp ../fcch-kiosk_4_all.deb fcch@192.168.63.192:/tmp && \
    ssh fcch@192.168.63.192 sudo dpkg -i /tmp/fcch-kiosk_4_all.deb
```

Once testing is comlete, upload the package to our website, for easy access
from Pis during setup:

```shell
scp ../fcch-kiosk_4_all.deb fcch-web:/home/u930-v2vbn3xb6dhb/www/fortcollinscreatorhub.org/public_html/rpi-packages
```
