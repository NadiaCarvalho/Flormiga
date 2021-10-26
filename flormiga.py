#!/usr/bin/env python3
import time

import board
import digitalio
import busio

from adafruit_seesaw.seesaw import Seesaw
from digitalio import DigitalInOut, Direction, Pull


# Adafruit  STEMMA  Soil  Sensor :
# (1) valor de capacitância
# (2) valor de temperatura

i2c_bus = busio.I2C(board.SCL, board.SDA)
soil_sensor = Seesaw(i2c_bus, addr=0x36)

# Photo-conductive cell:
# (3) brightness/valor de resistência

RCpin = board.D17

def read_photocell(pin):
    with DigitalInOut(pin) as rc:
        reading = 0

        # setup pin as output and direction low value
        rc.direction = Direction.OUTPUT
        rc.value = False

        time.sleep(0.1)

        # setup pin as input and wait for low value
        rc.direction = Direction.INPUT

        # This takes about 1 millisecond per loop cycle
        while rc.value is False:
            reading += 1
        return reading

# (4) Returns 1 if button pressed and 0 otherwise

BTpin = board.D23

def read_button(pin):
    with DigitalInOut(pin) as btn:
        btn.direction = Direction.INPUT
        btn.pull = Pull.UP

        print(btn.value)

        if not btn.value:
            print('down')
            return 1
        else:
            print('up')
            return 0

# (5) Returns 1 if switch activated and 0 otherwise

SWpin = board.D25

def read_switch(pin):
    with DigitalInOut(pin) as swt:
        swt.direction = Direction.INPUT
        swt.pull = Pull.UP

        if not swt.value:
            return 1
        else:
            return 0

# (6) percentagem ou na verdade basta um sinal (0/1 p.ex) que a bateria está abaixo de 8%

import psutil

def get_battery_percentage():
    battery = psutil.sensors_battery()

    plugged = True
    percent = 100
    if battery:
        plugged = battery.power_plugged
        percent = battery.percent

    return 1 if not plugged and percent < 8 else 0

# Setup SEND to pd
from pythonosc import udp_client

#'IP'
ip = '127.0.0.1'
port = 3001

client = udp_client.SimpleUDPClient(ip, port)

while True:
    # read the soil moisture level through capacitive touch pad (1)
    touch = soil_sensor.moisture_read()

    # read temperature from the soil temperature sensor (2)
    temp = soil_sensor.get_temp()

    # read brightness from photocell (3)
    photocell = read_photocell(RCpin)

    # Voltage (4)
    button = read_button(BTpin)

    # Voltage (5)
    switch = 0 #read_switch(SWpin)

    # Battery (6) -> 1: low battery, 0: either pi is plugged or has good battery
    battery_signal = get_battery_percentage()

    # If you want to see information being sent in the terminal, uncomment the following line
    print("Info => capacitance: {}, temperature: {}, brightness: {}, button: {}, switch: {}, battery: {}.".format(
        str(touch), str(temp), str(photocell), str(button), str(switch), str(battery_signal)
    ))

    client.send_message("/capacitance", touch)
    client.send_message("/temperature", temp)
    client.send_message("/brightness", photocell)
    client.send_message("/button", button)
    client.send_message("/switch", switch)
    client.send_message("/battery", battery_signal)

    time.sleep(1)
