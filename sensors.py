import RPi.GPIO as GPIO
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import os
from dotenv import load_dotenv, find_dotenv
from pubnub.pubnub import SubscribeListener
import json

load_dotenv(find_dotenv())
pnconfig = PNConfiguration()
pnconfig.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
print(os.getenv("PUBNUB_SUBSCRIBE_KEY"))
pnconfig.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
pnconfig.user_id = "pi-0"
pnconfig.enable_subscribe = True

pubnub = PubNub(pnconfig)


sensors_list=["buzzer"]
data = {}

class StatusListener(SubscribeListener):
    def status(self, pubnub, status):
        print(f'Status: {status.category.name}')
        
        
status_listener = StatusListener()
pubnub.add_listener(status_listener)

my_channel = "johns-pi"
subscription = pubnub.channel(my_channel).subscription()

subscription.on_message = lambda message: handle_message(message)
subscription.subscribe()
print(f'Subscribed to channel: {my_channel}')

publish_result = pubnub.publish().channel(my_channel).message("Hello from John's pi").sync()

def handle_message(message):
    print(message.message)
    msg = json.loads(json.dumps(message.message))
    if 'message' in msg:
        buzzer = msg['message']['buzzer']
        if buzzer == 'on':
            data["alarm"] = True
        elif buzzer == 'off':
            data["alarm"] = False


pir_pin = 23
buzzer_pin = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)
GPIO.setup(buzzer_pin, GPIO.OUT)

def main():
    motion_detection()


def motion_detection():
    data["alarm"] = False
    trigger = False
    while True:
        if GPIO.input(pir_pin):
            print("Motion detected")
            beep(4)
            trigger = True
            pubnub.publish().channel(my_channel).message('Motion:Yes').sync()
            time.sleep(1)
        elif trigger:
            pubnub.publish().channel(my_channel).message('Motion:No').sync()
            trigger = False

        if data["alarm"]:
            beep(2)


def beep(repeat):
    for i in range(0, repeat):
        for pulse in range(60):
            GPIO.output(buzzer_pin, True)
            time.sleep(0.001)
            GPIO.output(buzzer_pin, False)
            time.sleep(0.001)
        time.sleep(0.02)


if __name__ == "__main__":
    main()
