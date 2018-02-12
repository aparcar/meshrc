from flask import Flask
from flask import render_template, jsonify, request
from prometheus_2_netjson import PromNetJson

import datetime

app = Flask(__name__)

p2nj = PromNetJson()

@app.route("/")
def root():
    return "<h2>mesh-cc</h2>"

@app.route("/graph")
def graph():
    return render_template("graph.html")

@app.route("/graph-json")
def grap_json():
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
                    seconds=seconds, minutes=minutes, hours=hours, days=days, weeks=weeks)
            timestamp = delta.timestamp()

    return jsonify(p2nj.get_prometheus(timestamp))

@app.route("/overview")
def overview():
    return render_template("overview.html", nodes=p2nj.get_nodes_prometheus())



app.run()
