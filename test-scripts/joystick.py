import inputs
import sys

pads = inputs.devices.gamepads
if len(pads) == 0:
	raise Exception("Could not find Gamepads!")

try:
	while True:
		events = inputs.get_gamepad()
		for event in events:
                        print(f"{event.code}, {event.state}")
			
except KeyboardInterrupt:
	sys.exit()
