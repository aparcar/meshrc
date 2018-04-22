#!/bin/sh

CONFIG="config.tar.gz"
CONFIG_DIR="/var/lib/config/"

[[ -d "$CONFIG_DIR" ]] || mkdir "$CONFIG_DIR"

while true; do
    tar c -z -C "$CONFIG_DIR" -f "/www/config/${CONFIG}"
    inotifywait -e create -e delete -e modify "$CONFIG_DIR" || sleep 10
done
