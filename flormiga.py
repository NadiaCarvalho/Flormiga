#!/usr/bin/env python3
import time

import board
import digitalio
import busio

from adafruit_seesaw.seesaw import Seesaw
from digitalio import DigitalInOut, Direction


# Adafruit  STEMMA  Soil  Sensor :
# (1) valor de capacitância
# (2) valor de temperatura

i2c_bus = busio.I2C(board.SCL, board.SDA)
soil_sensor = Seesaw(i2c_bus, addr=0x36)

# Photo-conductive cell:
# (3) brightness/valor de resistência

RCpin = board.D18

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

def analog_voltage(adc):
    return adc.value / 65535 * adc.reference_voltage

# (4)(5) voltagem (assumo que receba só 0/1)

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
# ip = '192.168.1.2'
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
    volt_1 = 0 # analog_voltage()

    # Voltage (5)
    volt_2 = 0 # analog_voltage()

    # Battery (6) -> 1: low battery, 0: either pi is plugged or has good battery
    battery_signal = get_battery_percentage()

    # If you want to see information being sent in the terminal, uncomment the following line
    print("Info => cap: {}, temp: {}, bright: {}, volt_1: {}, volt_2: {}, bat: {}.".format(
        str(touch), str(temp), str(photocell), str(volt_1), str(volt_2), str(battery_signal)
    ))

    client.send_message("/capacitance", touch)
    client.send_message("/temperature", temp)
    client.send_message("/brightness", photocell)
    client.send_message("/volt_1", volt_1)
    client.send_message("/volt_2", volt_2)
    client.send_message("/battery", battery_signal)

    time.sleep(1)
