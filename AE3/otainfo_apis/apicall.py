'''
# API Requests to OTAinfo cloud - By: Akshay - Sun Aug 10 2025
#
#
# **kwargs must atleast have
 {  'url' : '',
    'url_port' : '',
    'protocol' : '',
    'header' :{'k':'v', 'k1': 'v1',...},
    'status' : '',
    'method' : '',
    'uri' : '',
    'payload' : '',
    'response' : '',
    'certificate' : '',
    'retries' : ''

 }


'''
#import uasyncio as asyncio
#import usocket as socket
#import ussl
import requests


class api_request():

    def __init__(self, args):
        print("In api")
        self.args = args

    async def make_post_call(self):
        print("make post call")
        if 'url' in self.args.keys():
            if self.validate_url(self.args['url']):
                fqurl = self.args['url'] + self.args['uri']
                headers = self.args['header']
                payload = ''
                if self.args['method'] == 'POST':
                    payload = self.args['payload']

                self.post_data_with_headers(fqurl, payload, headers)
                print("Request complete.")


    def validate_url(self, url):
        if url:
            return True
        return False

    def post_data_with_headers(self, url, data, headers):
        response = None
        try:
            response = requests.post(url, data=data, headers=headers)
            # print("Status Code:", response.status_code)
            # print("Response Content:", response.content)
            # print("Response encoding:", response.encoding)
            # print("Response headers: ", response.headers)
            # print("Response reason:", response.reason)
            # print("Response Content: ", response.content)
            # print("Response json: " ,response.json())
            # print("Response status_code: " , response.status_code)
        except Exception as e:
            print("Error during POST request:", e)
        if response:
            print("Status: : ", response.status_code)
