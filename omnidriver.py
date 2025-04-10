from machine import Pin, PWM, TouchPad
import neopixel
from time import sleep, ticks_ms
import math
import random
recorded_values = []
recorded_valuesproc = []


class omnidriver:
    def __init__(self, in1, in2):
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        
        self.pwm1 = PWM(self.in1)
        self.pwm2 = PWM(self.in2)
       
        self.pwm1.freq(500)
        self.pwm2.freq(500)
        
        #stop the motor hard
        self.pwm1.duty(1023)
        self.pwm2.duty(1023)
        


    

    def motgo(self, speed):
        pwm_value = int(min(max(abs(speed), 0), 100) * 10.23)  # Map -100 to 100 to 0 to 1023
        #print('speed pwm value = ', pwm_value)
        if speed > 0:
            # Forward direction
            self.pwm1.duty(pwm_value)
            self.pwm2.duty(0)
        elif speed < 0:
            # Reverse direction
            self.pwm1.duty(0)
            self.pwm2.duty(pwm_value)
        else:
            # Stop the motor
            self.pwm1.duty(0)
            self.pwm2.duty(0)    

    
    def stophard(self):
            self.pwm1.duty(1023)
            self.pwm2.duty(1023)
            

    
