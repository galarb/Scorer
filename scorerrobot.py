from scorer import scorer
from time import sleep
from threading import Thread
from signal import pause
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory

# Initialize scorer 
pilot = scorer(10, 22, 17, 27, 5, 6, 19, 13, 21, 20, 16, 12, 8, 7, 24, 23, 18, 4)

# Worker thread function
def robot_loop():
    try:
        while True:
            if pilot.get_modeflag() == 0:
                pilot.govector(0, 0, 0)
                pilot.dribble(0)
                pilot.kick()
                pilot.release()
                print(pilot.ball_loaded())
                sleep(1)
                
            else:
                pilot.joyride()
                #pilot.dribble(80)
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


