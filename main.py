import micropython            # Needed to run any MicroPython code
import machine                # Interfaces with hardware components
from machine import Pin, ADC  # Define pin and ADC
import time                   # Allows use of time.sleep() for delays
from lib.keys import *        # Secrets
from music import *           # imports the song stuff
import ubinascii              # Conversions between binary data and various encodings
import random                 # Random number generator
from mqtt import MQTTClient   # For use of MQTT protocol
import dht                    # For the DHT temp and humidity sensor

# BEGIN SETTINGS
# These need to be change to suit your environment
RANDOMS_INTERVAL = 20000    # milliseconds
last_random_sent_ticks = 0  # milliseconds

# Adafruit IO (AIO) configuration modified to work with local Home Assistant Mosquitto Broker
AIO_SERVER        = MQTT_BROKER
AIO_PORT          = MQTT_PORT
AIO_USER          = MQTT_USER
AIO_KEY           = MQTT_PASSWORD
AIO_CLIENT_ID     = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_GADGET_FEED   = "homeassistant/gadget"
AIO_RANDOMS_FEED  = "homeassistant/gadget/random"
AIO_CURTAINS_FEED = "homeassistant/gadget/curtains"
AIO_LIGHT_FEED    = "homeassistant/gadget/light"
AIO_TEMP_FEED     = "homeassistant/gadget/temp"
AIO_HUMIDITY_FEED = "homeassistant/gadget/humidity"

# PIN setup below

# led pin initialization for Raspberry Pico W
led = Pin("LED", Pin.OUT)   

# Joystick
xAxisPin = ADC(Pin(28))
yAxisPin = ADC(Pin(27))
buttonPin = Pin(20,Pin.IN, Pin.PULL_UP)

# Light sensor
ldr = ADC(Pin(26))

# DHT - temperature and humidity sensor
dhtSensor = dht.DHT11(machine.Pin(19))

# Speaker setup is done in music.py:
# buzzer = PWM(Pin(22))

# END SETTINGS

# Callback Function to respond to messages from the MQTT server
def sub_cb(topic, msg):                         # sub_cb means "callback subroutine"
    print((topic, msg))                         # Outputs the message that was received. Debugging use.
    if  msg == b"XMAS":                         # If message says "XMAS" 
        playsong(song)                          # ... then play Jingle Bells
    else:                                       # If any other message is received ...
        print(msg)                # ... do nothing but output that it happened.

# Function to generate a random number between 0 and the upper_bound
def random_integer(upper_bound):
    return random.getrandbits(32) % upper_bound

# Function to publish Home Assistant MQTT server at fixed interval.
# Random function from sample code has been left in as an function POC

def send():
    #Random function from the MQTT sample code. Used as a canary and can be removed. 

    global last_random_sent_ticks
    global RANDOMS_INTERVAL

    if ((time.ticks_ms() - last_random_sent_ticks) < RANDOMS_INTERVAL):
        return; # Too soon since last one sent.

    some_number = random_integer(100)

    try:
        client.publish(topic=AIO_RANDOMS_FEED, msg=str(some_number))
    #    print("DONE")
    except Exception as e:
        print("FAILED {}" .format(AIO_RANDOMS_FEED))
    finally:
       last_random_sent_ticks = time.ticks_ms()

    # Light sensor stuff here
    # Original code: https://github.com/iot-lnu/pico-w/blob/main/sensor-examples/P23_LDR_Photo_Resistor
    light = ldr.read_u16()
    darkness = round(light / 65535 * 100, 2)
    percent_brightness = round(100 - light / 65535 * 100, 2)

    try:
        client.publish(topic=AIO_LIGHT_FEED, msg=(str(percent_brightness)))
    except Exception as e:
        print("FAILED {}" .format(AIO_LIGHT_FEED))
        print(e)
    
    # Temperature sensor stuff here
    # Original code: https://github.com/iot-lnu/pico-w/blob/main/sensor-examples/P5_DHT_11_DHT_22
    try:
        dhtSensor.measure()
        temperature = dhtSensor.temperature()
        #print("Temperature is {} degrees Celsius".format(temperature))
        client.publish(topic=AIO_TEMP_FEED, msg=(str(temperature)))
    except Exception as error:
        print("Exception occurred", error)

    # Humidity sensor stuff here

    try:
        dhtSensor.measure()
        humidity = dhtSensor.humidity()
        #print("Humidity is {}%".format(humidity))
        client.publish(topic=AIO_HUMIDITY_FEED, msg=(str(humidity)))
    except Exception as error:
        print("Exception occurred", error) 

    # Jostick code below
    # Original code: https://github.com/iot-lnu/pico-w/blob/main/sensor-examples/P16_Joystick
def control_curtains():
    xAxisValue = xAxisPin.read_u16()
    yAxisValue = yAxisPin.read_u16()
    buttonValue = buttonPin.value()

    xAxisStatus = "center"
    yAxisStatus = "center"
    buttonStatus = "not pressed"
    action = ""

    if xAxisValue <= 600:
        xAxisStatus = "south"
        action = "down"
    elif xAxisValue >= 60000:
        xAxisStatus = "north"
        action = "up"
# At the moment only up and down are used. Below are code that can be used for left and right too.
#    if yAxisValue <= 600:
#        yAxisStatus = "east"
#        action = "right"
#    elif yAxisValue >= 60000:
#        yAxisStatus = "west"
#        action = "left"
    if buttonValue == 0:
        buttonStatus = "pressed"
        action = "button_pressed"
    
    if action != "":
        try:
            client.publish(topic=AIO_CURTAINS_FEED, msg=str(action))
        #    print("DONE")
        except Exception as e:
            print("FAILED")
        finally:
            action = ""

# Use the MQTT protocol to connect to the MQTT server
client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)

client.set_callback(sub_cb)
client.connect()
client.subscribe(AIO_GADGET_FEED)
print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, AIO_GADGET_FEED))

try:                            # Code between try: and finally: may cause an error
                                # so ensure the client disconnects the server if
                                # that happens.
    while 1:                    # Repeat this loop forever
        client.check_msg()      # Action a message if one is received. Non-blocking.
        send()           # Send a random number to Adafruit IO if it's time.
        control_curtains()      # Use joystick to control curtains in kid's bedrooms
finally:                        # If an exception is thrown ...
    client.disconnect()         # ... disconnect the client and clean up.
    client = None
    print("Disconnected from the MQTT server.")