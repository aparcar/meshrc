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

run_command() {
    echo "run command $1"
    if [[ "$nodes" == "" ]]
        echo "$@" > "/var/run/bmx7/sms/sendSms/${1}"
        bmx7_add_sms_entry "${1}"
    else
        for node_id in $node_ids; do
            echo "$@" > "/var/run/bmx7/sms/sendSms/${1}_${node_id}"
            bmx7_add_sms_entry "${1}_${node_id}"
        done
    fi
}

usage() {
    cat << EOF
Usage: $0 

    -h --help                           : show this message
    -i --id <shortid>                   : short id of node to be configured
    -l --list-nodes                     : show all nodes of mesh network
    -n --node-name <name>               : sets node name for given shortId
    -a --ap-pass <passworkd>            : set access point password of all nodes
    -m --mesh-pass <passworkd>          : set mesh password of all nodes
    -f --firstboot                      : resets all nodes by removing overlayfs
    -r --raw                            : runs given command directly on node
    --add-ssh <ssh_key>                 : add ssh key to all nodes
    --del-ssh <ssh_key>                 : remove ssh key to all nodes

Examples:

    $0 -i ABCD1234 -a "individual-ap-password"
    $0 -i ABCD1234 -i BCDE2345 -r "reboot"
    $0 -m "new-mesh-password"
EOF
}

node_ids=""

while [ "$#" ]; do
    case $1 in
        -h|--help)
            usage
            shift
            ;;
        -i|--id)
            node_ids+=" $2"
            shift; shift
        -n|--node-name)
            run_command "hn" "$2"
            shift; shift
            ;;
        -a|--ap-pass)
            run_command "ap" "$2"
            shift; shift
            ;;
        -m|--mesh-pass)
            run_command "mesh" "$2"
            shift; shift
            ;;
        -l|--list-nodes)
            bmx7 -c originators | tail -n +3 | awk '{ print $1" "$2 }'
            shift
            ;;
        -f|--firstboot)
            reset_network
            shift
            ;;
        -r|--raw)
            run_command "raw" "$2"
            shift; shift
        --add-ssh)
            run_command "as" "$2"
            shift; shift
        --del-ssh)
            run_command "ds" "$2"
            shift; shift
        *)
            break
        ;;
    esac
done
