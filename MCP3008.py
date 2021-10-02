#MCP3008.py

from spidev import SpiDev

#modified a bit from the original, original class in tutorial.

class MCP3008:
    channel = 0
	def __init__(self, _channel, bus = 0, device = 0):
		self.bus, self.device = bus, device
        self.channel = _channel
		self.spi = SpiDev()
		self.open()
		self.spi.max_speed_hz = 1000000 #1MHz

	def open(self):
		self.spi.open(self.bus, self.device)
		self.spi.max_speed_hz = 1000000 #1MHz

	def read(self):
		adc = self.spi.xfer2([1, (8 + self.channel) << 4, 0])
		data = ((adc[1] & 3) << 8) + adc[2]
		return data

	def close(self):
		self.spi.close()