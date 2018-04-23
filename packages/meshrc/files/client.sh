#!/bin/sh

. /usr/share/libubox/jshn.sh

# loads trusted bmx7 ids from lime(-defaults)
trusted_ids=$(uci -q get lime-defaults.meshrc.trusted)
[[ -z "$trusted_ids" ]]  && {
    trusted_ids=$(uci -q get lime.meshrc.trusted)
    [[ -z "$trusted_ids" ]] && {
        uci -q set lime.meshrc="lime"
        uci -q add_list lime.meshrc.trusted=""
        echo "please add section trusted_nodes in /etc/config/lime"
        exit 1
    }
}

# parses the own shortid and stores it in uci format
bmx7_shortid="$(uci -q get lime.system.bmx7_shortid)"
[[ -z "$bmx7_shortid" ]] && {
    json_load "$(cat /var/run/bmx7/json/status)"
    json_select status
    json_get_var bmx7_shortid shortId
    uci -q set lime.system.bmx7_shortid="$bmx7_shortid"
}

# add $1 to be synced as sms
bmx7_add_sms_entry() {
	bmx7 -c syncSms="${1}"
}

# return all node ids currently active in the network
active_nodes_ids() {
    return "$(ls -1 /var/run/bmx7/json/originators/ | sort)"
}

# return all node ids which acked the comment $1
acked_command() {
    return "$(ls /var/run/bmx7/sms/rcvdSms/*:${1}-ack | cut -d '/' -f 7 | \
            cut -d ':' -f 1 | sort)"
}

# sync cmd $1-ack to the cloud and wait until all other nodes acked it
wait_cloud_synced() {
    [[ -n $1 ]] || echo "missing argument" && return

    # create & share acked file
    touch "/var/run/bmx7/sms/sendSms/${1}-ack"
    bmx7_add_sms_entry "${1}-ack"

    # wait until cloud is synced
    while [[ active_node_ids != acked_command "$1" ]]; do
        sleep 5
    done
}

while true; do
    for trusted_id in $trusted_ids; do
        [[ -z "$trusted_id" ]] && return
        for config_path in ls /var/run/bmx7/sms/rcvdSms/${trusted_id}*; do
            config_file="$(basename $config_file | cut -d ':' -f 2)"
            case $config_file in
                # change the mesh password
                mesh)
                    uci -q set lime.wifi.ieee80211s_key="$(cat $config_path)"
                    wait_cloud_synced "$config_file"
                    ;;
                # change the ap password of all nodes
                ap)
                    uci -q set lime.wifi.ap_key="$(cat $config_path)"
                    wait_cloud_synced "$config_file"
                    ;;
                # resets everything
                firstboot)
                    wait_cloud_synced "$config_file"
                    firstboot -y
                    reboot
                    ;;
                # change the lime-defaults file
                lime-defaults)
                    wait_cloud_synced "$config_file"
                    cp $config_path /etc/config/lime-defaults

                    # remove everything except the given hostname
                    uci delete lime.wifi
                    uci delete lime.network
                    ;;
                # change hostname of single node
                hn_${bmx7_shortid})
                    uci -q set lime.system.hostname="$(cat $config_path)"
                    ;;
            esac
        done
    done
    uci commit lime
    lime-config
    lime-apply

    # wait for received sms
    inotifywait -e delete -e create -e modify /var/run/bmx7/sms/rcvdSms
done
