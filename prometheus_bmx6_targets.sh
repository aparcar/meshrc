#!/bin/sh

# adds all bmx7 originators to hosts directory
bmx6 -c originators | tail -n +3 | awk '{ print $3" "$1 }' >> /tmp/hosts/bmx6_originators

# make dnsmasq reread the host file
/etc/init.d/dnsmasq reload

# create new prometheus targets file
echo "- targets:" > /tmp/targets.yml.tmp
cat /tmp/hosts/bmx6_originators | awk '{ print "  - "$2":9100" }' | sort >> /tmp/targets_bmx6.yml.tmp

# only overwrite targets if it actually change
if [[ "$(sha256sum /var/targets_bmx6.yml.tmp | cut -c -32)" != "$(sha256sum /var/targets_bmx6.yml | cut -c -32)" ]]; then
        # this is done to not lose any offline nodes
        cat /var/targets_bmx6.yml >> /var/targets_bmx6.yml.tmp
        cat /var/targets_bmx6.yml.tmp | sort | uniq > /var/targets_bmx6.yml
        cp /var/targets_bmx6.yml.tmp /var/targets_bmx6.yml
        echo "updated"
fi
