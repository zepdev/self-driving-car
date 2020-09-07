#!/bin/bash
# run.sh
# navigate to home directory, then to this directory, then execute python script in correct order, than back to home directory

cd /
cd home/jetson-nano/self-driving-car/client/app
sudo busybox devmem 0x700031fc 32 0x45
sudo busybox devmem 0x6000d504 32 0x2
sudo busybox devmem 0x70003248 32 0x46
sudo busybox devmem 0x6000d100 32 0x00
python3 record.py &
sleep 1
python3 main.py &
cd /