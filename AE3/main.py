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
import alif
import deflate
import io

#print(help('requests.head'))
#print(dir(alif))
#alif.info()
#print("alif data: ", alif_data)
#print(alif.Flash())
#print("usc_msc: " ,alif.usb_msc)

cfg = config.config('')
cfg.loadconfig()
cfgdata = cfg.getconfig()

cfgdata_type_validation = isinstance(cfgdata, dict)
macaddress= ""
count = sum(1 for _ in cfgdata.keys())
if (cfgdata and cfgdata_type_validation and count > 0):
    print("Config loaded")
st =config.st()
st.loadconfig(cfgdata)
st.addkey('board_id', omv.board_id())
st.addkey('arch', omv.arch())
st.addkey('hw_version_str', omv.version_string())
st.saveconfig()
byte_string = machine.unique_id()
decimal_value = int.from_bytes(byte_string)

try:
    con = wifi_connect(cfgdata['wifi_username'], cfgdata['wifi_password'])
    con.connect()
    while not con.wlan.isconnected():
        time.sleep(1)
    macaddress = con.getmac()
except:
    print('wifi credentials absent')
print("Mac Address: " , macaddress)
cfgdata = st.getcacheconfig()

cloudpass = st.getvalueifkeypresent('cloudpassword')
cloudusername=st.getvalueifkeypresent('cloudusername')
cloudurl=st.getvalueifkeypresent("cloudurl")
cloudsfid= st.getvalueifkeypresent("sfid")
cloudcompanyid = st.getvalueifkeypresent('coudcompanyid')

payload = {}
payload['username']= cloudusername
payload['password'] = cloudpass
payload['device_id'] = macaddress
payload['model'] = st.getvalueifkeypresent('arch')
json_str_payload = str(json.dumps(payload))
uri = cloudsfid + '/api-token-auth/'
nobj =  {  'url' : 'https://otainfo.us:9001/',
            'url_port' : '9001',
            'protocol' : 'https',
            'header' :{"Content-Type": "application/json"},
            'status' : '',
            'method' : 'POST',
            'uri' : uri,
            'payload' : json_str_payload,
            'response' : '',
            'certificate' : '',
            'retries' : ''
            }

api_req = apicall.api_request(nobj)
asyncio.run(api_req.make_http_call())

update_process = update.update(cfgdata)
update_process.checkandgetupdate()

