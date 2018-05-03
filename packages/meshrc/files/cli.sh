#!/bin/sh

CONFIG="config.tar.gz"
CONFIG_DIR="/var/lib/config/"

bmx7_add_sms_entry() {
    bmx7 -c syncSms="${1}"
}

bmx7_del_sms_entry() {
    uci delete bmx7.${1}
}

bmx7_add_sms_file() {
    filename = "basename($1)"
    bmx7_add_sms_entry "${filename}"
    ln -s "$1" "/var/run/bmx7/sms/sendSms/${filename}"
}

bmx7_del_sms_file() {
    filename = "basename($1)"
    #bmx7_del_sms_entry "${filename}"
    rm "/var/run/bmx7/sms/sendSms/${filename}"
}

reset_network() {
    read -p "confirm network reset [y/N]" -n 1 -r
    if [[ $REPLY == "Y" || $REPLY == "y" ]]
    then
        echo "send reset command to mesh network"
        run_command "fb"
    else
        echo "reset canceled"
    fi
}

initial_config() {
    mkdir -p /var/lib/config/etc/config/
    mkdir -p /var/lib/config/etc/uci-defaults/
    ln -s /etc/config/lime-defaults /var/lib/config/etc/config/lime-defaults
    cat <<EOF > /var/lib/config/etc/uci-defaults/lime-defaults
#!/bin/sh

lime-config -d
lime-smart-wifi
lime-config
lime-apply
EOF
}

update_config() {
    tar c -z -C "$CONFIG_DIR" -f "/www/config/${CONFIG}"
}

run_command() {
    echo "run command $1"
    if [[ "$node_id" == "" ]]; then
        echo "$@" > "/var/run/bmx7/sms/sendSms/${1}"
        bmx7_add_sms_entry "${1}"
    else
        echo "$@" > "/var/run/bmx7/sms/sendSms/${1}_${node_id}"
        bmx7_add_sms_entry "${1}_${node_id}"
    fi
}

usage() {
    cat << EOF
Usage: $0 

    -h --help                           : show this message
    -i --shortid <shortid>              : short id of node to be configured
    -l --list-nodes                     : show all nodes of mesh network
    -n --node-name <name>               : sets node name for given shortId
    -a --ap-pass <passworkd>            : set access point password of all nodes
    -m --mesh-pass <passworkd>          : set mesh password of all nodes
    -f --firstboot                      : resets all nodes by removing overlayfs
    -r --raw                            : runs given command directly on node
    -s --set-ssh <ssh_keys>             : set ssh key to all nodes

Examples:

    $0 -i ABCD1234 -a "individual-ap-password"
    $0 -i ABCD1234 -i BCDE2345 -r "reboot"
    $0 -m "new-mesh-password"
EOF
}

node_id=""

while [ "$#" ]; do
    case $1 in
        -h|--help)
            usage
            shift
            ;;
        -l|--list-nodes)
            bmx7 -c originators | tail -n +3 | awk '{ print $1" "$2 }'
            shift
            ;;
        -n|--network-name)
            run_command "nn" "$2"
            shift; shift
            ;;
        -i|--shortid)
            node_id="$2"
            shift; shift
            ;;
        -n|--node-name)
            run_command "hn" "$2"
            shift; shift
            ;;
        -a|--ap-pass)
            run_command "ap" "$2"
            shift; shift
            ;;
        -d|--mesh-name)
            run_command "mn" "$2"
            shift; shift
            ;;
        -m|--mesh-pass)
            run_command "mp" "$2"
            shift; shift
            ;;
        -f|--firstboot)
            reset_network
            shift
            ;;
        -r|--raw)
            run_command "raw" "$2"
            shift; shift
            ;;
        -s|--set-ssh)
            run_command "ssh" "$2"
            shift; shift
            ;;
        *)
            break
        ;;
    esac
done
