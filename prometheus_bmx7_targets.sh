#!/bin/sh

# touch targets_bmx7.json to make sure it exists
touch /tmp/targets_bmx7.json

cat /tmp/targets_bmx7.json | tail -n +2 | head -n -1 > /tmp/targets_bmx7.tmp
bmx7 -c originators | tail -n +3 | \
	awk '{ print "{ \"targets\": [ \"["$13"]:9100\" ],\"labels\": { \"shortId\": \""$1"\", \"hostname\": \""$2"\"}}," }' >> /tmp/targets_bmx7.tmp

# create new prometheus targets_bmx7 file
echo "[" > /tmp/targets_bmx7.json
cat /tmp/targets_bmx7.tmp | sort | uniq >> /tmp/targets_bmx7.json
echo "{} ]" >> /tmp/targets_bmx7.json

