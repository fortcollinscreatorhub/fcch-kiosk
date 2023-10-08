#!/bin/sh

# Copyright 2023 Stephen Warren <swarren@wwwdotorg.org>
# SPDX-License-Identifier: MIT

script_dir=$(dirname "$0")

exec "${script_dir}/fcch-kiosk.web.py" \
    --urls-file "${script_dir}/../var/urls.txt" \
    --control-pipe "${script_dir}/../var/control.pipe" \
    --web-dir "${script_dir}/../web"
