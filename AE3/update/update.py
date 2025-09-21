# OTAinfo, Inc - By: Akshay - Mon Aug 18 2025
import asyncio
from otainfo_apis import apicall
import time
import deflate
import uos

class update:

    def __init__(self, config):
        self.cfg = config

    def checkandgetupdate(self):
        print("checking for Update..")
        if True:
            if('update' in self.cfg.keys() and self.cfg['update']):
                url = self.cfg['update']
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
                    nobj1['header'] = response['headers']
                api_req.update_args(nobj1)
                response, filepath = asyncio.run(api_req.make_http_call())
                print(dir(filepath))
                print(filepath)
                self.extract_tar_gz(filepath)
                #print(len(response.content))


    def extract_tar_gz(self, filename, output_dir="."):
        # Step 1: decompress gzip into memory/file-like object
        print("fqfp: " ,filename)
        with open(filename, "rb") as f:
            with deflate.DeflateIO(f, deflate.AUTO) as gz:
                data = gz.read()

        # Step 2: parse tar archive
        i = 0
        block_size = 512

        while i < len(data):
            block = data[i:i+block_size]
            i += block_size

            # Empty block -> end of archive
            if block.strip(b"\0") == b"":
                break

            # File name (100 bytes)
            name = block[0:100].rstrip(b"\0").decode("utf-8")
            if not name:
                continue

            # File size is stored in octal at offset 124–136
            size_str = block[124:136].rstrip(b"\0").decode("utf-8").strip()
            size = int(size_str, 8) if size_str else 0
            print("size: " , size)

            # Read file content
            file_data = data[i:i+size]
            i += (size + block_size - 1) // block_size * block_size  # align to 512
            #print(file_data)
            # Skip directories
            if name.endswith("/"):
                try:
                    uos.mkdir(output_dir + "/" + name)
                except OSError:
                    pass
                continue

            # Ensure parent directories exist
            parts = name.split("/")
            if len(parts) > 1:
                path = output_dir
                for p in parts[:-1]:
                    path = path + "/" + p
                    try:
                        uos.mkdir(path)
                    except OSError:
                        pass

            # Write file
            print(name[2:])
            with open("./" +name[2:], "wb", encoding='utf-8' ) as out:
                out.write(file_data)

            print("Extracted:", name[2:])





