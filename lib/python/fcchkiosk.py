# Copyright 2023 Stephen Warren <swarren@wwwdotorg.org>
# SPDX-License-Identifier: MIT

import traceback
import subprocess

def bToS(b):
    try:
        s = b.decode('utf-8')
    except:
        traceback.print_exc(file=sys.stderr)
        s = ''
    s = s.strip()
    return s

def getStatusText():
    text = 'Status | IP '
    cp = subprocess.run(['nmcli', '-g', 'IP4.ADDRESS', 'device', 'show', 'wlan0'], capture_output=True)
    ip = bToS(cp.stdout)
    hasIp = bool(ip)
    if not ip:
        ip = '??'
    text += ip
    text += ' | http://'
    cp = subprocess.run(['hostname'], capture_output=True)
    text += bToS(cp.stdout)
    text += '.local/'
    return hasIp, text
