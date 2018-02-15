import json
import requests
import time

class PromNetJson():
    def __init__(self):
        print("init")
        self.init_config()
        self.init_netjsongraph()
        self.time = ""

    def init_config(self):
        self.BMX_VERSION = "7"
        self.FILES_PATH = "./qmp"
        self.LABEL = "Test Network"
        self.PROTOCOL = "bmx" + self.BMX_VERSION
        self.VERSION = "0.1"
        self.METRIC = "rxRate"
        self.PROMETHEUS_HOST = "http://localhost:9090"

    def timer_start(self):
        self.time_start = time.time()

    def timer_end(self, task):
        print("{} in {:.3f}ms".format(task,
            (time.time() - self.time_start) * 1000))

    def init_netjsongraph(self):
        self.njg = {}
        self.njg["type"] = "NetworkGraph"
        self.njg["label"] = self.LABEL
        self.njg["protocol"] = self.PROTOCOL
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
            self.njg_links[n1][n2]["properties"]["devs"]
                [link["dev"]] = link["rxRate"]

        self.timer_end("merged links")
        self.timer_start()

        njg_links_set = set(self.njg_links.keys())
        for offline_link in (njg_links_set - online_links):
            del self.njg_links[offline_link]

        self.timer_end("removed offline links")

    def api_call(self, query):
        return requests.get("{}/api/v1/query?query={}&time={}".format(
            self.PROMETHEUS_HOST, query, self.time)).json()["data"]["result"]

    def api_call_propertie(self, query, propertie):
        for v in self.api_call(query):
            instance = v["metric"]["instance"]
            if instance in self.njg_nodes:
                self.njg_nodes[instance]["properties"][propertie] = v["value"][1]

    def get_nodes_prometheus(self):
        self.timer_start()
        for v in self.api_call("up"):
            self.njg_nodes[v["metric"]["instance"]] = {}
            self.njg_nodes[v["metric"]["instance"]]
                ["label"] = v["metric"]["instance"]
            self.njg_nodes[v["metric"]["instance"]]
                ["properties"] = {}
            self.njg_nodes[v["metric"]["instance"]]
                ["properties"]["up"] = v["value"][1]

        for v in self.api_call("bmx7_status"):
            self.njg_nodes[v["metric"]["instance"]]
                ["id"] = v["metric"]["id"]
            self.njg_nodes[v["metric"]["instance"]]
                ["properties"]["address"] = v["metric"]["address"]

        self.api_call_propertie(
                "sum(node_network_receive_bytes{device=~'wlan.*mesh'}) by (instance)",
                "traffic_mesh")
        self.api_call_propertie(
                "sum(node_network_receive_bytes{device=~'wlan.*ap.*'}) by (instance)",
                "traffic_ap")
        self.api_call_propertie(
                "node_time - node_boot_time",
                "uptime")
        self.api_call_propertie(
                "node_load15",
                "load")
        self.api_call_propertie(
                "100* (node_memory_MemFree / node_memory_MemTotal)",
                "memory")
        self.api_call_propertie(
                "count(wifi_station_signal{ifname=~'wlan.*-ap.*'}) by (instance)",
                "clients")
        self.timer_end("get nodes prometheus")

        return self.njg_nodes

    def hms_string(self, sec_elapsed):
        h = int(int(sec_elapsed) / (60 * 60))
        m = int((int(sec_elapsed) % (60 * 60)) / 60)
        s = int(sec_elapsed) % 60
        return "{}:{:>02}:{:>02}".format(h, m, s)

    def get_links_prometheus(self):
        self.timer_start()
        for link in self.api_call("bmx7_link_rxRate"):
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

    def get_prometheus(self, time=""):
        self.time = time
        self.get_nodes_prometheus()
        self.get_links_prometheus()
        return self.dump_json()

if __name__ == '__main__':
    s = PromNetJson()
    s.get_nodes_prometheus()
    s.get_links_prometheus()
    s.dump_json()
    s.print_json()
