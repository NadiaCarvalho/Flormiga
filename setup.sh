#!/bin/bash

cd ~
git clone https://github.com/NadiaCarvalho/Flormiga.git
cd Flormiga

# Install PD
sudo apt-get install puredata
sudo apt install pd-cyclone
sudo apt install pd-rtclib

# Install Python dependencies
pip3 install python-osc

# Services
sudo cp flormiga_launcher_python.service /etc/systemd/system/
sudo systemctl enable flormiga_launcher_python.service
sudo systemctl start flormiga_launcher_python.service

sudo cp flormiga_launcher_pd.service /etc/systemd/system/
sudo systemctl enable flormiga_launcher_pd.service
sudo systemctl start flormiga_launcher_pd.service