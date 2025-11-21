import requests
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
import time
import random

# Config
EC2_SERVER = "http://AWS:5000" #
PI_UUID = "raspi-01"
CHANNEL = "raspi"
TOKEN_REFRESH_INTERVAL = 50 * 60  # refresh every 50 minutes

#Function to fetch token
def get_write_token():
    resp = requests.get(f"{EC2_SERVER}/get-token/{PI_UUID}")
    resp.raise_for_status()
    return resp.json()["token"]

# PubNub init
token = get_write_token()
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "subscribe_key" #
pnconfig.publish_key = "publish_key" #
pnconfig.uuid = PI_UUID
pnconfig.auth_key = token
pnconfig.ssl = True

pubnub = PubNub(pnconfig)

#  Main Loop
last_refresh = time.time()

while True:
    # Auto-refresh token
    if time.time() - last_refresh > TOKEN_REFRESH_INTERVAL:
        print("Refreshing token...")
        token = get_write_token()
        pubnub.set_auth_key(token)
        last_refresh = time.time()
        print("Token refreshed!")

    # Send fake sensor data
    temperature = random.uniform(20.0, 30.0)
    message = {"temperature": temperature}
    print("Sending:", message)
    pubnub.publish().channel(CHANNEL).message(message).sync()
    time.sleep(2)
