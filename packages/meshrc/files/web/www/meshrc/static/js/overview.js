// draws table based on NetJson
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
        var properties = node.properties
        var button = document.createElement("a")
        button.href = "#node" + node.id
        button.classList.add("btn")
        button.style.width = "100%"
        button.innerHTML = node.label

        // change class based on load
        if (properties.node_state == "down") {
            button.classList.add("btn-danger")
            button.href = ""
        } else if (properties.node_state == "up-mload") {
            button.classList.add("btn-warning")
        } else {
            button.classList.add("btn-success")
        }

        tr.insertCell().appendChild(button);
        for (var property in properties_active) {
            var td = tr.insertCell();
            if (!properties_active[property][1]) {
                var value = fmt_default(properties[property])
            } else {
                var value = properties_active[property][1](properties[property])
            }
            td.appendChild(document.createTextNode(value));
        }
    }
}
