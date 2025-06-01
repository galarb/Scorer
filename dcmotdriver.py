from gpiozero import PWMOutputDevice, Device
import time 
import math
import random

        
    
class dcmotdriver:
    def __init__(self, in1_pin, in2_pin):
        self.mot1 = PWMOutputDevice(in1_pin)
        self.mot2 = PWMOutputDevice(in2_pin)
        self.mot1.value = 0  # start PWM with 0% duty cycle
        self.mot2.value = 0
        

    def motgo(self, speed):
        pwm_value = min(max(abs(speed) / 100.0, 0.0), 1.0)#convert to%
        #print('speed pwm value = ', pwm_value)
        if speed > 0:
            self.mot1.value = pwm_value
            self.mot2.value = 0
        elif speed < 0:
            self.mot1.value = 0
            self.mot2.value = pwm_value
        else:
            self.mot1.value = 0
            self.mot2.value = 0    

    
    def stophard(self):
            self.mot1.value = 1
            self.mot2.value = 1
            

    

