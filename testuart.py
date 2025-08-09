import time
from rpiuart import RpiUart

uart = RpiUart()
uart.start()

try:
    while True:
        msg = uart.get_message()
        if msg:
            if msg == "None":
                print("No ball detected")
            else:
                try:
                    x, y, area = map(int, msg.split(','))
                    print(f"Ball: x={x}, y={y}, area={area}")
                except ValueError:
                    print(f"Bad data: {msg}")
        # Your robot’s other tasks here
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Stopping UART listener...")
    uart.stop()

