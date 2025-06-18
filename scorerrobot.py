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
            mode = pilot.get_modeflag()

            if mode == 0:  # IDLE mode
                pilot.govector(0, 0, 0)
                pilot.dribbler.motgo(0)
                pilot.kickermotor.motgo(0)
                if pilot.ball_loaded():
                    print('ball ready')
                sleep(1)

            elif mode == 1:  # HUNT mode
                # Insert autonomous behavior here
                #print("Hunt behavior running...")
                sleep(3)

            elif mode == 2:  # MANUAL mode
                #print("Manual behavior running...")

                # Manual control handler, probably from mobile
                # pilot.update_from_manual_commands()  ← to be implemented
                pass

            sleep(0.1)

    except KeyboardInterrupt:
        print("Stopped by user")
        pilot.stophard()
        
# Start robot loop in background
t = Thread(target=robot_loop)
t.daemon = True
t.start()

# Keep main thread alive to handle GPIO IRQs
pause()


