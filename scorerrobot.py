from scorer import scorer
from time import sleep
from threading import Thread
from signal import pause
import RPi.GPIO as GPIO

# Initialize scorer
pilot = scorer(10, 22, 17, 27, 5, 6, 19, 13, 21, 20, 16, 12, 8, 7, 24, 23, 18, 4)

# Worker thread function
def robot_loop():
    try:
        while True:
            if pilot.get_modeflag() == 0:
                pilot.govector(0, 0, 0)
                pilot.dribble(0)
            else:
                pilot.joyride()
                pilot.dribble(0)
            sleep(0.1)
    except KeyboardInterrupt:
        print("Stopped by user")
        pilot.stophard()
        GPIO.cleanup()

# Start robot loop in background
t = Thread(target=robot_loop)
t.daemon = True
t.start()

# Keep main thread alive to handle GPIO IRQs
pause()


