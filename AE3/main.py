# OTAinfo, Inc - By: Akshay - Mon Aug 11 2025

from wifi.wifi_connection import wifi_connect
from otainfo_apis import apicall
import asyncio
import time
import omv
import machine
import json
from config import config
from update import update

cfg = config.config('')
cfg.loadconfig()
cfgdata = cfg.getconfig()
print(omv.board_id());
print(omv.arch())
print(omv.version_string())
print(machine.unique_id())
byte_string = machine.unique_id()
decimal_value = int.from_bytes(byte_string)
try:
    con = wifi_connect(cfgdata['wifi_username'], cfgdata['wifi_password'])
    con.connect()
    while not con.wlan.isconnected():
        time.sleep(1)
except:
    print('wifi credentials absent')


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
asyncio.run(api_req.make_http_call())
update_process = update.update(cfgdata)
update_process.checkandgetupdate()

