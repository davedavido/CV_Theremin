import time
import Adafruit_MCP4725

# Create a DAC instance.
dac = Adafruit_MCP4725.MCP4725(address = 0x60, busnum = 1)

dac.set_voltage(0) #0=GND 4095=VCC -> 12-Bit