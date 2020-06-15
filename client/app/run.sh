#!/bin/bash
# run.sh
# navigate to home directory, then to this directory, then execute python script in correct order, than back to home directory

cd /
cd home/pi/self-driving-car/client/app
python3 record.py &
sleep 1
python3 main.py &
cd /