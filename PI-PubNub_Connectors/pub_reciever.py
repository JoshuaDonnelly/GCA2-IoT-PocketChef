
import requests
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
import time

CHANNEL = "raspi"
UUID = "ec2-subscriber"
TOKEN_SERVER = "http:/AWS:5000/get-token" #

def get_read_token():
    resp = requests.get(f"{TOKEN_SERVER}/{UUID}")
    resp.raise_for_status()
    return resp.json()["token"]

# Fetch token from pub_server
auth_token = get_read_token()

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "subscribe_key" #
pnconfig.publish_key = "publish_key" #
pnconfig.uuid = UUID
pnconfig.auth_key = auth_token
pnconfig.ssl = True

pubnub = PubNub(pnconfig)

class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        print("Received:", message.message)

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(CHANNEL).execute()

# Keep alive and refresh token if needed
while True:
    time.sleep(1)

