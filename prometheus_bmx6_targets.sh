#!/bin/sh

# adds all bmx6 originators to hosts directory
bmx6 -c originators | tail -n +3 | awk '{ print $3" "$1 }' >> /tmp/hosts/bmx6_originators

# make dnsmasq reread the host file
/etc/init.d/dnsmasq reload

# create new prometheus targets_bmx6 file
cat /tmp/hosts/bmx6_originators | awk '{ print "  - "$2":9100" }' > /tmp/targets_bmx6.yml.tmp
cat /var/targets_bmx6.yml | tail -n +2 >> /var/targets_bmx6.yml.tmp
echo "- targets:" > /tmp/targets_bmx6.yml
cat /var/targets_bmx6.yml.tmp | sort | uniq >> /var/targets_bmx6.yml
cp /var/targets_bmx6.yml /var/targets_bmx6.yml.tmp
