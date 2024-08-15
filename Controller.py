import json
import time

import requests
from Dial import Dial

class Controller:
    def __init__(self,config_file="config.json"):
        data = json.load(open(config_file))
        self.secret = data["key"]
        self.server = data["server"]
        self.dails = []
        self.enumerate_dials()

    def enumerate_dials(self):
        message = f"http://{self.server}/api/v0/dial/list?key={self.secret}"
        response = json.loads(requests.get(message).text)["data"]
        print(response)
        for dial in response:
            self.dails.append(Dial(dial["uid"],self.secret,self.server))

if __name__ == "__main__":
    controller = Controller()
    time.sleep(20)
    controller.dails[0].set_color(50)