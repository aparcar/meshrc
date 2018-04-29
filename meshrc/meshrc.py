import subprocess
from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash, jsonify

from .prometheus_2_netjson import PromNetJson

app = Flask(__name__)
app.config.from_object(__name__)

p2nj = PromNetJson()

@app.route("/")
@app.route("/graph")
def graph():
    bmx = request.args.get("bmx", "7")
    return render_template("graph.html", bmx=bmx)

@app.route("/netjson")
def grap_json():
    bmx = request.args.get("bmx", "7")
    time = request.args.get('time', "")
    timestamp=""
    if time != "":
        if time[0] == "-":
            value = int(time[1:-1])
            suffix = time[-1]
            seconds = 0
            minutes = 0
            hours = 0
            days = 0
            weeks = 0
            if suffix == "s":
                seconds = value
            elif suffix == "m":
                minutes = value
            elif suffix == "h":
                hours = value
            elif suffix == "d":
                days = value
            elif suffix == "w":
                weeks = value
            delta = datetime.datetime.now() - datetime.timedelta(
                    seconds=seconds, minutes=minutes, hours=hours, days=days,
                    weeks=weeks)
            timestamp = delta.timestamp()

    # this enables very simple caching
    current_time = int(datetime.now().strftime("%s"))
    if not hasattr(g, 'last_sync'):
        g.last_sync = current_time
    if not hasattr(g, 'netjson') or g.last_sync + 5*60 > current_time:
        g.netjson = jsonify(p2nj.get_bmx7(timestamp))
    return g.netjson

@app.route("/overview")
def overview():
    return render_template("overview.html",
            nodes=p2nj.get_nodes_bmx7())

@app.route("/config", methods=['GET', 'POST'])
def config():
    if request.method == 'GET':
        return render_template("config.html")
    else:
        config_data = request.form.to_dict()
        cmd = ""
        if mesh_data["ap_psk"]:
            flash("New access point password set")
            cmd += " -a {}".format(mesh_data["ap_psk"])
        if node_data["mesh_psk"]:
            flash("Rename {} to {}".format(mesh_data["mesh_psk"]))
            cmd += " -m {}".format(mesh_data["mesh_psk"])

        print("running {}".format(cmd))
        if os.system(cmd):
            return redirect("/")
        else:
            return 500

@app.route("/config/<node_id>", methods=['GET', 'POST'])
def config_node(node_id):
    hostname=p2nj.get_hostname(node_id)
    if request.method == 'GET':
        return render_template("config_node.html",
                hostname=hostname, node_id=node_id)
    else:
        node_data = request.form.to_dict()
        cmd="/usr/bin/meshrc-cli"
        if node_data["ap_psk"]:
            flash("New password for node".format(node_id, node_data["ap_psk"]))
            cmd += " -p {} {}".format(node_id, node_data["ap_psk"])
        if node_data["hostname"] != hostname:
            flash("Rename {} to {}".format(node_id, node_data["hostname"]))
            cmd += " -h {} {}".format(node_id, node_data["hostname"])

        print("running {}".format(cmd))
        if os.system(cmd):
            return redirect("/")
        else:
            return 500
