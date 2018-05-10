function $(s) {
    return document.getElementById(s.substring(1));
}

function show(s) {
    console.log("show " + s)
    $(s).style.display = 'block';
}

function hide(s) {
    console.log("hide " + s)
    $(s).style.display = 'none';
}

// from https://stackoverflow.com/a/487049/8309585
function set_url_param(key, value) {
    key = encodeURI(key);
    value = encodeURI(value);

    var kvp = document.location.search.substr(1).split('&');

    var i = kvp.length;
    var x;
    while (i--) {
        x = kvp[i].split('=');

        if (x[0] == key) {
            x[1] = value;
            kvp[i] = x.join('=');
            break;
        }
    }

    if (i < 0) {
        kvp[kvp.length] = [key, value].join('=');
    }

    //this will reload the page, it's likely better to store this until finished
    document.location.search = kvp.join('&');
}

// from https://stackoverflow.com/a/5448595/8309585
function get_url_param(parameterName) {
    var result = "",
        tmp = [];
    location.search.substr(1).split("&").forEach(function(item) {
        tmp = item.split("=");
        if (tmp[0] === parameterName) {
            result = decodeURIComponent(tmp[1]);
        }
    });
    return result;
}

function ubus_call(command, argument, params, callback) {
    console.log(command + " " + argument + " " + params + " " + callback)
    var request_data = {};
    request_data.jsonrpc = "2.0";
    request_data.id = ubus_counter;
    request_data.method = "call";
    request_data.params = [ubus_rpc_session, command, argument, params]
    console.log(JSON.stringify(request_data))
    fetch(ubus_url, {
            method: "POST",
            body: JSON.stringify(request_data)
        })
        .then(function(res) {
            return res.json();
        })
        .then(function(data) {
            if (typeof data["error"] == "undefined") {
                if (typeof callback != "undefined") {
                    callback(data);
                }
            } else {
                authed = 0;
                navi()
            }
        })
    ubus_counter++;
}

function apply_config(form) {
    console.log("apply config")
    var fe = $(form).elements
    for (var i = 0; i < fe.length; i++) {
        if (fe[i].value != "" && fe[i].name != "apply") {
            ubus_call("meshrc", fe[i].id, {
                "param": fe[i].value,
                "node_id": node_id
            }, debug_callback)
        }
    }
    set_url_param("node-id", "")
}

function firstboot() {
    console.log("reset network")
    var txt;
    var confirmation = confirm("Reset?");
    if (confirmation) {
        ubus_call("meshrc", "firstboot", {
            "node_id": node_id
        }, debug_callback)
    }
}

function ubus_login_callback(data) {
    console.log("callback")
    if (data.result == 6) {
        alert("Wrong password!")
    } else {
        authed = true
        ubus_rpc_session = data.result[1].ubus_rpc_session
        set_url_param("ubus-session", ubus_rpc_session)
    }
}

function ubus_login() {
    ubus_rpc_session = "00000000000000000000000000000000"
    ubus_call("session", "login", {
        "username": "root",
        "password": $("#login_password").value
    }, ubus_login_callback)
}

function reload_node() {
    console.log("reload config")
    ubus_call("meshrc", "get_hostname", {
        "node_id": node_id
    }, reload_node_callback)
}

function reload_node_callback(data) {
    var fe = $("#form_node").elements
    for (var i = 0; i < fe.length; i++) {
        fe[i].value = data.result[1][fe[i].id]
    }
}

function reload_config() {
    console.log("reload config")
    ubus_call("meshrc", "get_config", {}, reload_config_callback)
}

function reload_config_callback(data) {
    console.log(data.result[1])
    var fe = $("#form_config").elements
    for (var i = 0; i < fe.length; i++) {
        if(fe[i].type == "checkbox") {
            fe[i].checked = data.result[1][fe[i].id]
        } else {
            fe[i].value = data.result[1][fe[i].id]
        }
    }
}

function reload_netjson(timestamp_new) {
    ubus_call("meshrc", "netjson", {
        "timestamp": timestamp_new
    }, reload_netjson_callback)
    set_url_param("timestamp", timestamp_new)
}

function reload_netjson_callback(data) {
    netjson_data = data.result[1]
    func = "reload_" + window.location.hash.substring(1)
    console.log("reload_func " + func)
    window[func]()
}

function reload_debug() {
    $("#debug").innerHTML = "<pre>" + JSON.stringify(netjson_data, null, 4) + "</pre>"
}

function debug_callback(data) {
    console.log(data.result[1])
}

function navi() {
    hide("#debug")
    hide("#config")
    hide("#node")
    hide("#overview")
    hide("#graph")
    if (authed) {
        var hash = window.location.hash;
        if (hash.startsWith("#node")) {
            show("#node")
            node_id = hash.substring(5)
            reload_node()
        } else {
            node_id = ""
            if (hash == "" || hash == "#") {
                window.location.hash = "graph"
            } else {
                show(hash)
                reload_netjson(timestamp)
            }
        }
    } else {
        show("#login")
    }
}

ubus_rpc_session = get_url_param("ubus-session")
timestamp = get_url_param("timestamp") || ""
$("#time_relative").value = timestamp
authed = false

if (!ubus_rpc_session) {
    show("#login")
} else {
    hide("#login")
    authed = true
    navi()
}
