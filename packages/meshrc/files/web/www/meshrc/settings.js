netjson_url = "/ubus"
netjson_url = "http://localhost:8080/cgi-bin/netjson"

properties_active = {
    "load": ["Load", false],
    "memory": ["Free memory", fmt_percent],
    "traffic_mesh": ["Traffic Mesh", fmt_filesize],
    "traffic_ap": ["Traffic AP", fmt_filesize],
    "uptime": ["Uptime", fmt_duration]
}
