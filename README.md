# Home Control Gadget

Course 24ST - 1DT305 - Tillämpad Internet of Things, Introduktion - 7,5 hp at Linnaeus University in Kalmar. 
Andreas Galistel (ag22fi)

## Table of content
- [Home Control Gadget](#home-control-gadget)
  - [Table of content](#table-of-content)
  - [Project description](#project-description)
    - [Out of scope for course, but coming in the future](#out-of-scope-for-course-but-coming-in-the-future)
  - [Time needed](#time-needed)
    - [Hardware and software](#hardware-and-software)
      - [Hardware](#hardware)
      - [Easter egg](#easter-egg)
    - [Preparing the Pico W](#preparing-the-pico-w)
        - [Uh-oh, it's not responding anymore?!](#uh-oh-its-not-responding-anymore)
      - [IDE / Development environment](#ide--development-environment)
      - [Local server (Home Assistant)](#local-server-home-assistant)
    - [Wiring up the Pico W](#wiring-up-the-pico-w)
  - [Pico W code](#pico-w-code)
    - [Code samples](#code-samples)
    - [Full code](#full-code)
  - [Home Assistant code](#home-assistant-code)
    - [MQTT sensors in Home Assistant](#mqtt-sensors-in-home-assistant)
    - [Automations in Home Assistant:](#automations-in-home-assistant)
      - [Gadget: when button is pressed](#gadget-when-button-is-pressed)
      - [Gadget: close curtain](#gadget-close-curtain)
      - [Gadget: open curtain](#gadget-open-curtain)
      - [Gadget: Turn off lights](#gadget-turn-off-lights)
      - [Gadget: Turn on lights](#gadget-turn-on-lights)
  - [Visualisation:](#visualisation)
    - [Custom apex graph card code:](#custom-apex-graph-card-code)
  - [Todo later:](#todo-later)

## Project description

Since the course only ran over five weeks during the summer I had limited time to complete the device. 

My objective for the finished device was this:

A gadget equipped with sensors that automatically triggers automations in my existing Home Assistant setup, but also offer some manual input to trigger devices in the room the device is located. Thus, Home Assistant needs to have room presence working. 

 The idea is to improve quality of life by further enabling automations that will adjust lights, curtains and give notifications based on the sensory data. However all of this is not possible within the short timeframe of this course.

It was inspired by the [Aqara Cube](https://www.aqara.com/us/product/cube/) and similar such "odd" devices that also works as a sort of remote control, but don't look or act like the usual kind of control device. 

 These devices usually require manual input though, while my device is intended to mainly use sensors and react on the sensored values. I want to press as few buttons as possible in life. but the option for a "manual override" should be there if necessary. 

 The MVP (minimum viable product) was intended to use a light sensor and joystick. It will connect via WiFi to an MQTT server within Home Assistant. 

I live nextdoor to a swamp so humidity can be rather excruciating during the Summer and there is basically no trees offering shadow to our house. Plenty in the swamp though, along with one or two mosquittos.  

### Out of scope for course, but coming in the future

The gadget will (eventually) have a presence control thanks to its BLE component, which allows for automations to trigger differently depending on the room it is in. 

The presence control will be based on my existing Google/Nest Home devices which are present in most rooms of the house. I will start off using code by Sean Green from his repository: [Room presence with Google Homes](]https://github.com/seangreen2/home_assistant/wiki/Room-Presence-with-Google-Homes)

However the room presence is essentially all built inside of Home Assistant thus I did not focus on completing it before the end of the course. It would also require me to make the gadget movable and battery-powered, which I currently do not have the hardware for. 

E.g. in a bedroom it would allow me to control the bedroom curtains and start playing relaxing sounds on the speaker, while in the living room it would make it possible to close those curtains and start up cinema mode instead. 

## Time needed

How much experience you have with Python, MQTT and Home Assistant plays a big part, but even with limited experience you should be able to build the device itself relatively fast. 

If you're somewhat experienced, to complete the MVP (minimum viable product) with just the light sensor and WiFi setup you will need a couple of hours at most. 

1. If you have Home Assistant up and running already:
   
Setting up MQTT in Home Assistant is done in seconds. Copy my code above for the sensors, reload the yaml configuration and they should pop up right away in Home Assistant. For the regular sensors they should have values right away. The button sensor will update when you ... press the button. 

2. Installing Home Assistant
   
If you are not already running [Home Assistant](https://www.home-assistant.io/) that in itself can be a big leap. It is however the most potent, secure and most of all private home automation platform available. It is well worth trying out. 

You can install Home Assistant on a Raspberry Pi, but also an Intel Nuc or as a container in Proxmox or on a NAS. The core is the same, but you get slightly different feature on top of that. 
The Raspberry Pi solution is the most complete one and easiest to get started with.   

There are plug-n-play solutions too. Check out the installation guide on the official website: [Get started with Home Assistant](https://www.home-assistant.io/installation/)

### Hardware and software

The gadget is built up on the [Raspberry Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html). It's a single-board microcontroller with loads of compatible sensors and other components, and it's easy to program with [MicroPython](https://micropython.org/), which is essentially Python, but optimized for running on a microcontroller with some specific libraries added (e.g. machine).

The Raspberry Pico W and sensors used for this project was purchased from [electrokit.com](https://www.electrokit.com). They even have course specific kits you can buy that works well with the course.

 - [LNU Starter kit](https://www.electrokit.com/lnu-starter)
 - [25 sensor kit package](electrokit.com/sensor-kit-25-moduler)
 - [Addon Kit (if you want to use LoraWan)](https://www.electrokit.com/lnu-addon)

The university also has a repository with lots of code samples, which this projects has been based on: [IoT-LNU/Pico W](https://github.com/iot-lnu/pico-w/)

You can build pretty much any kind of smart device with these sensors. Your imagination sets the limits. 

#### Hardware
List of material for this project:

| Hardware | Purpose |
|------------------|---------------|
| Raspberry Pico W | Main hardware |
| Light Dependent Resistor | Measures level of light |
| Joystick | Manual input |
| Passive buzzer | Play tunes |
| DHT sensor | Measure temperature and humidity |

It should be noted that the light sensor that came with a 10k resistor on-board did not work with the sample code. It was confirmed by a teacher's assistant so I decided to use the more barebone solution with two two parallell 5k resistors instead ([the second alternative](https://github.com/iot-lnu/pico-w/tree/main/sensor-examples/P23_LDR_Photo_Resistor)). 

I also went with the [analog joystick](https://github.com/iot-lnu/pico-w/tree/main/sensor-examples/P16_Joystick) to allow for manual inputs. 
I decided that controling the curtains made sense since I can do that in most rooms and currently they are set to a schedule, but sometimes schedules change on the fly as the sun decide to go full supernova and heat up the Earth like a South Carolina BBQ.

#### Easter egg

Since I had time I had to add some kind of fun side thing too so I added a [passive buzzer](https://github.com/iot-lnu/pico-w/tree/main/sensor-examples/P18_Active_Piezo_Buzzer) that allows for playing music (if you can call it that) on the Pico W. Inside Home Assistant there is an automation that checks if the button is pressed for too long, and thus increase the value of the sensor, it then sends out an MQTT message called "XMAS", which makes the buzzer play a short version of "Jinglebells". It sounds horrible, but it gets the job done as the user will most likely be tempted to release the button. 

### Preparing the Pico W

You need to update the firmware of the Pico W to enable support for MicroPython, but don't worry. It's really easy. 

Hold down the BOOTSEL button on the controller when you plug in the USB cable into the computer and it will load as a mass storage device, which means you can browse to it using your file explorer (e.g. Explorer on Windows, Finder on Mac). Release the button if you're still holding it down.

In the root folder of the device you simply drop in the firmware that can be downloaded from the [micropython website](https://micropython.org/download/rp2-pico-w). 

The device will reboot and flash the new firmare automatically. Wait for a bit and then unplug and plug it in again. You are now ready to program it with MicroPython. 

##### Uh-oh, it's not responding anymore?!

If the device gets stuck in an infinite loop (it can happen to the best of us) or simply refuses to connect for some other unknown reason. Disconnect the device, hold down the BOOTSEL button, plug it in and then drop in a firmware that "nukes" the device.

The firmware can be downloaded from [here](https://datasheets.raspberrypi.com/soft/flash_nuke.uf2).

Don't worry, the name is scarier than it has to be. It just resets the device. You then have to reflash it with the MicroPython firmware. 

#### IDE / Development environment

I ran Windows 11 and used [Visual Studio Code](https://code.visualstudio.com/) with the Pymakr Extension to program the device and transfer code to the device. USB-cable is included in the starter kit from Electrokit. If you're using your own cable, make sure it has a data connection and is not just a charging cable. 

You might want to consider getting the official Python and Pylance extensions for VS Code too. They help with writing code, but beware that they are not perfect for MicroPython and will give you faulty errors on e.g. the machine library, which is normally not part of Python. 

I created this repository on GitHub where I can track code changes and have an online backup of my work. 

You also need to install Node.js too to make it all work: [Node.js (LTS)](https://nodejs.org/en/)

#### Local server (Home Assistant)

I currently have a [Home Assistant](https://www.home-assistant.io/) setup in my home that runs on an Intel NUC and control everything from curtains to lights and speakers, along with monitoring my solar panels, heatpump and other things related to my home. 

I have been running it for many years now and if you don't know what Home Assistant is I highly encourage you to check it out. It has saved me many hours and lots of energy (both mental and electrical) by automating a lot of boring stuff.

There is an [online demo you can try](https://demo.home-assistant.io/#/lovelace/home).

### Wiring up the Pico W

The pin setup I decided to go with are as follows (set up in main.py). The Pico W has limited amount of analog pins so you need to plan your pin usage accordingly. 

```python
# Joystick
xAxisPin = ADC(Pin(28))
yAxisPin = ADC(Pin(27))
buttonPin = Pin(20,Pin.IN, Pin.PULL_UP)

# Light sensor
ldr = ADC(Pin(26))

# DHT
dhtSensor = dht.DHT11(machine.Pin(19))

# Speaker
buzzer = PWM(Pin(22))
```

![Project pin diagram](images/Connections%20overview.png?raw=true "Project pin diagram")
*Project pin diagram. The buzzer and DHT sensor is reversed on this diagram compared to the dev product pictured down below.*


Make sure to reference the [official pin diagram for the Pico W](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf) to make sure this matches with your hardware. Revisions do happen, although seldom with Raspberry products. 


| GPIO pin | Physical pin | Device       |
|----------|--------------|--------------|
|    28    |      34      | xAxisPin     |
|    27    |      32      | yAxisPin     |
|    26    |      31      | light sensor |
|    22    |      29      | buzzer       |
|    20    |      26      | buttonPin    |
|    19    |      25      | DHT-sensor   |


![Picture of the gadget](images/PXL_20240618_121147509.MP~2.jpg?raw=true "The Gadget")
*The gadget in its most basic form*

## Pico W code

Below I have shared a couple of code samples that are key to the project. If you want the full code you can check the files at the top of the page or scroll a bit further and you can view the content there. 

All MQTT code is based on this repository:
https://github.com/iot-lnu/pico-w/tree/main/network-examples/N2_WiFi_MQTT_Webhook_Adafruit

WiFi code is based on this repository:
https://github.com/iot-lnu/pico-w/tree/main/network-examples/N1_WiFi_Connection

### Code samples

Here is the code that connects to the MQTT server and then runs a loop in which we can both receive and send messages.

```python
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
```


This is the receiver function of the MQTT flow. It checks the MQTT server for messages and extracts the message and topic, when there is one. 

At the moment this is only used for the Easter egg since I don't need the device to act on anything else yet.

```python
# Callback Function to respond to messages from the MQQT server
def sub_cb(topic, msg):                         # sub_cb means "callback subroutine"
    print((topic, msg))                         # Outputs the message that was received. Debugging use.
    if  msg == b"XMAS":                         # If msg is XMAS
        playsong(song)                          # ... then play Jingle Bells
    else:                                       # If any other message is received ...
        print(msg)                # ... do nothing but output that it happened.

```

Below is a portion of the code that sends messages to the MQTT server. The light resistor readings are read from the Pico W and sent to the MQTT server. 

The code looks about the same for all sensors, and the joystick. I should try to refactor the code later to make it more efficient. 

```python
def send():
  ...
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
  ...
```

### Full code

Click the filename to expand the segment and show the content of the file.

The project structure was as follows in my case. 

<details>
  <summary>lib/wifiConnection.py (click to expand)</summary>
  
  ```python
  #Original code: https://github.com/iot-lnu/pico-w/tree/main/network-examples/N1_WiFi_Connection

import keys
import network
from time import sleep

def connect():
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
    if not wlan.isconnected():                  # Check if already connected
        print('connecting to network...')
        wlan.active(True)                       # Activate network interface
        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm = 0xa11140)
        wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)  # Your WiFi Credential
        print('Waiting for connection...', end='')
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            sleep(1)
    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    return ip

def disconnect():
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
    wlan.disconnect()
    wlan = None 
  ```
</details>

<details>
  <summary>lib/keys.py (click to expand)</summary>

  ```python
  WIFI_SSID      = "name of your 2.4GHz WIFI"
  WIFI_PASS      = "password to your 2.4GHz WiFi"

  MQTT_BROKER    = "address to your broker"
  MQTT_USER      = "broker username"
  MQTT_PASSWORD  = "broker password"
  MQTT_PORT      = "broker port, usually 1883 or 8883 with SSL enabled"
```

Make sure you add the file to your .gitignore so you don't push it to your repository. 
</details>


<details>
  <summary>boot.py (click to expand)</summary>

```python
# boot.py -- run on boot-up

import wifiConnection

def http_get(url = 'http://detectportal.firefox.com/'):
    import socket                           # Used by HTML get request
    import time                             # Used for delay
    _, _, host, path = url.split('/', 3)    # Separate URL request
    addr = socket.getaddrinfo(host, 80)[0][-1]  # Get IP address of host
    s = socket.socket()                     # Initialise the socket
    s.connect(addr)                         # Try connecting to host address
    # Send HTTP request to the host with specific path
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))    
    time.sleep(1)                           # Sleep for a second
    rec_bytes = s.recv(10000)               # Receve response
    print(rec_bytes)                        # Print the response
    s.close()                               # Close connection

# WiFi Connection
try:
    ip = wifiConnection.connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

# HTTP request
try:
    http_get()
except (Exception, KeyboardInterrupt) as err:
    print("No Internet", err)

```

</details>

<details>
  <summary>main.py (click to expand)</summary>

```python
import micropython            # Needed to run any MicroPython code
import machine                # Interfaces with hardware components
from machine import Pin, ADC  # Define pin and ADC
import time                   # Allows use of time.sleep() for delays
from lib.keys import *        # Secrets
from music import *           # imports the song stuff
import ubinascii              # Conversions between binary data and various encodings
import random                 # Random number generator
from mqtt import MQTTClient   # For use of MQTT protocol to talk to Adafruit IO
import dht                    # For the DHT temp and humidity sensor

# BEGIN SETTINGS
# These need to be change to suit your environment
RANDOMS_INTERVAL = 20000    # milliseconds
last_random_sent_ticks = 0  # milliseconds
led = Pin("LED", Pin.OUT)   # led pin initialization for Raspberry Pi Pico W

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

# Callback Function to respond to messages from the MRTT server
def sub_cb(topic, msg):                         # sub_cb means "callback subroutine"
    print((topic, msg))                         # Outputs the message that was received. Debugging use.
    if  msg == b"XMAS":                         # If topic is XMAS and message says "YES" ...
        playsong(song)                          # ... then play Jingle Bells
    else:                                       # If any other message is received ...
        print("Unknown message")                # ... do nothing but output that it happened.

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
```
</details>

<details>
  <summary>mqtt.py (click to expand)</summary>

```python
#Original code: https://github.com/iot-lnu/pico-w/tree/main/network-examples/N2_WiFi_MQTT_Webhook_Adafruit

import usocket as socket
import ustruct as struct
from ubinascii import hexlify

class MQTTException(Exception):
    pass

class MQTTClient:

    def __init__(self, client_id, server, port=0, user=None, password=None, keepalive=0,
                 ssl=False, ssl_params={}):
        if port == 0:
            port = 8883 if ssl else 1883
        self.client_id = client_id
        self.sock = None
        self.addr = socket.getaddrinfo(server, port)[0][-1]
        self.ssl = ssl
        self.ssl_params = ssl_params
        self.pid = 0
        self.cb = None
        self.user = user
        self.pswd = password
        self.keepalive = keepalive
        self.lw_topic = None
        self.lw_msg = None
        self.lw_qos = 0
        self.lw_retain = False

    def _send_str(self, s):
        self.sock.write(struct.pack("!H", len(s)))
        self.sock.write(s)

    def _recv_len(self):
        n = 0
        sh = 0
        while 1:
            b = self.sock.read(1)[0]
            n |= (b & 0x7f) << sh
            if not b & 0x80:
                return n
            sh += 7

    def set_callback(self, f):
        self.cb = f

    def set_last_will(self, topic, msg, retain=False, qos=0):
        assert 0 <= qos <= 2
        assert topic
        self.lw_topic = topic
        self.lw_msg = msg
        self.lw_qos = qos
        self.lw_retain = retain

    def connect(self, clean_session=True):
        self.sock = socket.socket()
        self.sock.connect(self.addr)
        if self.ssl:
            import ussl
            self.sock = ussl.wrap_socket(self.sock, **self.ssl_params)
        msg = bytearray(b"\x10\0\0\x04MQTT\x04\x02\0\0")
        msg[1] = 10 + 2 + len(self.client_id)
        msg[9] = clean_session << 1
        if self.user is not None:
            msg[1] += 2 + len(self.user) + 2 + len(self.pswd)
            msg[9] |= 0xC0
        if self.keepalive:
            assert self.keepalive < 65536
            msg[10] |= self.keepalive >> 8
            msg[11] |= self.keepalive & 0x00FF
        if self.lw_topic:
            msg[1] += 2 + len(self.lw_topic) + 2 + len(self.lw_msg)
            msg[9] |= 0x4 | (self.lw_qos & 0x1) << 3 | (self.lw_qos & 0x2) << 3
            msg[9] |= self.lw_retain << 5
        self.sock.write(msg)
        #print(hex(len(msg)), hexlify(msg, ":"))
        self._send_str(self.client_id)
        if self.lw_topic:
            self._send_str(self.lw_topic)
            self._send_str(self.lw_msg)
        if self.user is not None:
            self._send_str(self.user)
            self._send_str(self.pswd)
        resp = self.sock.read(4)
        assert resp[0] == 0x20 and resp[1] == 0x02
        if resp[3] != 0:
            raise MQTTException(resp[3])
        return resp[2] & 1

    def disconnect(self):
        self.sock.write(b"\xe0\0")
        self.sock.close()

    def ping(self):
        self.sock.write(b"\xc0\0")

    def publish(self, topic, msg, retain=False, qos=0):
        pkt = bytearray(b"\x30\0\0\0")
        pkt[0] |= qos << 1 | retain
        sz = 2 + len(topic) + len(msg)
        if qos > 0:
            sz += 2
        assert sz < 2097152
        i = 1
        while sz > 0x7f:
            pkt[i] = (sz & 0x7f) | 0x80
            sz >>= 7
            i += 1
        pkt[i] = sz
        #print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.write(pkt, i + 1)
        self._send_str(topic)
        if qos > 0:
            self.pid += 1
            pid = self.pid
            struct.pack_into("!H", pkt, 0, pid)
            self.sock.write(pkt, 2)
        self.sock.write(msg)
        if qos == 1:
            while 1:
                op = self.wait_msg()
                if op == 0x40:
                    sz = self.sock.read(1)
                    assert sz == b"\x02"
                    rcv_pid = self.sock.read(2)
                    rcv_pid = rcv_pid[0] << 8 | rcv_pid[1]
                    if pid == rcv_pid:
                        return
        elif qos == 2:
            assert 0

    def subscribe(self, topic, qos=0):
        assert self.cb is not None, "Subscribe callback is not set"
        pkt = bytearray(b"\x82\0\0\0")
        self.pid += 1
        struct.pack_into("!BH", pkt, 1, 2 + 2 + len(topic) + 1, self.pid)
        #print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.write(pkt)
        self._send_str(topic)
        self.sock.write(qos.to_bytes(1, 'little'))
        while 1:
            op = self.wait_msg()
            if op == 0x90:
                resp = self.sock.read(4)
                #print(resp)
                assert resp[1] == pkt[2] and resp[2] == pkt[3]
                if resp[3] == 0x80:
                    raise MQTTException(resp[3])
                return

    # Wait for a single incoming MQTT message and process it.
    # Subscribed messages are delivered to a callback previously
    # set by .set_callback() method. Other (internal) MQTT
    # messages processed internally.
    def wait_msg(self):
        res = self.sock.read(1)
        self.sock.setblocking(True)
        if res is None:
            return None
        if res == b"":
            raise OSError(-1)
        if res == b"\xd0":  # PINGRESP
            sz = self.sock.read(1)[0]
            assert sz == 0
            return None
        op = res[0]
        if op & 0xf0 != 0x30:
            return op
        sz = self._recv_len()
        topic_len = self.sock.read(2)
        topic_len = (topic_len[0] << 8) | topic_len[1]
        topic = self.sock.read(topic_len)
        sz -= topic_len + 2
        if op & 6:
            pid = self.sock.read(2)
            pid = pid[0] << 8 | pid[1]
            sz -= 2
        msg = self.sock.read(sz)
        self.cb(topic, msg)
        if op & 6 == 2:
            pkt = bytearray(b"\x40\x02\0\0")
            struct.pack_into("!H", pkt, 2, pid)
            self.sock.write(pkt)
        elif op & 6 == 4:
            assert 0

    # Checks whether a pending message from server is available.
    # If not, returns immediately with None. Otherwise, does
    # the same processing as wait_msg.
    def check_msg(self):
        self.sock.setblocking(False)
        return self.wait_msg()
```

</details>

<details>
  <summary>music.py (click to expand)</summary>

```python
#original code: https://github.com/iot-lnu/pico-w/blob/main/sensor-examples/P19_Passive_Piezo_Buzzer

from machine import Pin, PWM
from time import sleep

buzzer = PWM(Pin(22))

tones = {
    'C0':16,
    'CS0':17,
    'D0':18,
    'DS0':19,
    'E0':21,
    'F0':22,
    'FS0':23,
    'G0':24,
    'GS0':26,
    'A0':28,
    'AS0':29,
    'B0':31,
    'C1':33,
    'CS1':35,
    'D1':37,
    'DS1':39,
    'E1':41,
    'F1':44,
    'FS1':46,
    'G1':49,
    'GS1':52,
    'A1':55,
    'AS1':58,
    'B1':62,
    'C2':65,
    'CS2':69,
    'D2':73,
    'DS2':78,
    'E2':82,
    'F2':87,
    'FS2':92,
    'G2':98,
    'GS2':104,
    'A2':110,
    'AS2':117,
    'B2':123,
    'C3':131,
    'CS3':139,
    'D3':147,
    'DS3':156,
    'E3':165,
    'F3':175,
    'FS3':185,
    'G3':196,
    'GS3':208,
    'A3':220,
    'AS3':233,
    'B3':247,
    'C4':262,
    'CS4':277,
    'D4':294,
    'DS4':311,
    'E4':330,
    'F4':349,
    'FS4':370,
    'G4':392,
    'GS4':415,
    'A4':440,
    'AS4':466,
    'B4':494,
    'C5':523,
    'CS5':554,
    'D5':587,
    'DS5':622,
    'E5':659,
    'F5':698,
    'FS5':740,
    'G5':784,
    'GS5':831,
    'A5':880,
    'AS5':932,
    'B5':988,
    'C6':1047,
    'CS6':1109,
    'D6':1175,
    'DS6':1245,
    'E6':1319,
    'F6':1397,
    'FS6':1480,
    'G6':1568,
    'GS6':1661,
    'A6':1760,
    'AS6':1865,
    'B6':1976,
    'C7':2093,
    'CS7':2217,
    'D7':2349,
    'DS7':2489,
    'E7':2637,
    'F7':2794,
    'FS7':2960,
    'G7':3136,
    'GS7':3322,
    'A7':3520,
    'AS7':3729,
    'B7':3951,
    'C8':4186,
    'CS8':4435,
    'D8':4699,
    'DS8':4978,
    'E8':5274,
    'F8':5588,
    'FS8':5920,
    'G8':6272,
    'GS8':6645,
    'A8':7040,
    'AS8':7459,
    'B8':7902,
    'C9':8372,
    'CS9':8870,
    'D9':9397,
    'DS9':9956,
    'E9':10548,
    'F9':11175,
    'FS9':11840,
    'G9':12544,
    'GS9':13290,
    'A9':14080,
    'AS9':14917,
    'B9':15804
}


#JingleBells: https://onlinesequencer.net/1973173
song = ["G5","P","G5","P","G5","P","G5","P","G5","P","G5","P","G5","C6","C5","E5","G5","A5","P","A5","P","A5","P","A5","P","A5","G5","P","G5","P","C6","P","C6","G5","E5","C5","C6"]

def playtone(frequency):
    buzzer.duty_u16(1000)
    buzzer.freq(frequency)

def bequiet():
    buzzer.duty_u16(0)

def playsong(mysong):
    for i in range(len(mysong)):
        if (mysong[i] == "P"):
            bequiet()
        else:
            playtone(tones[mysong[i]])
        sleep(0.3)
    bequiet()
```

</details>

## Home Assistant code

### MQTT sensors in Home Assistant

This is how I set up my MQTT sensors in Home Assistant. I used the default Mosquitto broker add-on found in Home Assistant. It requires minimal settings to set up and I will refer to the [official documentation](https://www.home-assistant.io/integrations/mqtt/) for how to set it up.

File: mqtt.yaml
```yaml
sensor:
  - name: "Gadget: Random"
    state_topic: "homeassistant/gadget/random"
    state_class: measurement
    unit_of_measurement: Null

  - name: "Gadget: Curtains"
    state_topic: "homeassistant/gadget/curtains"

  - name: "Gadget: Light"
    state_topic: "homeassistant/gadget/light"
    state_class: measurement
    unit_of_measurement: "%"

  - name: "Gadget: Temperature"
    state_topic: "homeassistant/gadget/temp"
    state_class: measurement
    unit_of_measurement: "°C"

  - name: "Gadget: Humidity"
    state_topic: "homeassistant/gadget/humidity"
    state_class: measurement
    unit_of_measurement: "%"
```

### Automations in Home Assistant:

When the gadget gets presence control the automations will be updated to handle the room location via variables, which means the barebone code will be the same. It will just trigger different entities depending on the room.  

#### Gadget: when button is pressed

```yaml
alias: "Gadget: button pressed"
description: ""
trigger:
  - platform: mqtt
    topic: homeassistant/gadget/curtains
    payload: button_pressed
condition: []
action:
  - service: counter.increment
    metadata: {}
    data: {}
    target:
      entity_id: counter.gadget_button_press
  - service: mqtt.publish
    metadata: {}
    data:
      qos: "2"
      retain: false
      topic: homeassistant/gadget
      payload: XMAS
mode: single
```


#### Gadget: close curtain
```yaml
alias: "Gadget: Close curtain"
description: ""
trigger:
  - platform: state
    entity_id:
      - sensor.gadget_curtains
    to: down
condition: []
action:
  - service: cover.close_cover
    target:
      entity_id: cover.flush_shutter_dc_2
    data: {}
mode: single
```
#### Gadget: open curtain
```yaml
alias: "Gadget: Open curtain"
description: ""
trigger:
  - platform: state
    entity_id:
      - sensor.gadget_curtains
    to: up
condition: []
action:
  - service: cover.open_cover
    target:
      entity_id:
        - cover.flush_shutter_dc_2
mode: single
```
#### Gadget: Turn off lights
```yaml
alias: "Gadget: Turn off lights"
description: ""
trigger:
  - platform: numeric_state
    entity_id:
      - sensor.gadget_light
    above: 60
condition: []
action:
  - service: light.turn_off
    target:
      entity_id: light.biblioteket_spots
mode: single
```
#### Gadget: Turn on lights
```yaml
alias: "Gadget: Turn on light"
description: ""
trigger:
  - platform: numeric_state
    entity_id:
      - sensor.gadget_light
    below: 40
condition: []
action:
  - service: light.turn_on
    target:
      entity_id: light.biblioteket_spots
mode: single
```

## Visualisation:

I laborated with both InfluxDB and Grafana. They are both available as addons in Home Assistant, which means they install with the push of a button and you are up and running in a minute or so. 

The InfluxDB can be a bit finnicky though and I had to force include my sensors to get them to show up, as shown below.

file: configuration.yaml
```yaml
influxdb:
  host: a0d7b954-influxdb
  port: 8086
  database: homeassistant
  username: homeassistant
  password: <your password>
  max_retries: 3
  default_measurement: state
  include:
    entities:
      - sensor.gadget_random
      - sensor.gadget_curtains
      - sensor.gadget_light
      - sensor.gadget_humidity
      - counter.gadget_button_press
```

Since Grafana connects to InfluxDB any issues with InfluxDB transfers over to Grafana. 

I finally decided that it would be less complex and I would achieve pretty much the same end result, if not better, by just creating a new dashboard in Home Assistant and use some custom graph cards. Specifically I used the [Apex Graph card](https://github.com/RomRider/apexcharts-card) by RomRider.

Screenshots from different solutions I tried out to visualize the sensor data:

![InfluxDB Screenshot](images/Skärmbild%202024-06-19%20193205.png?raw=true "InfluxDB screenshot")
*InfluxDB screenshot*

![Grafana Screenshot](images/Skärmbild%202024-06-19%20193349.png?raw=true "Grafana screenshot")
*Grafana screenshot*

![Home Assistant Dashboard](images/Skärmbild%202024-06-19%20192531.png "Home Assistant Dashboard")
*Home Assistant Dashboard*

### Custom apex graph card code:
```yaml
type: custom:apexcharts-card
graph_span: 2h
header:
  show: true
  title: 'Gadget: Humidity sensor'
  show_states: true
  colorize_states: true
series:
  - entity: sensor.gadget_humidity
    type: line
    stroke_width: 2
    fill_raw: last
    color: pink
yaxis:
  - min: 0
    max: 100

```

## Todo later:

 * Battery power the device
 * Presence detection
   * Write a bunch of automation code in Home Assistant and learn to use variables in automations so I don't have to write one per room...
  
And probably more things as I come up with new ideas.
