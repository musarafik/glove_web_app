import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
spi = busio.SPI(clock=board.SCK, MISO = board.MISO, MOSI = board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

finger1 = AnalogIn(mcp, MCP.P0)
finger2 = AnalogIn(mcp, MCP.P1)
finger3 = AnalogIn(mcp, MCP.P2)
finger4 = AnalogIn(mcp, MCP.P3)
finger5 = AnalogIn(mcp, MCP.P4)

print('Reading values on MCP3008, press Ctrl-C to quit')
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} |'.format(*range(5)))
print('-' * 57)
out = open("sensorout.txt", "w")
while True:
	values = [0]*5
	values[0] = finger1.voltage / 1024.0 * 100000 / (1 - finger1.voltage / 1024.0)
	values[1] = finger2.voltage / 1024.0 * 100000 / (1 - finger2.voltage / 1024.0)
	values[2] = finger3.voltage / 1024.0 * 100000 / (1 - finger3.voltage / 1024.0)
	values[3] = finger4.voltage / 1024.0 * 100000 / (1 - finger4.voltage / 1024.0)
	values[4] = finger5.voltage / 1024.0 * 100000 / (1 - finger5.voltage / 1024.0)

	print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} |'.format(*values))
	time.sleep(0.5)
	out.write(str(values[0]) + ", " + str(values[1]) + ", " + str(values[2]) + ", " + str(values[3]) + ", " + str(values[4]) + "\n")
