from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep

class omnidriver:
    def __init__(self, in1, in2):
        self.in1 = PWMOutputDevice(in1)
        self.in2 = PWMOutputDevice(in2)
        
        self.in1.value = 0  # brake
        self.in2.value = 0


    def motgo(self, speed):
        pwm_value = min(max(abs(speed) / 100.0, 0.0), 1.0)#convert to%
        if speed > 0:
            self.in1.value = pwm_value
            self.in2.value = 0
        elif speed < 0:
            self.in1.value = 0
            self.in2.value = pwm_value
            
        else:
            self.in1.value = 0
            self.in2.value = 0
        #print(f"PWM1: {pwm_value if speed > 0 else 0}\nPWM2: {pwm_value if speed < 0 else 0}")

    def stophard(self):
        self.in1.value = 1
        self.in2.value = 1
            
        sleep(0.01)

