cd Flormiga

# Install Python dependencies
pip3 install -r requirements.txt

# Install PD
sudo apt-get install puredata
sudo apt install pd-cyclone
sudo apt install pd-rtclib

# Services
sudo cp flormiga_launcher_python.service /etc/systemd/system/
sudo systemctl enable flormiga_launcher_python.service
sudo systemctl start flormiga_launcher_python.service

sudo cp flormiga_launcher_pd.service /etc/systemd/system/
sudo systemctl enable flormiga_launcher_pd.service
sudo systemctl start flormiga_launcher_pd.service