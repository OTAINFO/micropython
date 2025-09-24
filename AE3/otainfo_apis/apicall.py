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
import json
import deflate
import os

from config import config


class api_request():

    def __init__(self, args):
        print("In api")
        self.args = args

    def update_args(self, args):
        self.args = args

    async def make_http_call(self):
        print("making http call ..")
        if 'url' in self.args.keys():
            print("url: " , self.args['url'])
            if self.validate_url(self.args['url']):
                fqurl = self.args['url'] + self.args['uri']
                headers = self.args['header']
                payload = ''
                if self.args['method'] == 'POST':
                    payload = self.args['payload']
                    print("Method: POST")
                    self.post_data_with_headers(fqurl, payload, headers)
                if self.args['method'] == 'HEAD':
                    fqurl = self.args['url']
                    print("Method: HEAD")
                    payload = ''
                    return self.head_method(fqurl)

                if self.args['method'] == 'GET':
                    headers = self.args['header']
                    fqurl = self.args['url']
                    print("Method: GET")
                    return self.get_method(fqurl)
                print("Request complete.")


    def validate_url(self, url):
        if url:
            return True
        return False

    def post_data_with_headers(self, url, data, headers):
        response = None
        try:
            print(url)
            response = requests.post(url, data=data, headers=headers)
            print("Post response: ", response.content)
            if('api-token-auth' in url):
                print("Auth api was called")
                print("status code: ", response.status_code)
                if response.status_code == 200:
                    #save token
                    print("Saving token")
                    st = config.st()
                    print("Singleton loaded")
                    st.addkey('auth_api', response.status_code)
                    print("Saving response code")
                    response_data = json.loads(response.content)
                    print("Response data format changed")
                    print("Auth api response: ", response_data)
                    if 'token' in response_data.keys():
                        st.addkey('token', response_data['token'])
                        print("Cloud access token saved in cache..")
                        if 'nup' in response_data.keys():
                            print("New username/password must be present")
                            st.addkey('cloudpass', response_data['nup'])
                            st.addkey('cloudusername', response_data['username'])
                            print("New username/password found")
                    if 'update_url' in response_data.keys():
                        st.addkey('update', response_data['update_url'])
                        st.saveconfig()
                        print("New config saved")
            else:
                print(response.status_code)

        except Exception as e:
            print("Error during POST request:", e)
        if response:
            print("Status: : ", response.status_code)
        return response

    def head_method(self, url):
        response = None
        response_object = {}
        headers = {"Content-Type" : "plain/text",
        'User-Agent': 'Mozilla/5.0'}
        try:
            headers = {"Content-Type" : "text/plain"}
            response = requests.head(url, headers=headers)
        except Exception as e:
            response_object['url'] = url
            response_object['exception'] = str(e)
            response_object['action'] = 'Fix the url or wifi'
            response_object['cause'] = 'url or wifi'

        if response:
            response_split = response.headers.split('\n')
            response_object = {}
            response_headers = {}
            for elem in response_split:
                _temp = elem.split(':')
                key = _temp[0].strip()
                value = _temp[1].strip()
                if key == 'Content-Length':
                    value = int(value)
                response_headers[key] = value
            if 'status_code' not in response_object.keys():
                response_object['status_code'] = response.status_code
            response_object['content'] = response.content
            response_object['encoding'] = response.encoding
            response_object['reason'] = response.reason
            response_object['headers'] = response_headers
        return response_object

    def get_method(self, url):
        response = None
        filename = url[url.rindex('/')+1:]
        filewritepath = './repo'
        fqfp = filewritepath + '/' + filename
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(fqfp, 'wb', encoding='utf-8') as f:
                    try:
                        f.write(response._content)
                        print(f"File '{filename}' downloaded and saved successfully.")
                    except Exception as ex:
                        print("Exception: ",ex)
            else:
                print("File download error:  ", response.status_code)
        except Exception as e:
            print("HTTP GET could not execute for: " , url)
            print(e)
        return response, fqfp
