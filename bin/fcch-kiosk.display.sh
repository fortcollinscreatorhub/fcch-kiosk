#!/bin/sh

# Copyright 2023 Stephen Warren <swarren@wwwdotorg.org>
# SPDX-License-Identifier: MIT

set -e

tty=/dev/tty0

disable_cursor_blink() {
    /bin/echo -ne "\033[?25l" > "${tty}"
}

enable_cursor_blink() {
    /bin/echo -ne "\033[?25h" > "${tty}"
}

clear_screen() {
    /bin/echo -ne "\033[2J" > "${tty}"
}

cursor_home() {
    /bin/echo -ne "\033[1;1H" > "${tty}"
}

cleanup() {
    set +e
    enable_cursor_blink
    #clear_screen
    #cursor_home
    chvt 1
    echo > "${tty}" # probably at a login prompt; this moves to next line
    echo "Kiosk display exited" > "${tty}"
}

script_dir=$(dirname "$0")
root_dir=$(realpath "${script_dir}/..")
trap cleanup EXIT
chvt 7
disable_cursor_blink

export QT_QPA_PLATFORM=linuxfb
export PYTHONPATH="${root_dir}/lib/python${PYTHONPATH:+:${PYTHONPATH}}"
# Don't exec, so the EXIT trap runs
"${script_dir}/fcch-kiosk.display.py" \
    --urls-file "${root_dir}/var/urls.txt" \
    --control-pipe "${root_dir}/var/control.pipe"
