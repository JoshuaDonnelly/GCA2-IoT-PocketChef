import requests
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
import time
import os

CHANNEL = "raspi"
UUID = "ec2-subscriber"
TOKEN_SERVER = "http://3.252.126.184:4999" 

def get_read_token():
    resp = requests.get(f"{TOKEN_SERVER}/{UUID}")
    resp.raise_for_status()
    return resp.json()["token"]

# Fetch token from pub_server
auth_token = get_read_token()


pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-72118a46-881b-4c38-abd5-5a19c619592a"
pnconfig.publish_key = "pub-c-0b280189-eca0-4ad4-9d6d-4f6ab038e2f7"
pnconfig.uuid = UUID
pnconfig.auth_key = auth_token
pnconfig.ssl = True

pubnub = PubNub(pnconfig)


class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        print("Received:", message.message)
        with open("latest_temp.json", "w") as f:
            json.dump(message.message, f)
            
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(CHANNEL).execute()

# Keep alive and refresh token if needed
while True:
    time.sleep(1)
