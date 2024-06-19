# Home Control Gadget

For course 24ST - 1DT305 - Tillämpad Internet of Things, Introduktion - 7,5 hp at Linnaeus University in Kalmar. 
Andreas Galistel (ag22fi)

## Table of content
- [Home Control Gadget](#home-control-gadget)
  - [Table of content](#table-of-content)
  - [Background](#background)
    - [Objective](#objective)
    - [Hardware and software](#hardware-and-software)
      - [Hardware](#hardware)
        - [Uh-oh, it's not responding anymore?!](#uh-oh-its-not-responding-anymore)
      - [IDE / Development environment](#ide--development-environment)
      - [Local server (Home Assistant)](#local-server-home-assistant)
  - [Project descriptions and out of scope](#project-descriptions-and-out-of-scope)
    - [So what did I ACTUALLY do?](#so-what-did-i-actually-do)
      - [Pin setup](#pin-setup)
      - [Secret stuff](#secret-stuff)
    - [Easter egg](#easter-egg)
  - [Home Assistant code](#home-assistant-code)
    - [MQTT sensors in Home Assistant](#mqtt-sensors-in-home-assistant)
    - [Automations in Home Assistant:](#automations-in-home-assistant)
      - [Gadget: when button is pressed](#gadget-when-button-is-pressed)
      - [Gadget: close curtain](#gadget-close-curtain)
      - [Gadget: open curtain](#gadget-open-curtain)
      - [Gadget: Turn off lights](#gadget-turn-off-lights)
      - [Gadget: Turn on lights](#gadget-turn-on-lights)
  - [Time needed](#time-needed)
  - [Visualisation:](#visualisation)
  - [Todo later:](#todo-later)


## Background

### Objective
 The objective of this course is to build a personal gadget that would enable automation of my home on another level. It was inspired by the [Aqara Cube](https://www.aqara.com/us/product/cube/) and similar such "odd" devices that also works as a sort of remote control, but don't look or act like the usual kind of control device. 

 These devices usually require manual input though, while my device is intended to mainly use sensors and react on the sensored values. I want to press as few buttons as possible. but that option should be there if necessary. 

 The idea is to improve quality of life by further enabling automations that will adjust lights, curtains and give notifications based on the sensory data. However all of this is not possible within the short timeframe of this course.

 The MVP (minimum viable product) was intended to use a light sensor and joystick. It will connect via WiFi to an MQTT server within Home Assistant. 

 I managed to do a bit more than that though. I added a temperature and humidity sensor along with a speaker that is mainly used as an Easter egg for now, but hopefully I can use it for other type of notifications later on.   

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

You might want to consider getting the official Python and Pylance extensions too. They help with writing code, but beware that they are not perfect for MicroPython and will give you faulty errors on e.g. the machine library, which is normally not part of Python. 

I also created this repository on GitHub where I can track code changes and have an online backup of my work. 

You also need to install Node.js too to make it all work: [Node.js (LTS)](https://nodejs.org/en/)

#### Local server (Home Assistant)

I currently have a [Home Assistant](https://www.home-assistant.io/) setup in my home that runs on an Intel NUC and control anything from curtains to lights and speakers, along with monitoring my solar panels, heatpump and other things related to my home. 

I use a variety of protocols including Zigbee, Z-wave and WiFi to control the devices, but that is out of scope for this project. 

I have been running it for many years now and if you don't know what Home Assistant is I highly encourage you to check it out. It has saved me many hours and lots of energy (both mental and electrical) by automating a lot of boring stuff.

There is an [online demo you can try](https://demo.home-assistant.io/#/lovelace/home).

## Project descriptions and out of scope 

Since the course only ran over five weeks during the summer I had limited time to complete the device. 

My initial scope for the finished device was this:

A gadget equipped with sensors that automatically triggers automations in my existing Home Assistant setup, but also offer some manual input. The gadget will (eventually) have a presence control thanks to its BLE component, which allows for automations to trigger differently depending on the room it is in. 

The presence control will be based on my existing Google/Nest Home devices which are present in most rooms of the house. I will start off using code by Sean Green from his repository: [Room presence with Google Homes](]https://github.com/seangreen2/home_assistant/wiki/Room-Presence-with-Google-Homes)

However the room presence is essentially all built inside of Home Assistant thus I did not focus on completing it before the end of the course. It would also require me to make the gadget movable and battery-powered, which I currently do not have the hardware for. 

E.g. in a bedroom it would allow me to control the bedroom curtains and start playing relaxing sounds on the speaker, while in the living room it would make it possible to close those curtains and start up cinema mode instead. 

This is something I will have to do later on. 

### So what did I ACTUALLY do?

I decided between a couple of different sensors, but decided to go with the light sensor for the MVP (minimum viable product) and when I got that working I added on the temperature and humidity sensor. I live nextdoor to a swamp so humidity can be rather excruciating during the summer and there is basically no trees offering shadow to our house. Plenty in the swamp though.  

It should be noted though, that the light sensor that came with a 10k resistor on-board did not work with the sample code. It was confirmed by a teacher's assistant so I had to use the more barebone solution with two two parallell 5k resistors instead ([the second alternative](https://github.com/iot-lnu/pico-w/tree/main/sensor-examples/P23_LDR_Photo_Resistor)).

I also went with the [analog joystick](https://github.com/iot-lnu/pico-w/tree/main/sensor-examples/P16_Joystick) to allow for manual inputs. 
I decided that controling the curtains made sense since I can do that in most rooms and currently they are set to a schedule, but sometimes schedules change on the fly as the sun decide to go full supernova and heat up the Earth like a South Carolina BBQ.

The code is well documented (in my humble opinion) and should be easy for anyone else to reuse. 

#### Pin setup

The pin setup I decided to go with are as follows (from main.py). The Pico W has limited amount of analog sensors so you need to plan your pin usage accordingly. 

```python
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
```

![Project pin diagram](images/Connections%20overview.png?raw=true "Project pin diagram")
*Project pin diagram*


Make sure to reference the [pin diagram for the Pico W](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf) to make sure this matches with your hardware. Revisions do happen, although seldom with Raspberry products. 


| GPIO pin | Physical pin | Device       |
|----------|--------------|--------------|
|    28    |      34      | xAxisPin     |
|    27    |      32      | yAxisPin     |
|    26    |      31      | light sensor |
|    22    |      29      | buzzer       |
|    20    |      26      | buttonPin    |
|    19    |      25      | DHT-sensor   |

#### Secret stuff

What is not in the repository is the keys.py file that is supposed to be in the lib folder.

The content of the keys.py file looks something like this:

```python
WIFI_SSID      = "name of your 2.4GHz WIFI"
WIFI_PASS      = "password to your 2.4GHz WiFi"

MQTT_BROKER    = "address to your broker"
MQTT_USER      = "broker username"
MQTT_PASSWORD  = "broker password"
MQTT_PORT      = "broker port, usually 1883 or 8883 with SSL enabled"
```

Make sure you add the file to your .gitignore so you don't push it to your repository. 

![Picture of the gadget](images/PXL_20240618_121147509.MP~2.jpg?raw=true "The Gadget")
*The gadget in its most basic form*

### Easter egg

Since I had time I had to add some kind of fun side thing too so I added a [passive buzzer](https://github.com/iot-lnu/pico-w/tree/main/sensor-examples/P18_Active_Piezo_Buzzer) that allows for playing music (if you can call it that) on the Pico W. Inside Home Assistant there is an automation that checks if the button is pressed for too long, and thus increase the value of the sensor, it then sends out an MQTT message called "XMAS", which makes the buzzer play a short version of "Jinglebells". It sounds horrible, but it gets the job done as the user will most likely be tempted to release the button. 

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

## Todo later:

 * Battery power the device
 * Presence detection
   * Write a bunch of automation code in Home Assistant and learn to use variables in automations so I don't have to write one per room...
  
And probably more things as I come up with new ideas.
