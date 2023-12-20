# Copyright 2023 Stephen Warren <swarren@wwwdotorg.org>
# SPDX-License-Identifier: MIT

.PHONY: default
default: build

.PHONY: build
build:

.PHONY: install
install:
	# Must be in /lib not /opt/fcch/kiosk/lib for some reason?
	install -D -d $(DESTDIR)/lib/systemd/system/
	install -m 644 lib/systemd/system/fcch-kiosk.display.service $(DESTDIR)/lib/systemd/system/
	install -m 644 lib/systemd/system/fcch-kiosk.web.service $(DESTDIR)/lib/systemd/system/
	install -D -d $(DESTDIR)/opt/fcch/kiosk/
	install -D -d $(DESTDIR)/opt/fcch/kiosk/bin/
	install -m 755 bin/fcch-kiosk.display.sh $(DESTDIR)/opt/fcch/kiosk/bin/
	install -m 755 bin/fcch-kiosk.display.py $(DESTDIR)/opt/fcch/kiosk/bin/
	install -m 755 bin/fcch-kiosk.display-stop.sh $(DESTDIR)/opt/fcch/kiosk/bin/
	install -m 755 bin/fcch-kiosk.web.sh $(DESTDIR)/opt/fcch/kiosk/bin/
	install -m 755 bin/fcch-kiosk.web.py $(DESTDIR)/opt/fcch/kiosk/bin/
	install -D -d $(DESTDIR)/opt/fcch/kiosk/var/
	install -m 644 var/urls.txt $(DESTDIR)/opt/fcch/kiosk/var/
	install -D -d $(DESTDIR)/opt/fcch/kiosk/web/static/
	install -m 644 web/static/main.js $(DESTDIR)/opt/fcch/kiosk/web/static
	install -D -d $(DESTDIR)/opt/fcch/kiosk/web/templates/
	install -m 644 web/templates/index.html $(DESTDIR)/opt/fcch/kiosk/web/templates/
	install -D -d $(DESTDIR)/opt/fcch/kiosk/lib/python/
	install -m 644 lib/python/fcchkiosk.py $(DESTDIR)/opt/fcch/kiosk/lib/python/
