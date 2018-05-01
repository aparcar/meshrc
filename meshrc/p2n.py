import json
import requests
import time
import datetime
import http.server
import socketserver

class PromNetJson(http.server.SimpleHTTPRequestHandler):
    def init_config(self):
        self.LABEL = "Test Network"
        self.VERSION = "0.1"
        self.METRIC = "rxRate"
        self.PROMETHEUS_HOST = "http://localhost:9090"

    def timer_start(self):
        self.time_start = time.time()

    def timer_end(self, task):
        print("{} in {:.3f}ms".format(task,
            (time.time() - self.time_start) * 1000))

    def init_netjsongraph(self):
        self.init_config()
        self.njg = {}
        self.njg["type"] = "NetworkGraph"
        self.njg["label"] = self.LABEL
        self.njg["protocol"] = "BMX7"
        self.njg["version"] = self.VERSION
        self.njg["metric"] = self.METRIC
        self.njg_nodes = {}
        self.njg_links = {}

    def merge_links(self, links):
        self.timer_start()
        online_links = set()
        for link in links:
            # sort to save bidirectional links only once
            n1, n2 = sorted([link["source"], link["target"]])
            online_links.add(n1)

            if not n1 in self.njg_nodes or not n2 in self.njg_nodes:
                print("{} or {} not in njg_nodes".format(n1, n2))
                continue

            if not n1 in self.njg_links:
                self.njg_links[n1] = {}

            if not n2 in self.njg_links[n1]:
                self.njg_links[n1][n2] = {}

            self.njg_links[n1][n2]["source"] = n1
            self.njg_links[n1][n2]["target"] = n2

            if not "properties" in self.njg_links[n1][n2]:
                self.njg_links[n1][n2]["properties"] = {}

            if not "devs" in self.njg_links[n1][n2]["properties"]:
                self.njg_links[n1][n2]["properties"]["devs"] = {}
            self.njg_links[n1][n2]["properties"]["devs"][link["dev"]] = \
                    link["rxRate"]
            if not "rate" in self.njg_links[n1][n2]["properties"]:
                self.njg_links[n1][n2]["properties"]["rate"] = 0
            rx_rate = int(link["rxRate"])
            if rx_rate > self.njg_links[n1][n2]["properties"]["rate"]:
                self.njg_links[n1][n2]["properties"]["rate"] = rx_rate
                if rx_rate > 9.9 * 10 ** 8: best_rate = "over1Gbit"
                elif rx_rate > 9.9 * 10 ** 7: best_rate = "over100Mbit"
                elif rx_rate > 4.9 * 10 ** 6: best_rate = "over50Mbit"
                elif rx_rate > 9.9 * 10 ** 6: best_rate = "over10Mbit"
                elif rx_rate > 4.9 * 10 ** 2: best_rate = "over5Mbit"
                else: best_rate = "under5Mbit"
                self.njg_links[n1][n2]["properties"]["best_rate"] = best_rate

        self.timer_end("merged links")
        self.timer_start()

        njg_links_set = set(self.njg_links.keys())
        for offline_link in (njg_links_set - online_links):
            del self.njg_links[offline_link]

        self.timer_end("removed offline links")

    def api_call(self, query):
        print(query)
        try:
            response = requests.get("{}/api/v1/query?query={}&time={}".format(
            self.PROMETHEUS_HOST, query, self.timestamp)).json()["data"]["result"]
        except:
            response = []
        return response

    def api_call_propertie(self, query, propertie, label=None, multi=False):
        for v in self.api_call(query):
            shortId = v["metric"]["shortId"]
            if shortId in self.njg_nodes:
                if label:
                    value = v["metric"][label]
                else:
                    value = v["value"][1]
                if not multi:
                    self.njg_nodes[shortId]["properties"][propertie] = value
                else:
                    if not propertie in self.njg_nodes[shortId]["properties"]:
                        self.njg_nodes[shortId]["properties"][propertie] = []
                    self.njg_nodes[shortId]["properties"][propertie] \
                            .append(value)

    def get_nodes_bmx7(self):
        self.timer_start()
        for v in self.api_call("up{job='mesh'}"):
            self.njg_nodes[v["metric"]["shortId"]] = {}
            self.njg_nodes[v["metric"]["shortId"]]["id"] = \
                    v["metric"]["shortId"]
            if "hostname" in v["metric"]:
                self.njg_nodes[v["metric"]["shortId"]]["label"] = \
                        v["metric"]["hostname"]
            else:
                self.njg_nodes[v["metric"]["shortId"]]["label"] = \
                        v["metric"]["shortId"]
            self.njg_nodes[v["metric"]["shortId"]]["properties"] = {}
            if v["value"][1] == "1":
                self.njg_nodes[v["metric"]["shortId"]]["properties"] \
                        ["node_state"] = "up"
            else:
                self.njg_nodes[v["metric"]["shortId"]]["properties"] \
                        ["node_state"] = "down"

        self.api_call_propertie(
            "sum(node_network_transmit_bytes{device=~'wlan.*mesh'}) by (shortId)",
                "traffic_mesh")
        self.api_call_propertie(
            "sum(node_network_transmit_bytes{device=~'wlan.*ap'}) by (shortId)",
                "traffic_ap")
        self.api_call_propertie(
                "node_time - node_boot_time",
                "uptime")
        self.api_call_propertie(
                "node_load15",
                "load")
        self.api_call_propertie("bmx7_tunIn", "tunIn", "network", True)
        self.api_call_propertie(
                "100* (node_memory_MemFree / node_memory_MemTotal)", "memory")
        #self.api_call_propertie(
        #        "count(wifi_station_signal{ifname=~'wlan.*-ap.*'}) by (shortId)",
        #        "clients")
        self.timer_end("get nodes prometheus")

        # mark gateways
        for node in self.njg_nodes.values():
            if node["properties"]["node_state"] == "up":
                if "tunIn" in node["properties"]:
                    if "0.0.0.0/0" in node["properties"]["tunIn"]:
                        node["properties"]["node_state"] = "up-gateway"
                node_load = float(node["properties"]["load"])
                if node_load > 2:
                    if node["properties"]["node_state"] == "up-gateway":
                        node["properties"]["node_state"] = "up-hload-gateway"
                    else:
                        node["properties"]["node_state"] = "up-hload"
                elif node_load > 1:
                    if node["properties"]["node_state"] == "up-gateway":
                        node["properties"]["node_state"] = "up-mload-gateway"
                    else:
                        node["properties"]["node_state"] = "up-mload"

        return self.njg_nodes

    def get_links_bmx7(self):
        self.timer_start()
        links = []
        for link in self.api_call("bmx7_link_rxRate{job='mesh'}"):
            metric = link["metric"]
            value = link["value"][1]
            metric["rxRate"] = value
            links.append(metric)

        self.timer_end("get links prometheus")
        self.merge_links(links)

    def write_json(self, dest="netjson.json"):
        with open(dest, "w") as netjson_dest:
            netjson_dest.write(json.dumps(self.njg_out))

    def print_json(self):
        print(json.dumps(self.njg_out, indent="  "))

    def get_hostname(self, node_id):
        return self.api_call("bmx7_status{id='" + node_id + "'}")[0] \
                ["metric"]["hostname"]

    def dump_json(self):
        self.timer_start()

        self.njg_out = self.njg

        self.njg_out["nodes"] = []
        for node in self.njg_nodes.values():
            self.njg_out["nodes"].append(node)

        self.njg_out["links"] = []
        for source in self.njg_links:
            for target in self.njg_links[source]:
                self.njg_out["links"].append(self.njg_links[source][target])

        self.timer_end("dump json")
        return self.njg_out

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        if "timestamp=" in self.path:
            timestamp = self.path.split("timestamp=")[1]
        else:
            timestamp = ""
        self.wfile.write(bytes(json.dumps(self.get_bmx7(timestamp)), "utf-8"))
        return

    def get_bmx7(self, timestamp=None):
        if timestamp and timestamp != "undefined":
            value = int(timestamp[0:-1])
            suffix = timestamp[-1]
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
                    seconds=seconds, minutes=minutes, hours=hours, 
                    days=days, weeks=weeks)
            self.timestamp = delta.timestamp()
            print("timestamp is", self.timestamp, "xxx")
        else:
            self.timestamp = ""
        self.init_netjsongraph()
        self.get_nodes_bmx7()
        self.get_links_bmx7()
        return self.dump_json()


if __name__ == '__main__':
    print('Server listening on port 8899..')
    httpd = socketserver.TCPServer(('', 8899), PromNetJson)
    httpd.serve_forever()
