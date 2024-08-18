import requests
import json
import time
class Dial:
    def __init__(self, uuid, secret,server):
        self.uuid = uuid
        self.secret = secret
        self.name = "Not set"
        self.server = server
        self.light = False
        self.color = 5,5,5
        #time.sleep(5)
        #self.get_data()

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

    def light_on(self):
        if not self.light:
            self.set_color(self.color[0],self.color[1],self.color[2])
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
        try:
            message = f"http://{self.server}/api/v0/dial/{self.uuid}/backlight?red={self.clamp(r)}&green={self.clamp(g)}&blue={self.clamp(b)}&white={self.clamp(w)}&key={self.secret}"
            requests.get(message)
            if r+g+b > 0:
                self.light = True
                self.color = [r,g,b]
            else:
                self.light = False
        except:
            print("sending error")

    def set_name(self,name):
        self.name = name
        message = f"http://{self.server}/api/v0/dial/{self.uuid}/name?key={self.secret}&name={self.name}"
        requests.get(message)


if __name__ == "__main__":
    d = Dial("90002E000650564139323920","cTpAWYuRpA2zx75Yh961Cg","vumeter.local:5340") #currently the default keys are used - move to config file once in production
    time.sleep(2)
    #d.set_dial(60)
    #d.set_image("arc_image.png")
    #d.get_image()
    d.set_color(0,80,0)