#!/bin/sh

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

bmx7_apply_changes() {
    uci commit bmx7
    /etc/init.d/bmx7 reload
}

reset_network() {
    read -p "confirm network reset [y/N]" -n 1 -r
    if [[ $REPLY == "Y" || $REPLY == "y" ]]
    then
        echo "send reset command to mesh network"
        touch /var/run/bmx7/sms/sendSms/reset
        bmx7_add_sms_entry reset
    else
        echo "reset canceled"
    fi
}

set_node_name() {
    echo "set node shortId ${1} to ${2}"
    echo "$2" > "/var/run/bmx7/sms/sendSms/hn_${1}"
    bmx7_add_sms_entry "hn_${1}"
}

set_node_ap_password() {
    echo "set access point password for shortId ${1}"
    echo "$2" > "/var/run/bmx7/sms/sendSms/ap_${1}"
    bmx7_add_sms_entry "ap_${1}"
}

set_ap_password() {
    echo "set access point password for all nodes"
    echo "$1" > "/var/run/bmx7/sms/sendSms/ap"
    bmx7_add_sms_entry "ap"
}

set_mesh_password() {
    echo "set mesh password for all nodes"
    echo "$1" > "/var/run/bmx7/sms/sendSms/mesh"
    bmx7_add_sms_entry "mesh"
}

usage() {
    cat << EOF
Usage: $0 

    -h --help                           : show this message
    -l --list-nodes                     : show all nodes of mesh network
    -n --node-name <shortId> <name>     : sets node name for given shortId
    -a --ap-pass <pass>                 : set access point password of all nodes
    -m --mesh-pass <pass>               : set mesh password of all nodes
    -p --node-ap-pass <shortId> <pass>  : set access point password of shortId
    -r --reset                          : resets all nodes by removing overlayfs
EOF
}

while [ "$#" ]; do
    case $1 in
        -h|--help)
            usage
            shift
            ;;
        -n|--node-name)
            set_node_name "$2" "$3"
            shift; shift; shift
            ;;
        -p|--node-ap-pass)
            set_node_ap_password "$2" "$3"
            shift; shift; shift
            ;;
        -a|--ap-pass)
            set_ap_password "$2"
            shift; shift
            ;;
        -m|--mesh-pass)
            set_mesh_password "$2"
            shift; shift
            ;;
        -l|--list-nodes)
            bmx7 -c originators | tail -n +3 | awk '{ print $1" "$2 }'
            shift
            ;;
        -r|--reset)
            reset_network
            shift
            ;;
        *)
            break
        ;;
    esac
done
