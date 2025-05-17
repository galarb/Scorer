import smbus2 as smbus
import time

bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

print("Scanning I2C bus...")

for address in range(0x03, 0x78):  # Valid I2C addresses
    try:
        bus.write_quick(address)
        print(f"Found device at 0x{address:02X}")
    except OSError:
        pass

print("Scan complete.")
