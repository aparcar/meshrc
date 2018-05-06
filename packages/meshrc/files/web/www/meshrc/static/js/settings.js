netjson_url = "/ubus"
netjson_url = "http://localhost:8111/cgi-bin/netjson"

ubus_url = "http://localhost:8111/ubus"
ubus_counter = 1

properties_active = {
    "load": ["Load", false],
    "memory": ["Free memory", fmt_percent],
    "traffic_mesh": ["Traffic Mesh", fmt_filesize],
    "traffic_ap": ["Traffic AP", fmt_filesize],
    "clients": ["Clients", fmt_default],
    "uptime": ["Uptime", fmt_duration],
    "model": ["Device", fmt_default]
}
