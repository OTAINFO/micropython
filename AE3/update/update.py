# OTAinfo, Inc - By: Akshay - Mon Aug 18 2025
#import zlib
import asyncio
from otainfo_apis import apicall
import time
class update:

    def __init__(self, config):
        self.cfg = config

    def checkandgetupdate(self):

        try:
            if(self.cfg['update']):
                url = self.cfg['update']

                nobj =  {  'url' : url,
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
                api_req = apicall.api_request(nobj)
                file_found = asyncio.run(api_req.make_http_call())
                time.sleep(10)
                print(file_found)
                if file_found:
                    nobj['method'] = 'GET'
                    nobj['header'] = {"Content-Type": "text/plain"}
                api_req.update_args(nobj)
                filedata = asyncio.run(api_req.make_http_call())
                print(filedata)
        except:
            print("No updates found.. ")



