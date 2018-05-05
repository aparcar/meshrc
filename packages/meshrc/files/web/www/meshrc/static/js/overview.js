function reload_overview() {
    console.log("table_content" + netjson_data)
    tbl = document.getElementById("table_overview")
    tbl.innerHTML = ""
    var header = tbl.createTHead();
    var header_row = header.insertRow(0);
    header_row.insertCell().innerHTML = "Hostname"
    for (var property in properties_active) {
        header_row.insertCell().innerHTML = properties_active[property][0]
    }

    var nodes = netjson_data.nodes

    for (node_index in nodes) {
        var node = nodes[node_index]
        var tr = tbl.insertRow();
        tr.insertCell().appendChild(document.createTextNode(node.label));
        var properties = node.properties
        if (properties.node_state == "down") {
            tr.classList.add("table-danger")
        } else if (properties.node_state == "up-mload") {
            tr.classList.add("table-warning")
        }
        for (var property in properties_active) {
            var td = tr.insertCell();
            if (!properties_active[property][1]) {
                var value = fmt_normal(properties[property])
            } else {
                var value = properties_active[property][1](properties[property])
            }
            td.appendChild(document.createTextNode(value));
        }
    }
}
