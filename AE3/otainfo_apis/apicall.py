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

    def make_post_call(self):
        print("make post call")
        print(self.args.keys())
        if 'url' in self.args.keys():
            if self.validate_url(self.args['url']):
                fqurl = self.args['url'] + self.args['uri']
                headers = self.args['header']
                print(headers)
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
        try:
            print(url)
            print(data)
            print(headers)
            response = requests.post(url, json=data, headers=headers)
            print("Status Code:", response.status_code)
            print("Response Content:", response.content)
           # print("Response apperent_encoding:", response.apparent_encoding)
            #print("Response elapsed:", response.elapsed)
            #print("Response history:", response.history)
            #print("Response request:", response.request)
            #--#print("Response reason:", response.reason)
            #print("Response text:", response.text)
            #print("Response url:", response.url)
            #response.close()
        except Exception as e:
            print("Error during POST request:", e)


