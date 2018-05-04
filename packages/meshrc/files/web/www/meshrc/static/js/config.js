authed = false
timestamp = ""

function $(s) {
    return document.getElementById(s.substring(1));
}

function show(s) {
    $(s).style.display = 'block';
}

function hide(s) {
    $(s).style.display = 'none';
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
            if (typeof callback != "undefined") {
                callback(data);
            }
        })
    ubus_counter++;
}

function debug_callback(string) {
    console.log(string)
}

function apply_config() {
    console.log("apply config")
    var fe = $("#form_config").elements
    for (var i = 0; i < fe.length; i++) {
        if (fe[i].value != "") {
            ubus_call("meshrc", fe[i].id, {
                "param": fe[i].value,
                "node_id": ""
            }, debug_callback)
        }
    }
}

function ubus_login_callback(data) {
    if (data.result == 6) {
        alert("Wrong password!")
    } else {
        authed = true
        ubus_rpc_session = data.result[1].ubus_rpc_session
        hide("#login")
        navi()
    }
}

function ubus_login() {
    ubus_rpc_session = "00000000000000000000000000000000"
    ubus_call("session", "login", {
        "username": "root",
        "password": $("#login_password").value
    }, ubus_login_callback)
}

function reload_config() {
    console.log("reload config")
}

function reload_netjson(timestamp_new) {
    timestamp = timestamp_new
    func = "reload_" + window.location.hash.substring(1)
    window[func]()
}

function navi() {
    hide("#config")
    hide("#overview")
    hide("#graph")
    d3.select("svg").remove(); // resets the graph
    if (typeof reload_overview_timeout != "undefined") {
        clearTimeout(reload_overview_timeout)
    }
    if (authed) {
        var hash = window.location.hash;
        if (hash != "" && hash != "#") {
            show(hash)
        } else {
            window.location.hash = "graph"
        }
        reload_netjson(timestamp)
    } else {
        show("#login")
    }
}
