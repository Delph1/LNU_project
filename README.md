## LNU Gadget for course 24ST - 1DT305 - Tillämpad Internet of Things, Introduktion - 7,5 hp at LInnaeus University in Kalmar. 

### Background

I took a summer course over the summer of 2024 at Linneaus University where we got to build our own IoT device. I decided to go with a sort of personal gadget, inspired by the [Aqara Cube](https://www.aqara.com/us/product/cube/) and similar such "odd" devices that also works as a sort of remote control. 

The gadget is built up on the Raspberry Pico W. Documentation can be found here at the [official website](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)

The Raspberry Pico W and sensors used for this project was purchased from [electrokit.com](https://www.electrokit.com). They even have course specific kits you can buy that works well with the course.

 - [LNU Starter kit](https://www.electrokit.com/lnu-starter)
 - [25 sensor kit package](electrokit.com/sensor-kit-25-moduler)
 - [Addon Kit (if you want to use LoraWan)](https://www.electrokit.com/lnu-addon)

The university also has a repository with lots of code samples, which this projects has been based on: [IoT-LNU/Pico W](https://github.com/iot-lnu/pico-w/)

### Project descriptions

Since the course only ran over five weeks during the summer I had limited time to complete the device. 

My initial scope for the finished device was this:

A gadget equipped with sensors that automatically triggers automations in my existing Home Assistant setup, but also offer some manual input. The gadget will (eventually) have a presence control thanks to its BLE component, which allows for automations to trigger differently depending on the room it is in. 

The presence control will be based on my existing Google/Nest Home devices which are present in most rooms of the house. I will start off using code by Sean Green from his repository: [Room presence with Google Homes](]https://github.com/seangreen2/home_assistant/wiki/Room-Presence-with-Google-Homes)

However the room presence is essentially all built inside of Home Assistant thus I did not focus on completing it before the end of the course. It would also require me to make the gadget movable and battery-powered, which I currently do not have the hardware for. 

E.g. in a bedroom it would allow me to control the bedroom curtains and start playing relaxing sounds on the speaker, while in the living room it would make it possible to close those curtains and start up cinema mode instead. 

This is something I will have to complete after the course has completed. 

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
    payload: reset
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

## Todo later:

 * Battery power the device
 * Presence detection
   * Write a bunch of automation code in Home Assistant 
  
And probably more things as I come up with new ideas.
