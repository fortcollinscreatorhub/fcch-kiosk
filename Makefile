# Copyright 2023 Stephen Warren <swarren@wwwdotorg.org>
# SPDX-License-Identifier: MIT

.PHONY: default
default: build

.PHONY: build
build:

.PHONY: install
install:
	install -D -d $(DESTDIR)/opt/fcch/kiosk/
	install -D -d $(DESTDIR)/opt/fcch/kiosk/bin/
	install -m 755 fcch-kiosk.display.sh $(DESTDIR)/opt/fcch/kiosk/bin/
	install -m 755 fcch-kiosk.display.py $(DESTDIR)/opt/fcch/kiosk/bin/
	install -m 755 fcch-kiosk.display-stop.sh $(DESTDIR)/opt/fcch/kiosk/bin/
	install -m 755 fcch-kiosk.web.sh $(DESTDIR)/opt/fcch/kiosk/bin/
	install -m 755 fcch-kiosk.web.py $(DESTDIR)/opt/fcch/kiosk/bin/
	install -D -d $(DESTDIR)/opt/fcch/kiosk/var/
	install -m 644 var/urls.txt $(DESTDIR)/opt/fcch/kiosk/var/
	install -D -d $(DESTDIR)/opt/fcch/kiosk/web/
	install -m 644 web/index.html $(DESTDIR)/opt/fcch/kiosk/web/
	install -m 644 web/main.js $(DESTDIR)/opt/fcch/kiosk/web/
	# Must be in /lib not /opt/fcch/kiosk/lib for some reason?
	install -D -d $(DESTDIR)/lib/systemd/system/
	install -m 644 fcch-kiosk.display.service $(DESTDIR)/lib/systemd/system/
	install -m 644 fcch-kiosk.web.service $(DESTDIR)/lib/systemd/system/
