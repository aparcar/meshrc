import json
import requests
import time

class PromNetJson():
    def __init__(self):
        print("init")
        self.init_config()
        self.init_netjsongraph()

    def init_config(self):
        self.BMX_VERSION = "7"
        self.FILES_PATH = "./qmp"
        self.LABEL = "Prometheus 2 NetJson"
        self.PROTOCOL = "bmx" + self.BMX_VERSION
        self.VERSION = "0.1"
        self.METRIC = "rxRate"
        self.PROMETHEUS_HOST = "http://localhost:9090"
    
    def timer_start(self):
        self.time_start = time.time()

    def timer_end(self, task):
        print("{} in {:.3f}ms".format(task, (time.time() - self.time_start) * 1000) )

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
            self.njg_links[n1][n2]["properties"]["devs"][link["dev"]] = link["rxRate"]

        self.timer_end("merged links")
        self.timer_start()

        njg_links_set = set(self.njg_links.keys())
        for offline_link in (njg_links_set - online_links):
            del self.njg_links[offline_link]

        self.timer_end("removed offline links")

        self.dump_json(print_output=True)

    def get_nodes_prometheus(self):
        self.timer_start()
        request_url = "{}/api/v1/query?query=bmx7_status".format(
                self.PROMETHEUS_HOST)
        response = requests.get(request_url).json()
        if response["status"] == "success":
            for node in response["data"]["result"]:
                node = node["metric"]
                self.njg_nodes[node["id"]] = {}
                self.njg_nodes[node["id"]]["id"] = node["id"]
                self.njg_nodes[node["id"]]["label"] = node["name"]
                self.njg_nodes[node["id"]]["properties"] = {}
                self.njg_nodes[node["id"]]["properties"]["address"] = node["address"]
                self.njg_nodes[node["id"]]["properties"]["revision"] = node["revision"]

        self.timer_end("get nodes prometheus")

    def get_links_prometheus(self):
        self.timer_start()
        request_url = "{}/api/v1/query?query=bmx7_link_rxRate".format(
                self.PROMETHEUS_HOST)
        response = requests.get(request_url).json()
        links = [] 
        if response["status"] == "success":
            for link in response["data"]["result"]:
                metric = link["metric"]
                value = link["value"][1]
                metric["rxRate"] = value
                links.append(metric)

        self.timer_end("get links prometheus")
        self.merge_links(links)

    def dump_json(self, dest="netjson.json", print_output=False):
        self.timer_start()

        njg_out = self.njg

        njg_out["nodes"] = []
        for node in self.njg_nodes.values():
            njg_out["nodes"].append(node)

        njg_out["links"] = []
        for source in self.njg_links:
            for target in self.njg_links[source]:
                njg_out["links"].append(self.njg_links[source][target])

        if print_output:
            print("dumped {}:".format(dest))
            print(json.dumps(njg_out, indent="  "))
            
        with open(dest, "w") as netjson_dest:
            netjson_dest.write(json.dumps(njg_out))
        self.timer_end("dump json")

if __name__ == '__main__':
    s = PromNetJson()
    s.get_nodes_prometheus()
    s.get_links_prometheus()
