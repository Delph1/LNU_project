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
  - [Project descriptions](#project-descriptions)
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
  - [Todo later:](#todo-later)


## Background

### Objective
 The objective of this course is to  build a personal gadget that would enable automation of my home on another level. It was inspired by the [Aqara Cube](https://www.aqara.com/us/product/cube/) and similar such "odd" devices that also works as a sort of remote control, but don't look or act like the usual kind of control device. 

 These devices usually require some form of manual input though, while my device is intended to use sensors and just react on the sensored values. I want to press as few buttons as possible. 

 The idea is to improve quality of life by further enabling automations that will adjust lights, curtains and give notifications based on the sensory data. However all of this is not possible within the short timeframe of this course.

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

Hold down the BOOTSEL button on the controller when you plug in the USB cable into the computer and it will load as a mass storage device, which means you can browse to it using your file explorer (e.g. Explorer on Windows, Finder on Mac.). Release the button if you're still holding it down.

In the root folder of the device you simply drop in the firmware that can be downloaded from the [micropython website](https://micropython.org/download/rp2-pico-w). 

The device will reboot and flash the new firmare automatically. Wait for a bit and then unplug and plug it in again. You are now ready to program it with MicroPython. 

##### Uh-oh, it's not responding anymore?!

If the device gets stuck in an infinite loop (it can happen to the best of us) or simply refuses to connect for some other unknown reason. Disconnect the device, hold down the BOOTSEL button, plug it in and then drop in a firmware that "nukes" the device.

The firmware can be downloaded from [here](https://datasheets.raspberrypi.com/soft/flash_nuke.uf2).

Don't worry, the name is scarier than it has to be. It just resets the device. You then have to reflash it with the MicroPython firmware. 

#### IDE / Development environment

I ran Windows 11 and used [Visual Studio Code](https://code.visualstudio.com/) with the Pymakr Extension to program the device and transfer code to the device. USB-cable is included in the starter kit from Electrokit. 

You might want to consider getting the official Python and Pylance extensions too. They help with writing code, but beware that they are not perfect for MicroPython and will give you faulty errors on e.g. the machine library, which is normally not part of Python. 

You also need to install Node.js too to make it work: [Node.js (LTS)](https://nodejs.org/en/)

#### Local server (Home Assistant)

I currently have a [Home Assistant](https://www.home-assistant.io/) setup in my home that runs on an Intel NUC and control anything from curtains to lights and speakers, along with monitoring my solar panels, heatpump and other things related to my home. 

I use a variety of protocols including Zigbee, Z-wave and WiFi to control the devices, but that is out of scope for this project. 

I have been running it for many years now and if you don't know what Home Assistant is I highly encourage you to check it out. It has saved me many hours and lots of energy (both mental and electrical) by automating a lot of boring stuff.

There is an [online demo you can try](https://demo.home-assistant.io/#/lovelace/home).

## Project descriptions

Since the course only ran over five weeks during the summer I had limited time to complete the device. 

My initial scope for the finished device was this:

A gadget equipped with sensors that automatically triggers automations in my existing Home Assistant setup, but also offer some manual input. The gadget will (eventually) have a presence control thanks to its BLE component, which allows for automations to trigger differently depending on the room it is in. 

The presence control will be based on my existing Google/Nest Home devices which are present in most rooms of the house. I will start off using code by Sean Green from his repository: [Room presence with Google Homes](]https://github.com/seangreen2/home_assistant/wiki/Room-Presence-with-Google-Homes)

However the room presence is essentially all built inside of Home Assistant thus I did not focus on completing it before the end of the course. It would also require me to make the gadget movable and battery-powered, which I currently do not have the hardware for. 

E.g. in a bedroom it would allow me to control the bedroom curtains and start playing relaxing sounds on the speaker, while in the living room it would make it possible to close those curtains and start up cinema mode instead. 

This is something I will have to do later on. 

### So what did I ACTUALLY do?

I decided between a couple of different sensors, but decided to go with the light sensor for the MVP (minimum viable product) and when I got that working I added on the temperature and humidity sensor. I live nextdoor to a swamp so humidity can be rather excruciating during the summer and there is basically no trees offering shadow to our house. Plenty in the swamp though.  

It should be noted though, that the light sensor that came with a 10k resistor on-board did not work with the sample code. It was confirmed by a teacher's assistant so I had to use the more barebone solution with two two parallell resistors ([the second alternative](https://github.com/iot-lnu/pico-w/tree/main/sensor-examples/P23_LDR_Photo_Resistor)).

I also went with the [analog joystick](https://github.com/iot-lnu/pico-w/tree/main/sensor-examples/P16_Joystick) to allow for manual inputs. 
I decided that controling the curtains made sense since I can do that in most rooms and currently they are set to a schedule, but sometimes schedules change on the fly as the sun decide to go full supernova and heat up the Earth like a South Carolina BBQ.

The code is well documented (in my humble opinion) and should be easy for anyone else to reuse. 

#### Pin setup

The pin setup I decided to go with are as follows (from main.py). The Pico W has limited amount of analog sensors so you need to plan your pin usage accordingly. 

```

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

![Pin diagram](images/Connections%20overview.png?raw=true "Pin diagram")
*Pin diagram*


Do note that the pin numbers here are the GPIO pin numbers, not the actual pin on the Pico W. You need to look at the [pin diagram](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf) to see which physical pin this corresponds to. 

In my case it was this as of the Summer of 2024, but this could change if the Pico W gets an update or revision in the future:


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

```
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

I had to some kind of fun side thing too so I added a [passive buzzer](https://github.com/iot-lnu/pico-w/tree/main/sensor-examples/P18_Active_Piezo_Buzzer) that allows for playing music (if you can call it that) on the Pico W. Inside Home Assistant that is an automation that checks if the button is pressed for too long, and thus increase the value of the sensor, it sends out an MQTT message called "XMAS", which makes the buzzer play a short version of "Jinglebells". It sounds horrible, but it gets the job done.

## Home Assistant code

### MQTT sensors in Home Assistant

This is how I set up my MQTT sensors in Home Assistant. I used the default Mosquitto broker add-on found in Home Assistant. It requires minimal settings to set up and I will refer to the [official documentation](https://www.home-assistant.io/integrations/mqtt/) for how to set it up.

File: mqtt.yaml
``` 
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

```
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
mode: single
```


#### Gadget: close curtain
```
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
```
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
    data: {}
mode: single
```
#### Gadget: Turn off lights
```
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
    metadata: {}
    data: {}
    target:
      entity_id: light.biblioteket_spots
mode: single
```
#### Gadget: Turn on lights
```
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
    data: {}
    target:
      entity_id: light.biblioteket_spots
mode: single
```
## Time needed

How much experience you have with Python, MQTT and Home Assistant plays a big part, but even with limited experience you should be able to build this device relatively fast. 

If you're some experience, to complete the MVP (minimum viable product) with just the light sensor and WiFi setup you will need a couple of hours. 

If you are not already running [Home Assistant](https://www.home-assistant.io/) that in itself can be a big leap. It is however the most potent, secure and most of all private home automation platform available. It is well worth trying out. 

## Todo later:

 * Battery power the device
 * Presence detection
   * Write a bunch of automation code in Home Assistant 
  
And probably more things as I come up with new ideas.
