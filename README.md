# raspberrypi_oled_stats

![image](https://user-images.githubusercontent.com/3826426/129965421-e166138d-b62e-48f7-ab45-9d88600da85d.png)

#### Parts:
* Raspberry Pi 4
* OLED SSD1306 Display I2C IIC 128x32 0.91 4 pin

![image](https://user-images.githubusercontent.com/3826426/130323927-e9a21694-8eaa-49e4-a38a-4e489218c439.png)


#### Connections:
![image](https://user-images.githubusercontent.com/3826426/130324454-ccc9dd0a-bbc4-4e69-a4b6-8ef835b4b4c2.png)


#### How to install  
Highlevel guidelines written by heart. Some steps might be missing, some commands might have the syntax not 100% accurate.  

Python3 must be installed.  

1. getting the files  
```
cd ~  
git clone https://github.com/f616/raspberrypi_oled_stats.git  
cd raspberrypi_oled_stats  
```

2. create and enable the service  
```
cd /usr/bin/  
sudo ln -s ~/raspberrypi_oled_stats/statsdisplay_start.py  
sudo ln -s ~/raspberrypi_oled_stats/statsdisplay_stop.py  
cd /etc/systemd/system/multi-user.target.wants/  
sudo ln -s ~/raspberrypi_oled_stats/statsdisplay.service  
sudo systemctl daemon-reload  
```

To enable the service at start-up:  
```
sudo systemctl enable statsdisplay.service 
```

Start the service command:  
```
sudo service statsdisplay start  
```

Stop the service command:  
```
sudo service statsdisplay stop  
```

Get the service status  
```
sudo service statsdisplay status  
```


#### 40 pin header side extension  
https://oshwlab.com/filipe.neto616/raspberry-pi-40-pin-header-replicator  


#### Based on:  
https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage  
https://www.raspberrypi.org/forums/viewtopic.php?t=22180  
https://learn.sparkfun.com


