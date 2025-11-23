import requests
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
import time
import spidev
import math
from gpiozero import LED

# Config
EC2_SERVER = "http://AWS:5000" #
PI_UUID = "raspi-01"
CHANNEL = "raspi"
TOKEN_REFRESH_INTERVAL = 50 * 60 # 50 min

# LED settings
led = LED(17)
led.on()

# MCP3008 SPI
SPI_BUS = 0
SPI_DEVICE = 0

# Thermistor settings
VREF = 3.3
R_FIXED = 200000.0 # 200k resistor
R0 = 100000.0      # 100k thermistor
T0 = 25.0 + 273.15 # reference Kelvin
BETA = 3950.0      # typical for 100k NTC

# LED function
def led_flash(times=3, speed=0.2):
    for _ in range(times):
        led.on()
        time.sleep(speed)
        led.off()
        time.sleep(speed)

# Token function
def get_write_token():
    resp = requests.get(f"{EC2_SERVER}/get-token/{PI_UUID}")
    resp.raise_for_status()
    return resp.json()["token"]

# MCP3008 functions
spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = 1350000

def read_adc(channel):
    # MCP3008 protocol: start bit, single-ended, channel
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value

def read_temperature():
    adc_value = read_adc(0) # CH0
    voltage = (adc_value / 1023.0) * VREF

    if voltage <= 0:
        return None  # wire unplugged
    r_therm = (R_FIXED * voltage) / (VREF - voltage)

    # Beta equation
    temperature_k = 1.0 / (1.0 / BETA * math.log(r_therm / R0) + 1.0 / T0)
    temperature_c = temperature_k - 273.15
    return temperature_c

# Pubnub init
token = get_write_token()

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "subscribe_key" #
pnconfig.publish_key = "publish_key" #
pnconfig.uuid = PI_UUID
pnconfig.auth_key = token
pnconfig.ssl = True

pubnub = PubNub(pnconfig)

# Main loop
last_refresh = time.time()

while True:
    # Token auto-refresh
    if time.time() - last_refresh > TOKEN_REFRESH_INTERVAL:
        print("Refreshing token...")
        token = get_write_token()
        pubnub.set_auth_key(token)
        last_refresh = time.time()
        print("Token refreshed!")

    # Read temperature
    temperature = read_temperature()

    if temperature is None:
        print("Thermistor disconnected!")
        continue

    if temperature > 180:
        led_flash(times=5, speed=0.2)

    # Send to PubNub
    message = {"temperature": round(temperature, 2)}
    print("Sending:", message)

    pubnub.publish().channel(CHANNEL).message(message).sync()
    time.sleep(2)

