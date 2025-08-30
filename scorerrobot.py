from scorer import scorer
from time import sleep
from threading import Thread
from signal import pause
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory


# Initialize scorer 
pilot = scorer(
    motorA_pins=(22, 10, 17, 27),
    motorB_pins=(6, 5, 19, 13),
    kickerdribbler_pins=(16, 12, 20, 21),
    sensor_pins=(24, 18, 23),
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
                sleep(0.1)

            elif mode == 1:  # HUNT mode
                if(not pilot.check_cam()):
                    pilot.govector(0, 0, 0)
                #pilot.scan()
                sleep(0.12)

            elif mode == 2:  # MANUAL mode
                pilot.check_joystick()
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




