import requests
import json
import time
class Dial:
    def __init__(self, uuid, secret,server):
        self.uuid = uuid
        self.secret = secret
        self.name = "Not set"
        self.server = server
        #self.get_data()
        #time.sleep(1)

    def clamp(self,value, min_val=0, max_val=100):
        return max(min(value, max_val), min_val)

    def set_dial(self,percentage):
        message = f"http://{self.server}/api/v0/dial/{self.uuid}/set?key={self.secret}&value={percentage}"
        self.dial = percentage
        requests.get(message)

    def get_data(self):
        message = f"http://{self.server}/api/v0/dial/{self.uuid}/status?key={self.secret}"
        data = json.loads(requests.get(message).text)["data"]
        print(data)
        self.name = data["dial_name"]
        self.dial = data["value"]
        self.color = data["rgbw"]


    def set_image(self,imagefile):
        url = f"http://{self.server}/api/v0/dial/{self.uuid}/image/set?key={self.secret}"
        with open(imagefile, 'rb') as f:
            files = {"imgfile": f}
            response = requests.post(url,files=files)

    def get_image(self):
        message = f"http://{self.server}/api/v0/dial/{self.uuid}/image/get?key={self.secret}"
        data = requests.get(message)
        with open("test.png","wb") as r:
            r.write(data.content)
    def set_color(self,r=0,g=0,b=0,w=0):
        #sending white is currently not supported
        message = f"http://{self.server}/api/v0/dial/{self.uuid}/backlight?red={self.clamp(r)}&green={self.clamp(g)}&blue={self.clamp(b)}&white={self.clamp(w)}&key={self.secret}"
        requests.get(message)

    def set_name(self,name):
        self.name = name
        message = f"http://{self.server}/api/v0/dial/{self.uuid}/name?key={self.secret}&name={self.name}"
        requests.get(message)


if __name__ == "__main__":
    d = Dial("90002E000650564139323920","cTpAWYuRpA2zx75Yh961Cg","vumeter.local:5340") #currently the default keys are used - move to config file once in production
    #d.set_dial(56)
    #d.set_image("cpu-load.png")
    #d.get_image()
    d.set_color(0,0,0)