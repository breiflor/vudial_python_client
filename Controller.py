import json
import time

import requests
from Dial import Dial
from paho.mqtt import client as mqtt_client

class Controller:
    def __init__(self,config_file="config.json",client_id = "vuserver"):
        data = json.load(open(config_file))
        self.secret = data["key"]
        self.server = data["server"]
        self.dails = []
        self.enumerate_dials()
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,client_id)
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(data["user"], data["password"])
        self.client.connect(data["mqtt_Server"], data["port"])
        self.client.loop_start()

    def on_connect(self,client, userdata, flags, rc):
        print("connected to broker")
        for index,dail in enumerate(self.dails):
            print(f"vumeter/{index}/switch")
            self.client.subscribe(f"vumeter/{index}/switch")
            self.client.subscribe(f"vumeter/{index}/rgb/set")
        self.client.on_message = self.callback

    def enumerate_dials(self):
        message = f"http://{self.server}/api/v0/dial/list?key={self.secret}"
        response = json.loads(requests.get(message).text)["data"]
        print(response)
        for dial in response:
            self.dails.append(Dial(dial["uid"],self.secret,self.server))

    def callback(self, client, userdata, msg):
        print(msg.payload)
        if "switch" in msg.topic :
            self.switch_dial(msg)
        elif "rgb" in msg.topic:
            self.handle_light(msg)

    def handle_light(self,msg):
        color = msg.payload.decode("utf-8").split(",")
        print(color)
        self.dails[int(msg.topic.split("/")[1])].set_color(int(int(color[0])/255*100),int(int(color[1])/255*100),int(int(color[2])/255*100))
    def switch_dial(self, msg):
        if "ON" in msg.payload.decode("utf-8"):
            self.dails[int(msg.topic.split("/")[1])].light_on()
        else:
            self.dails[int(msg.topic.split("/")[1])].set_color(0, 0, 0)



if __name__ == "__main__":
    controller = Controller()
    while True:
        time.sleep(1)