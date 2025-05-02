from omnidriver import omnidriver
from time import sleep
from stepper import Stepper 
from gpiozero import Button,PWMOutputDevice
from signal import pause



class scorer:
    def __init__(self, DOA, D1A, D2A, D3A, DOB, D1B, D2B, D3B,
             in1_pin, in2_pin, in3_pin, in4_pin,
             drib1_pin, drib2_pin,
             RL1_pin, RL2_pin, RL3_pin,
             modebutton_pin):
    
        self.motors = [
            omnidriver(in1=DOA, in2=D1A),
            omnidriver(in1=D2A, in2=D3A),
            omnidriver(in1=DOB, in2=D1B),
            omnidriver(in1=D2B, in2=D3B),
        ]

        self.modeflag = False
       

        # Save pin numbers
        self.RL1 = Button(RL1_pin, pull_up=True, bounce_time=0.05)  # 50 ms debounce
        self.RL2 = Button(RL2_pin, pull_up=True, bounce_time=0.05)
        self.RL3 = Button(RL3_pin, pull_up=True, bounce_time=0.05)
        self.modbutton = Button(modebutton_pin, pull_up=True, bounce_time=0.05)
        self.modbutton_pin = modebutton_pin
        self.RL1_pin = RL1_pin
        self.RL2_pin = RL2_pin
        self.RL3_pin = RL3_pin
        
        self.drib1 = PWMOutputDevice(drib1_pin)
        self.drib2 = PWMOutputDevice(drib2_pin)
        self.drib1.value = 0  # start PWM with 0% duty cycle
        self.drib2.value = 0
        
        self.kickermotor = Stepper(in1_pin, in2_pin, in3_pin, in4_pin, step_mode="full", speed=1000)


        # Setup interrupts
        self.RL1.when_pressed = self.escapeLeft
        self.RL2.when_pressed = self.escapeFront
        self.RL3.when_pressed = self.escapeRight
        self.modbutton.when_pressed = self.changemode
    

    def govector(self, vx, vy, ω):  #ω
        v1 = vx - vy - ω     # Front-right  (M1)
        v2 = vx + vy - ω     # Back-right   (M2)
        v3 = vx - vy + ω     # Back-left    (M3)
        v4 = vx + vy + ω     # Front-left   (M4)
        
        self.motors[0].motgo(v1)
        self.motors[1].motgo(v2)
        self.motors[2].motgo(v3)
        self.motors[3].motgo(v4)
        #print('speed value = ', v1, v2, v3, v4)
    
    def gomotor(self, mot, speed):
        if 0 <= mot < 4:
            self.motors[mot].motgo(speed)
        else:
            print("Invalid motor index:", mot)
                        
    def stophard(self):
        for i in range(4):
            self.motors[i].stophard()
    def kick(self):
        self.kickermotor.step_motor(1, 512)

                        
    def dribble(self, speed):
        pwm_value = min(max(abs(speed) / 100.0, 0.0), 1.0)#convert to%
        if speed > 0:
            self.drib1.value = pwm_value
            self.drib2.value = 0
        elif speed < 0:
            self.drib1.value = 0
            self.drib2.value = pwm_value
        else:
            self.drib1.value = 0
            self.drib2.value = 0
    
    def escapeFront(self):
        print('back sensor triggered - escaping front')
        self.govector(0, 60, 0)
        sleep(1)
        self.govector(0, 0, 0)

    
    def escapeRight(self):
        print('left sensor triggered - escaping right')
        self.govector(60, 0, 0)
        sleep(1)
        self.govector(0, 0, 0)

    def escapeLeft(self):
        print('right sensor triggered - escaping left')
        self.govector(-60, 0, 0)
        sleep(1)
        self.govector(0, 0, 0)

    
    def changemode(self):
        self.modeflag = 1 - self.modeflag
        if self.modeflag == 1:
            print("HUNT MODE activated")
        else:
            print("IDLE MODE activated")

