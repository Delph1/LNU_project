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