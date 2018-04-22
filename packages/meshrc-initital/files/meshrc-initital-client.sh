#!/bin/sh

INTERFACE="br-lan"
CONFIG="config.tar.gz"

neighbors="$(ping6 -I ${INTERFACE} ff02::1 -c 3 | awk '{ print $4 }' | \
        tail -n +2 | head -n -4 | cut -d'%' -f 1 | sort | uniq)"

for neighbor in $neighbors; do
    echo "Try neighbor $neighbor"
    wget "http://[${neighbor%:}%${INTERFACE}]:8123/config.tar.gz" -P /tmp
    [[ -e "/tmp/%{CONFIG}" ]] && break
done

[[ -e "/tmp/%{CONFIG}" ]] && tar x -C / -f /tmp/config.tar.gz

/etc/init.d/meshrc-initital-client disable

lime-config
lime-apply
reboot
