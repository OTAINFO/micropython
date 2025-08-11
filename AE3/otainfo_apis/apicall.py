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
import uasyncio as asyncio
#import usocket as socket
#import ussl
import urequests

class api_request():

    def __init__(self, **kwargs):

        self.args = kwargs

    async def make_post_call(self):

        if 'url' in self.args.keys():
            if self.validate_url(self.args['url']):
                fqurl = self.args['url'] + self.args['uri']
                headers = self.args['header']
                payload = ''
                if self.args['method'] == 'POST':
                    payload = self.args['payload']

                await self.post_data_with_headers(fqurl, payload, headers)
                print("Request complete.")


    def validate_url(self, url):
        if url:
            return True
        return False

    def post_data_with_headers(self, url, data, headers):
        try:
            response = urequests.post(url, json=data, headers=headers, ssl=True)
            print("Status Code:", response.status_code)
            print("Response Text:", response.text)
            response.close()
        except Exception as e:
            print("Error during POST request:", e)


