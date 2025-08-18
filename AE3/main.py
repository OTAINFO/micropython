# OTAinfo, Inc - By: Akshay - Mon Aug 11 2025

from wifi.wifi_connection import wifi_connect
from otainfo_apis import apicall
import asyncio
import time


con = wifi_connect('', '')
con.connect()
while not con.wlan.isconnected():
    time.sleep(1)


nobj =  {  'url' : 'https://otainfo.us:9001/',
            'url_port' : '9001',
            'protocol' : 'https',
            'header' :{"Content-Type": "application/json"},
            'status' : '',
            'method' : 'POST',
            'uri' : '<sfid>/api-token-auth/',
            'payload' : '{"username" : "", "password" : ""}',
            'response' : '',
            'certificate' : '',
            'retries' : ''
            }

api_req = apicall.api_request(nobj)
#api_req.make_post_call()
asyncio.run(api_req.make_post_call())


