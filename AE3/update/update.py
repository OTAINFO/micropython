# OTAinfo, Inc - By: Akshay - Mon Aug 18 2025
import asyncio
from otainfo_apis import apicall
import time
class update:

    def __init__(self, config):
        self.cfg = config

    def checkandgetupdate(self):
        print("checking for Update..")
        print(self.cfg)
        if True:
            if('update' in self.cfg.keys() and self.cfg['update']):

                url = self.cfg['update']
                url = "https://otainfo.us:9001/test1.py"
                nobj1 =  {  'url' : url,
                            'url_port' : '9001',
                            'protocol' : 'https',
                            'header' :{"Content-Type": "application/json"},
                            'status' : '',
                            'method' : 'HEAD',
                            'uri' : '',
                            'payload' : '',
                            'response' : '',
                            'certificate' : '',
                            'retries' : ''
                            }
                api_req = apicall.api_request(nobj1)
                response = asyncio.run(api_req.make_http_call())
                if 'exception' in response.keys():
                    response['message'] = 'Failed to update from: ' + url
                    response['status'] = 'Failed'
                    response['device_id'] = ''

                    #upload metric to OTAinfo cloud
                    #exit
                    print('Error in update')
                    return

                time.sleep(4)
                # print(file_found)
                if response:
                    nobj1['method'] = 'GET'
                    nobj1['header'] = response['Content-Type']
                api_req.update_args(nobj1)
                asyncio.run(api_req.make_http_call())
                #print(len(response.content))



