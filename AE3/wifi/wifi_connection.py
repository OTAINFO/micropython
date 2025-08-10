'''
   2025 (c) OTAinfo, Inc.

'''

import network
import time

class wifi_connect:

    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.connect_metric = {}
        self.metric = self.empty_wifi_metric()
        self.singlemetric = []
        print("Wifi Connection class")

    def connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        self.load_single_metric("connecting", self.ssid)
        print(f"Connecting to Wi-Fi network: {self.ssid}...")
        wlan.connect(self.ssid, self.password)
        connection_timeout = 20  # Timeout in seconds
        while not wlan.isconnected() and connection_timeout > 0:
            print(".", end="")
            time.sleep(1)
            connection_timeout -= 1
        delay = 20 - connection_timeout
        self.load_single_metric("conntection_delay", str(delay))
        if wlan.isconnected():
            print (f"Wifi Connected: {self.ssid}")
            self.load_single_metric("wifi_status", f"Connected to {self.ssid}")
        else:
            print (f"Wifi connection failed: {self.ssid}")
            self.load_single_metric("wifi_status", f"Failed to connect with {self.ssid}")
        print(self.singlemetric)

    def load_single_metric(self, key, metric):
        _smetric = self.empty_single_metric()
        _smetric['key'] = key
        _smetric['metric'] = metric
        self.singlemetric.append(_smetric)

    def empty_wifi_metric(self):
        return {"mac" : "", "wifi_mac" : "", "model" : "", "make" : "",  "singlemetric" : []}

    def empty_single_metric(self):
        return {"key" :"", "metric" : ""}


