#!/bin/sh

# Copyright 2023 Stephen Warren <swarren@wwwdotorg.org>
# SPDX-License-Identifier: MIT

script_dir=$(realpath $(dirname "$0"))
root_dir=$(realpath "${script_dir}/..")

exec "${script_dir}/fcch-kiosk.web.py" \
    --urls-file "${root_dir}/var/urls.txt" \
    --control-pipe "${root_dir}/var/control.pipe" \
    --web-dir "${root_dir}/web"
