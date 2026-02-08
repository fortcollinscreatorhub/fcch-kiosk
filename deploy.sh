#!/bin/bash

set -ex

ips=()
ips+=(10.1.11.20) # Front office
ips+=(10.1.11.21) # LASERS
ips+=(10.1.12.20) # Unit 12
ips+=(10.1.14.22) # 3D printing
ips+=(10.1.15.20) # Unit 15

deb=fcch-kiosk_7_all.deb

for ip in "${ips[@]}"; do
    scp "../${deb}" "fcch@${ip}:/tmp"
    ssh "fcch@${ip}" sudo dpkg -i "/tmp/${deb}"
    ssh "fcch@${ip}" sudo reboot
done
