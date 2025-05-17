from smbus2 import SMBus
import time

VCNL4040_I2C_ADDR = 0x60

# Register addresses
VCNL4040_ALS_DATA = 0x09        # Ambient Light 16-bit
VCNL4040_PROXIMITY_DATA = 0x08  # Proximity 16-bit
VCNL4040_ALS_CONF = 0x00
VCNL4040_PROX_CONF = 0x03

class VCNL4040:
    def __init__(self, bus=1):
        self.bus = SMBus(bus)
        self.init_sensor()

    def init_sensor(self):
        # ALS: enable, 80ms integration time, continuous conversion
        self.write16(VCNL4040_ALS_CONF, 0x400)
        # Proximity: enable, high duty cycle
        self.write16(VCNL4040_PROX_CONF, 0x1800)

    def read_proximity(self):
        return self.read16(VCNL4040_PROXIMITY_DATA)

    def read_lux_raw(self):
        return self.read16(VCNL4040_ALS_DATA)

    def read16(self, reg):
        data = self.bus.read_i2c_block_data(VCNL4040_I2C_ADDR, reg, 2)
        return data[1] << 8 | data[0]

    def write16(self, reg, value):
        self.bus.write_i2c_block_data(VCNL4040_I2C_ADDR, reg, [value & 0xFF, (value >> 8) & 0xFF])



