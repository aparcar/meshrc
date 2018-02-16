#!/bin/sh

# adds all bmx7 originators to hosts directory
bmx7 -c originators | tail -n +3 | awk '{ print $13" "$2 }' >> /tmp/hosts/bmx7_originators

# make dnsmasq reread the host file
/etc/init.d/dnsmasq reload

# create new prometheus targets_bmx7 file
echo "- targets:" > /tmp/targets_bmx7.yml.tmp
cat /tmp/hosts/bmx_originators | awk '{ print "  - "$2":9100" }' | sort >> /tmp/targets_bmx7.yml.tmp

# only overwrite targets_bmx7 if it actually change
if [[ "$(sha256sum /var/targets_bmx7.yml.tmp | cut -c -32)" != "$(sha256sum /var/targets_bmx7.yml | cut -c -32)" ]]; then
        # this is done to not lose any offline nodes
        cat /var/targets_bmx7.yml >> /var/targets_bmx7.yml.tmp
        cat /var/targets_bmx7.yml.tmp | sort | uniq > /var/targets_bmx7.yml
        cp /var/targets_bmx7.yml.tmp /var/targets_bmx7.yml
        echo "updated"
fi
