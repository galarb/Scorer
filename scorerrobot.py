from scorer import scorer
from time import sleep
from threading import Thread
from signal import pause
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory

# Initialize scorer 
pilot = scorer(
    motorA_pins=(10, 22, 17, 27),
    motorB_pins=(5, 6, 19, 13),
    kickerdribbler_pins=(16, 12, 20, 21),
    sensor_pins=(24, 23, 18),
    modebutton_pin=4
)


# Worker thread function
def robot_loop():
    try:
        while True:
            if pilot.get_modeflag() == 0:
                pilot.govector(0, 0, 0)
                pilot.dribbler.motgo(0)
                pilot.kickermotor.motgo(0)
                if(pilot.ball_loaded()):
                    print('ball ready')
                sleep(1)
                
            else:
                pilot.start_dribbler(60, duration=2)  # Run dribbler at speed 60 for 2 seconds
                pilot.start_kicker(80, duration=1.5)  # Kick for 1.5 seconds
                sleep(3)
                #pilot.joyride()
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


