#!/bin/bash
# run.sh
# navigate to home directory, then to this directory, then execute python script in correct order, than back to home directory

cd /
cd home/pi/self-driving-car/client/app
sleep 3
python3 record.py
sleep 3
python3 main.py
cd /