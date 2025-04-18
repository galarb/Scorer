from scorer1 import scorer
from time import sleep
import RPi.GPIO as GPIO

pilot = scorer(10, 22, 17, 27, 5, 6, 19, 13)
pilot.govector(20, -20, 0)
#pilot.gomotor(0, 50)
sleep(2)
#pilot.govector(0, 0, 0)

pilot.govector(0, 0, 0)
#test2.motgo(0)
#test3.motgo(0)
#test4.motgo(0)
print('stopped')
GPIO.cleanup()
