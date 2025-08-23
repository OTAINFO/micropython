# OTAinfo, Inc - By: Akshay - Mon Aug 18 2025
import json
import os

class config:

    def __init__(self, passcode):
        self.config = {}
        self.passcode = passcode


    def loadconfig(self):

        filefound = False
        try:
            _temp = open('./config/config.json', 'r')
            filefound = True
        except:
            print("Error in reading config.json")
        print("File Found? ", filefound)
        if filefound:
            config_file = open('./config/config.json', 'r')
            secured_config_file_contents = config_file.read()
            print("Contents: ", secured_config_file_contents)
            config_file_contents = self.decrypt_contents(secured_config_file_contents)
            config_file.close()
            print(config_file_contents)
            if(config_file_contents):
                self.config = eval(config_file_contents)
                if len(self.config) > 0:
                    print("Config loaded")

    def decrypt_contents(self, contents):
        return contents

    def getconfig(self):
        return self.config

    def saveconfig(self, contents):
        print('Saving Config ... ')
        print(self.config)
        print(contents)
        if (self.config != contents):
            print('Contents Updated.. ')
            keys_added = set(contents.keys()) - set(self.config.keys())
            keys_removed = set(self.config.keys()) - set(contents.keys())
            if keys_removed:
                print(keys_removed)
                for key in keys_removed:
                    newkey = key + 'old'
                    self.config[newkey] = self.config[key]
            if keys_added:
                print(keys_added)
                for key in keys_added:
                    self.config[key] = contents[key]

            for key in contents.keys():
                if self.config[key] != contents[key]:
                    print('Contents changed for key: ' + key + ' old: ' + self.config[key] + '  new: ' + contents[key])
                    newkey = 'ov' + key
                    self.config[newkey] = self.config[key]
                    self.config[key] = contents[key]

       #Type Error: Object with buffer protocol required
        print("Saving ..")
        config_file = open('./config/config.json', 'w', encoding='utf-8')
        json.dump(self.config, config_file)
        config_file.close()

class st:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config):
       if not hasattr(self, '_initialized'):  # Prevent re-initialization on subsequent calls
           print("st initialized!")
           self._initialized = True
           self.config = config

    def getcacheconfig(self):
        return self.config

    def saveconfig(self):
        cfg = config('')
        cfg.saveconfig(self.config)

    def addkey(self, key, value):
        self.config[key] = value
        #pass

