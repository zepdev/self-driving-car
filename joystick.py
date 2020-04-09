import inputs
import sys

pads = inputs.devices.gamepads
if len(pads) == 0:
	raise Exception("Could not find Gamepads!")

try:
	while True:
		events = inputs.get_gamepad()
		for event in events:
			#if event.code in ["ABS_Y", "ABS_RX"]:
			#print(event.code, round((event.state+0.5)/32767.5, 1))
			print (event.ev_type, event.code, event.state)
			
except KeyboardInterrupt:
	sys.exit()
