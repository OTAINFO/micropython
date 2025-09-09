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
from metrics import metrics
#print(help('requests.head'))
#print(dir(alif))
#alif.info()
#print("alif data: ", alif_data)
#print(alif.Flash())
#print("usc_msc: " ,alif.usb_msc)
print(dir(time))
#print(time.strftime("%Y-%m-%d %H:%M:%S", current_time_struct))

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
connect_metric = {}
try:
    con = wifi_connect(cfgdata['wifi_username'], cfgdata['wifi_password'])
    connect_metric= con.connect()
    while not con.wlan.isconnected():
        time.sleep(1)
    macaddress = con.getmac()
except:
    print('wifi credentials absent')
upload_metric = metrics.metrics().wifi_metric()
if 'singlemetric' in connect_metric.keys():
    upload_metric['metric_data'] = connect_metric['singlemetric']
else:
    upload_metric['metric_data'] = '-'


if 'status' in connect_metric.keys():
    upload_metric['status'] = connect_metric['status']

upload_metric['record_date'] = "2025-09-09T00:00:00"
#connect_metric['record_time']
#print("Upload_metric: ", upload_metric)
#print("connect_metric: " , connect_metric)
#print("Mac Address: " , macaddress)
st.addkey("mac", macaddress)
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

uri = cloudsfid + '/mupload/'

metric_obj =  {  'url' : 'https://otainfo.us:9001/',
'url_port' : '9001',
'protocol' : 'https',
'header' :{},
'status' : '',
'method' : 'POST',
'uri' : uri,
'payload' : '',
'response' : '',
'certificate' : '',
'retries' : ''
}
metric_obj['uri'] = uri
metric_obj['header'] = {"Authorization" : "JWT " + cfgdata['token'], "Content-Type" : "application/json"}
upload_metric['banner'] = st.getvalueifkeypresent('mac')
print(upload_metric)
json_metric = str(json.dumps(upload_metric))
metric_obj['payload'] = json_metric
api_req.update_args(metric_obj)
asyncio.run(api_req.make_http_call())


#update_process = update.update(cfgdata)
#update_process.checkandgetupdate()

