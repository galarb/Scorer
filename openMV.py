import sensor, image, time, pyb
from pyb import UART

# UART to RPi on hardware UART pins (TX=Pin P4, RX=Pin P5 by default)
uart = UART(3, 115200, timeout_char=1000)  # UART3 is pins P4/P5

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

# Narrow LAB color range for white golf ball (adjust as needed)
thresholds = [(50, 100, -12, 12, -12, 3)]  # L A B

while True:
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs(
        thresholds,
        pixels_threshold=100,
        area_threshold=100,
        merge=True
    )

    found_ball = False
    for b in blobs:
        if 200 <= b.area() <= 2300 and 0.9 <= b.w() / b.h() <= 1.1:
            img.draw_rectangle(b.rect())
            img.draw_cross(b.cx(), b.cy())

            # Send as CSV: x,y,area\n
            uart.write("{},{},{}\n".format(b.cx(), b.cy(), b.area()))
            found_ball = True

    if not found_ball:
        uart.write("None\n")

    pyb.delay(200)  # small pause so RPi can read
