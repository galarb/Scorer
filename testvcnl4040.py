from vcnl4040 import VCNL4040
from time import sleep
sensor = VCNL4040()
while True:
    prox = sensor.read_proximity()
    lux = sensor.read_lux_raw()
    print(f"Proximity: {prox}, Lux Raw: {lux}")
    sleep(0.5)

