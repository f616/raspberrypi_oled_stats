#!/usr/bin/python3

# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess
import os 

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
#font = ImageFont.truetype('Minecraft.ttf',14)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # cmd = 'cut -f 1 -d " " /proc/loadavg'
    # CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    # MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    # Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # CPU informatiom
    CPU_temp = getCPUtemperature() + "C"
    CPU_usage = getCPUuse() + "%"

    # RAM information
    # Output is in kb, here I convert it in Mb for readability
    RAM_stats = getRAMinfo()
    RAM_total = round(int(RAM_stats[0]) / 1000,1)
    RAM_used = round(int(RAM_stats[1]) / 1000,1)
    RAM_free = round(int(RAM_stats[2]) / 1000,1)
    RAM_used_perc = str(round((RAM_used / RAM_total)*100, 1)) + "%"

    # print("RAM_used: " + str(RAM_used))
    # print("RAM_total: " + str(RAM_total))
    # print("RAM_used_perc: " + str(RAM_used_perc))


    # Disk information
    DISK_stats = getDiskSpace()
    DISK_total = DISK_stats[0]
    DISK_free = DISK_stats[1]
    DISK_perc = DISK_stats[3]

    # Write four lines of text.

    # draw.text((x, top + 0), IP, font=font, fill=255)
    # draw.text((x, top + 8), "CPU: " + CPU_usage, font=font, fill=255)
    # draw.text((x, top + 16), MemUsage, font=font, fill=255)
    # draw.text((x, top + 25), DISK_perc, font=font, fill=255)

    draw.text((x, top + 0), IP, font=font, fill=255)
    draw.text((x, top + 14), "CPU: " + CPU_usage, font=font, fill=255)
    draw.text((x + 64, top + 14), "MEM: " + RAM_used_perc, font=font, fill=255)
    draw.text((x, top + 24), "TEMP: " + CPU_temp, font=font, fill=255)
    draw.text((x + 64, top + 24), "DISK: " + DISK_perc, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(0.1)
