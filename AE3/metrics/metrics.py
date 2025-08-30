# Untitled - By: Akshay - Tue Aug 26 2025
from config import config

class metrics:

    def __init__(self):
        print("Running Metric Class")

    def getemptymetric(self):
        return { "action" : "",
                 "attribute_name" : "",
                 "device_data" : "",
                 "device_id" : "",
                 "message" : "",
                 "metric_data" : "",
                 "metric_name" : "",
                 "motive" : "",
                 "outcome" : "",
                 "record_date" : "",
                 "status" : "",
                 "success" : 0
                 }

    def wifi_metric(self):
        st = config.st()
        _device_data = {}
        _device_data['device_id'] =st.getvalueifkeypresent('mac')
        _device_data['arch'] =st.getvalueifkeypresent('arch')
        _device_data['hw_version_str'] =st.getvalueifkeypresent('hw_version_str')
        _device_data['board_id'] =st.getvalueifkeypresent('board_id')
        _empty_metric = self.getemptymetric()
        _empty_metric["action"] = "Connecting to Wifi"
        _empty_metric["attribute_name"] = "WiFi_Connect"
        _empty_metric["motive"] = "Collect Pass/Fail"
        _empty_metric["record_date"] = 0
        _empty_metric["device_data"] = _device_data
        _empty_metric["device_id"] = _device_data['device_id']
        _empty_metric["metric_name"] = "wifi"
        _empty_metric["motive"] = "Establish Wifi Connection"
        #Update after the motive is complete: message, metric_data, outcome, record_date,
        #                                     status and success
        return _empty_metric


