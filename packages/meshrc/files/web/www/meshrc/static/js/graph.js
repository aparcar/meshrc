function reload_graph() {
    d3.select("svg").remove(); // resets the graph
    d3.netJsonGraph(netjson_data, {
        el: "#graph",
        linkDistance: 150,
        charge: -200,
        circleRadius: 12,
        defaultStyle: false,
        linkClassProperty: "best_rate",
        nodeClassProperty: "node_state",
        gravity: 0.03,
        onClickNode: function(n) {
            var overlay = d3.select(".njg-overlay"),
                overlayInner = d3.select(".njg-overlay > .njg-inner"),
                html = "<p><b>Short ID</b>: " + n.id + "</p>";
            if (n.id) {
                if (n.label) {
                    html += "<p><b>Hostname</b>: <a href='#node" + n.id + "'>" + n.label + "</a></p>";
                }
            } else {
                if (n.label) {
                    html += "<p><b>Hostname</b>: " + n.label + "</p>";
                }
            }
            if (n.properties) {
                for (var property in properties_active) {
                    if (!properties_active[property][1]) {
                        var value = n.properties[property]
                    } else {
                        var value = properties_active[property][1](n.properties[property])
                    }
                    html += "<p><b>" + properties_active[property][0] + "</b>: " + value + "</p>";
                }
            }

            if (n.linkCount) {
                html += "<p><b>Link Count</b>: " + n.linkCount + "</p>";
            }
            if (n.local_addresses) {
                html += "<p><b>Local Addresses</b>:<br>" + n.local_addresses.join('<br>') + "</p>";
            }
            overlayInner.html(html);
            overlay.classed("njg-hidden", false);
            overlay.style("display", "block");
            removeOpenClass();
            d3.select(this).classed("njg-open", true);
        },
        onClickLink: function(l) {
            var overlay = d3.select(".njg-overlay"),
                overlayInner = d3.select(".njg-overlay > .njg-inner"),
                html = "<p><b>source</b>: " + (l.source.label || l.source.id) + "</p>";
            html += "<p><b>target</b>: " + (l.target.label || l.target.id) + "</p>";
            if (l.properties) {
                for (var key in l.properties) {
                    if (!l.properties.hasOwnProperty(key) || key == "devs" || key == "rate") {
                        continue;
                    }
                    html += "<p><b>" + key.replace(/_/g, " ") + "</b>: " + l.properties[key] + "</p>";
                }
            }
            html += "<b>devices:<b></br>"
            for (var dev in l.properties.devs) {
                html += "- " + dev + ": " + fmt_filesize(l.properties.devs[dev], "b/s") + "</br>";
            }
            overlayInner.html(html);
            overlay.classed("njg-hidden", false);
            overlay.style("display", "block");
            removeOpenClass();
            d3.select(this).classed("njg-open", true);
        },
    });
}
