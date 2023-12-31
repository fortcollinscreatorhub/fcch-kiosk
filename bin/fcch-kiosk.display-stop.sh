#!/bin/sh

# Copyright 2023 Stephen Warren <swarren@wwwdotorg.org>
# SPDX-License-Identifier: MIT

script_dir=$(dirname "$0")
root_dir=$(realpath "${script_dir}/..")

echo -n Q > "${root_dir}/var/control.pipe"
while true; do
  pids=$(pidof -x fcch-kiosk.display.sh)
  if [ -z "${pids}" ]; then
    break
  fi
  sleep 1
done
