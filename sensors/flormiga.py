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

def get_soil_sensor():
    try:
        # read the soil moisture level through capacitive touch pad (1)
        touch = soil_sensor.moisture_read()
        # read temperature from the soil temperature sensor (2)
        temp = soil_sensor.get_temp()
    except:
        touch = 330
        temp = 26.5
    return touch, temp

# Photo-conductive cell:
# (3) brightness/valor de resistência

RCpin = board.D24

def read_photocell(pin):
    with DigitalInOut(pin) as rc:
        reading = 0

        # setup pin as output and direction low value
        rc.direction = Direction.OUTPUT
        rc.value = False

        time.sleep(0.01)

        # setup pin as input and wait for low value
        rc.direction = Direction.INPUT

        # This takes about 1 millisecond per loop cycle
        while rc.value is False:
            reading += 1
        return reading

# (4) Returns 1 if button pressed and 0 otherwise

BTpin = board.D23

def read_button_and_switch(pin):
    with DigitalInOut(pin) as btn:
        btn.direction = Direction.INPUT
        btn.pull = Pull.UP

        if not btn.value:
            return 1
        else:
            return 0

# (5) Returns 1 if switch activated and 0 otherwise

SWpin = board.D25

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

from datetime import datetime
import os

filename = "data.txt"
date_format = '%d-%m-%y %H:%M:%S'

def get_time_date_spent():
    current_date = datetime.now()

    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(current_date.strftime(date_format))
            file.close()
        return 0

    time_spent = 0
    with open(filename, 'r') as file:
        last_date_str = file.readline()
        last_date = datetime.strptime(last_date_str, date_format)
        delta = current_date - last_date
        time_spent = delta.days
        file.close()

    return time_spent

def delete_date_file():
    if os.path.exists(filename):
        os.remove(filename)

# Setup SEND to pd
from pythonosc import udp_client
import sys
#'IP'
ip = '127.0.0.1'
if len(sys.argv) > 1:
    ip = sys.argv[1]

print(f'IP: {ip}')

port = 3001

client = udp_client.SimpleUDPClient(ip, port)

while True:

    # read the soil moisture level through capacitive touch pad (1)
    # read temperature from the soil temperature sensor (2)
    touch, temp = get_soil_sensor()

    # read brightness from photocell (3)
    photocell = read_photocell(RCpin)
    # Voltage (4)
    button = read_button_and_switch(BTpin)
    if button == 1:
        delete_date_file()

    # Voltage (5)
    switch = read_button_and_switch(SWpin)

    # Battery (6) -> 1: low battery, 0: either pi is plugged or has good battery
    battery_signal = get_battery_percentage()

    time_spent = get_time_date_spent()

    # If you want to see information being sent in the terminal, uncomment the following line
    print(f"Info => capacitance: {touch}, temperature: {temp}, brightness: {photocell}, button: {button}, switch: {switch}, battery: {battery_signal}, time: {time_spent}.")

    client.send_message("/capacitance", touch)
    client.send_message("/temperature", temp)
    client.send_message("/brightness", photocell)
    client.send_message("/button", button)
    client.send_message("/switch", switch)
    client.send_message("/battery", battery_signal)
    client.send_message("/time", time_spent)

    time.sleep(0.10)