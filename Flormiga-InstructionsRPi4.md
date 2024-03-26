# Install on RPi4:

1. Install OS and Configurations

- use Raspberry Pi Imager to install [PatchboxOS Image](https://blokas.io/patchbox-os/#patchbox-os-download) (go to settings and setup ssh, wifi, etc...)

- sudo raspi-config
- Select expand_roofts to expand root partition to the whole sd card (otherwise the pi will stop on upgrades, as it doesn't have enough space to update)
- sudo reboot
- sudo apt update && sudo apt upgrade

2. Install Python

- sudo apt-get install -y python3-pip
- sudo pip3 install --upgrade setuptools

3. Install Blinka/Adafruit Libraries

- cd ~
- sudo pip3 install --upgrade adafruit-python-shell
- wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
- sudo python3 raspi-blinka.py
- sudo reboot
- pip3 install --upgrade adafruit-circuitpython-dotstar adafruit-circuitpython-motor adafruit-circuitpython-bmp280

4. Install Amp
(follow https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-usage)

- curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash
- sudo reboot
- curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash
- sudo nano /boot/config.txt
- uncomment (remove '#') of 'dtparam=audio=on'

5. a. Check sensors

- sudo i2cdetect -y 1

(should be like following)

|     | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | a  | b  | c  | d  | e  | f  |
|-----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 00: |    |    |    |    |    |    |    |    | -- | -- | -- | -- | -- | -- | -- | -- |
| 10: | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| 20: | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| 30: | -- | -- | -- | -- | -- | -- | 36 | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| 40: | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| 50: | -- | -- | -- | -- | -- | -- | -- | 57 | -- | -- | -- | -- | -- | -- | -- | -- |
| 60: | -- | -- | -- | -- | -- | -- | -- | -- | UU | -- | -- | -- | -- | -- | -- | -- |
| 70: | -- | -- | -- | -- | -- | -- | -- | -- |    |    |    |    |    |    |    |    |

5. b. Install Adafruit STEMMA Soil Sensor

- pip3 install adafruit-circuitpython-seesaw

6. Install other libraries

8. Install PD

- sudo apt-get install puredata

