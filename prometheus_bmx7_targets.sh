#!/bin/sh

# adds all bmx7 originators to hosts directory
bmx7 -c originators | tail -n +3 | awk '{ print $13" "$2 }' > /tmp/hosts/bmx7_originators

# make dnsmasq reread the host file
/etc/init.d/dnsmasq reload

# create new prometheus targets_bmx7 file
cat /tmp/hosts/bmx7_originators | awk '{ print "  - "$2":9100" }' > /tmp/targets_bmx7.yml.tmp
cat /var/targets_bmx7.yml | tail -n +2 >> /var/targets_bmx7.yml.tmp
echo "- targets:" > /tmp/targets_bmx7.yml
cat /var/targets_bmx7.yml.tmp | sort | uniq >> /var/targets_bmx7.yml
cp /var/targets_bmx7.yml /var/targets_bmx7.yml.tmp
