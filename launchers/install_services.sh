# Services
sudo cp flormiga_python.service /etc/systemd/system/
sudo systemctl enable flormiga_python.service
sudo systemctl start flormiga_python.service

sudo cp flormiga_pd.service /etc/systemd/system/
sudo systemctl enable flormiga_pd.service
sudo systemctl start flormiga_pd.service