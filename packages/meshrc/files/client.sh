#!/bin/sh

. /usr/share/libubox/jshn.sh

# loads trusted bmx7 ids from lime(-defaults)
trusted_ids=$(uci -q get lime-defaults.trusted_nodes.node_id)
[[ -z "$trusted_ids" ]]  && {
    trusted_ids=$(uci -q get lime.trusted_nodes.node_id)
    [[ -z "$trusted_ids" ]] && {
        uci -q set lime.trusted_nodes="trusted_nodes"
        uci -q set lime.trusted_nodes.node_id=""
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
                # change the lime-defaults file
                lime-defaults)
                    wait_cloud_synced "$config_file"
                    cp $config_path /etc/config/lime-defaults
                    lime-config --reset
                    lime-apply
                    ;;
                firstboot)
                    wait_cloud_synced "$config_file"
                    firstboot -y
                    ;;
                hn_${bmx7_shortid})
                    uci -q set lime.system.hostname="$(cat $config_path)"
                    lime-config
                    lime-apply
                    ;;
            esac
        done
    done

    # wait for received sms
    inotifywait -e delete -e create -e modify /var/run/bmx7/sms/rcvdSms
done
