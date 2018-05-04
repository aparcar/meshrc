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
    var result = null,
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
    console.log("callback")
    if (data.result == 6) {
        alert("Wrong password!")
    } else {
        authed = true
        ubus_rpc_session = data.result[1].ubus_rpc_session
        set_url_param("ubus-session", ubus_rpc_session)
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
    console.log("reload_func " + func)
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

ubus_rpc_session = get_url_param("ubus-session")
if (!ubus_rpc_session) {
    show("#login")
} else {
    hide("#login")
    authed = true
    navi()
}
