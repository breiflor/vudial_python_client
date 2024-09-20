import json
import time

import requests
from Dial import Dial
from ImageCreator import ImageCreator
from paho.mqtt import client as mqtt_client
from pathlib import Path

class Controller:
    def __init__(self,config_file="config.json",client_id = "vuserver"):
        data = json.load(open(config_file))
        self.secret = data["key"]
        self.server = data["server"]
        self.dails = []
        self.enumerate_dials()
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,client_id)
        self.icons = []
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(data["user"], data["password"])
        self.client.connect(data["mqtt_Server"], data["port"])
        self.client.loop_start()
        self.list_icons()

    def on_connect(self,client, userdata, flags, rc):
        print("connected to broker")
        for index,dail in enumerate(self.dails):
            print(f"vumeter/{index}/switch")
            self.client.subscribe(f"vumeter/{index}/switch")
            self.client.subscribe(f"vumeter/{index}/rgb/set")
            self.client.subscribe(f"vumeter/{index}/range/start")
            self.client.subscribe(f"vumeter/{index}/range/end")
            self.client.subscribe(f"vumeter/{index}/range/center")
            self.client.subscribe(f"vumeter/{index}/unit")
            self.client.subscribe(f"vumeter/{index}/title")
            self.client.subscribe(f"vumeter/{index}/icon")
            self.client.subscribe(f"vumeter/{index}/value")
            self.client.subscribe(f"vumeter/{index}/segments")
            self.client.subscribe(f"vumeter/{index}/update")
        self.client.on_message = self.callback

    def list_icons(self):
        for asset in Path("./icons").absolute().iterdir():
            if asset.suffix == ".jpg" or asset.suffix == ".png":
                self.icons.append(asset.name)
        data = {"icons": self.icons}
        datastring = json.dumps(data)
        self.client.publish("vumeter/icons_list", datastring)

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
        elif "range" in msg.topic:
            self.handle_range(msg)
        elif "unit" in msg.topic:
            self.handle_unit(msg)
        elif "title" in msg.topic:
            self.handle_title(msg)
        elif "icon" in msg.topic:
            self.handle_icon(msg)
        elif "value" in msg.topic:
            self.handle_value(msg)
        elif "segments" in msg.topic:
            self.handle_segments(msg)
        elif "update" in msg.topic:
            self.handle_update(msg)

    def handle_light(self,msg):
        color = msg.payload.decode("utf-8").split(",")
        print(color)
        self.dails[int(msg.topic.split("/")[1])].set_color(int(int(color[0])/255*100),int(int(color[1])/255*100),int(int(color[2])/255*100))
    def switch_dial(self, msg):
        if "ON" in msg.payload.decode("utf-8"):
            self.dails[int(msg.topic.split("/")[1])].light_on()
        else:
            self.dails[int(msg.topic.split("/")[1])].set_color(0, 0, 0)

    def handle_range(self, msg):
        if "start" in msg.topic:
            self.dails[int(msg.topic.split("/")[1])].range[0] = msg.payload.decode("utf-8")
        elif "end" in msg.topic:
            self.dails[int(msg.topic.split("/")[1])].range[2] = msg.payload.decode("utf-8")
        elif "center" in msg.topic:
            self.dails[int(msg.topic.split("/")[1])].range[1] = msg.payload.decode("utf-8")

    def handle_unit(self, msg):
        self.dails[int(msg.topic.split("/")[1])].unit = msg.payload.decode("utf-8")

    def handle_title(self, msg):
        title = msg.payload.decode("utf-8")
        if title == "":
            self.dails[int(msg.topic.split("/")[1])].title = None
        else:
            self.dails[int(msg.topic.split("/")[1])].title = title

    def handle_icon(self, msg):
        self.dails[int(msg.topic.split("/")[1])].icon = "icons/"+msg.payload.decode("utf-8")

    def handle_value(self, msg):
        self.dails[int(msg.topic.split("/")[1])].set_dial(int(msg.payload.decode("utf-8")))

    def handle_segments(self, msg):
        self.dails[int(msg.topic.split("/")[1])].segments = int(msg.payload.decode("utf-8"))

    def handle_update(self, msg):
        tempfile = "temp.png"
        creator = ImageCreator()
        creator.create( self.dails[int(msg.topic.split("/")[1])],tempfile)
        self.dails[int(msg.topic.split("/")[1])].set_image(tempfile)


if __name__ == "__main__":
    time.sleep(20)
    controller = Controller()
    while True:
        time.sleep(21600) # update icon list every 6h
        controller.list_icons()