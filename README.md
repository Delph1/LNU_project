## LNU Gadget for course 24ST - 1DT305 - Tillämpad Internet of Things, Introduktion - 7,5 hp at LInnaeus University in Kalmar. 

### Background

I took a summer course over the summer of 2024 at Linneaus University where we got to build our own IoT device. I decided to go with a sort of personal gadget, inspired by the [Aqara Cube](https://www.aqara.com/us/product/cube/) and similar such "odd" devices that also works as a sort of remote control. 

The gadget is built up on the Raspberry Pico W. Documentation can be found here at the [official website](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)

The Raspberry and sensors used for this project was purchased from [electrokit.com](https://www.electrokit.com). They even have course specific kits you can buy that works well with the course.

 - [LNU Starter kit](https://www.electrokit.com/lnu-starter)
 - [25 sensor kit package](electrokit.com/sensor-kit-25-moduler)
 - [Addon Kit (if you want to use LoraWan)](https://www.electrokit.com/lnu-addon)

The university also has a repository with lots of code samples, which this projects has been based on: [IoT-LNU/Pico W](https://github.com/iot-lnu/pico-w/)

### Project descriptions

Since the course only ran over five weeks during the summer I had limited time to complete the device. 

My initial scope for the finished device was this:

A gadget equipped with sensors that automatically triggers automations in my existing Home Assistant setup, but also offer some manual input to control things. The gadget will (eventually) have a presence control thanks to its BLE component. 

The presence control will (eventually be based on my existing Google/Nest Home devices which are present in most rooms of the house. I will start off using code by Sean Green from this repository: [Room presence with Google Homes](]https://github.com/seangreen2/home_assistant/wiki/Room-Presence-with-Google-Homes)

However the room presence is essentially all built inside of Home Assistant thus I did not focus on completing it for now. It would also require me to make the gadget movable and battery-powered, which I currently do no have the hardware for. 

The presence would allow the device, or rather Home Assistant, to react differently depending on which room it is in. E.g. in a bedroom it would allow me to control the bedroom curtains and start playing relaxing sounds on the speaker, while in the living room it would make it possible to close those curtains and start up cinema mode instead. 

This is something I will have to complete after the course has completed. 

### So what did I ACTUALLY do?

I decided between a couple of different sensors, but decided to go with the light sensor first of all. 

...

### Easter egg. 

I had to some kind of fun side thing too so I added a passive buzzer that allows for playing music (if you can call it that) on the Pico W. Inside Home Assistant that is an automation that checks if the button is pressed for too long, and thus increase the value of the sensor, it sends out an MQTT message called "XMAS", which makes the buzzer play a short version of "Jinglebells". It sounds horrible, but it gets the job done.
