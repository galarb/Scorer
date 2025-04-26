from scorer import scorer
from time import sleep
import RPi.GPIO as GPIO

#DOA, D1A, D2A, D3A, DOB, D1B, D2B, D3B, in1_pin, in2_pin, in3_pin, in4_pin, drib1_pin, drib2_pin, RL1_pin, RL2_pin, RL3_pin

pilot = scorer(10, 22, 17, 27, 5, 6, 19, 13, 21, 20, 16, 12, 8, 7, 24, 23, 18)

#pilot.dribble(-50)
for _ in range(10):
    #pilot.govector(10, 10, 10)
    #pilot.gomotor(0, 50)
    #pilot.kick()
    #pilot.dribble(50)
    sleep(2)
    #pilot.govector(10, -10, -10)
    sleep(2)
    #pilot.govector(0, 0, 30)
    sleep(2)
    #pilot.govector(0, 0, -30)
    sleep(2)

pilot.govector(0, 0, 0)

#pilot.govector(0, 0, 0)

#pilot.govector(0, 0, 0)
#test2.motgo(0)
#test3.motgo(0)
#test4.motgo(0)
print('stopped')
GPIO.cleanup()
