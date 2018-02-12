from flask import Flask
from flask import render_template, jsonify
from prometheus_2_netjson import PromNetJson
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
    return jsonify(p2nj.get_prometheus())

@app.route("/overview")
def overview():
    return render_template("overview.html", nodes=p2nj.get_nodes_prometheus())



app.run()
