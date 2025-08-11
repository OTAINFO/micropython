# OTAinfo, Inc - By: Akshay - Mon Aug 11 2025

from wifi import wifi_connection
from otainfo_apis import apicall
import uasyncio as asyncio
import time


con = wifi_connection('', '')
con.connect()
while not con.wlan.isconnected():
    time.sleep(1)

nobj =  {  'url' : 'https://otainfo.us:9001/',
            'url_port' : '9001',
            'protocol' : 'https',
            'header' :{'Content-Type':'application/json'},
            'status' : '',
            'method' : 'POST',
            'uri' : 'api-token-auth/',
            'payload' : '{"username" : "", "password" : ""}',
            'response' : '',
            'certificate' : '',
            'retries' : ''
            }

api_req = apicall.api_request(nobj)
asyncio.run(api_req.make_post_call())


