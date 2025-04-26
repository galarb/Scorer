from omnidriver import omnidriver
from time import sleep
from stepper import Stepper 
import RPi.GPIO as GPIO
from gpiozero import Button
from signal import pause



class scorer:
    def __init__(self, DOA, D1A, D2A, D3A, DOB, D1B, D2B, D3B,
             in1_pin, in2_pin, in3_pin, in4_pin,
             drib1_pin, drib2_pin,
             RL1_pin, RL2_pin, RL3_pin):
    
        self.motors = [
            omnidriver(in1=DOA, in2=D1A),
            omnidriver(in1=D2A, in2=D3A),
            omnidriver(in1=DOB, in2=D1B),
            omnidriver(in1=D2B, in2=D3B),
        ]

        GPIO.setmode(GPIO.BCM)

        # Set up output pins
        GPIO.setup(drib1_pin, GPIO.OUT)
        GPIO.setup(drib2_pin, GPIO.OUT)

        # Save pin numbers
        self.RL1 = Button(RL1_pin, pull_up=True, bounce_time=0.05)  # 50 ms debounce
        self.RL2 = Button(RL2_pin, pull_up=True, bounce_time=0.05)
        self.RL3 = Button(RL3_pin, pull_up=True, bounce_time=0.05)
        self.RL1_pin = RL1_pin
        self.RL2_pin = RL2_pin
        self.RL3_pin = RL3_pin
        
        self.drib1 = GPIO.PWM(drib1_pin, 500)
        self.drib2 = GPIO.PWM(drib2_pin, 500)

        self.kickermotor = Stepper(in1_pin, in2_pin, in3_pin, in4_pin, step_mode="full", speed=1000)


        # Setup interrupts
        self.RL1.when_pressed = self.escapeLeft
        self.RL2.when_pressed = self.escapeFront
        self.RL3.when_pressed = self.escapeRight


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
        pwm_value = min(max(abs(speed), 0), 100)
        if speed > 0:
            self.drib1.ChangeDutyCycle(pwm_value)
            self.drib2.ChangeDutyCycle(0)
        elif speed < 0:
            self.drib1.ChangeDutyCycle(0)
            self.drib2.ChangeDutyCycle(pwm_value)
        else:
            self.drib1.ChangeDutyCycle(100)
            self.drib2.ChangeDutyCycle(100)
    
    def checkboundary(self):
        RL1 = GPIO.input(self.RL1_pin)
        RL2 = GPIO.input(self.RL2_pin)
        RL3 = GPIO.input(self.RL3_pin)

        if RL1:  # RIGHT sensor triggered: go LEFT (270° → -x)
            print('hit boundary - RiGHT sensor')
            self.govector(-45, 0, 0)
            sleep(2)
            return True
        elif RL2:  # BACK sensor triggered: go FORWARD (0° → +y)
            print('hit boundary - BACK sensor')
            self.govector(0, 45, 0)
            sleep(2)
            return True
        elif RL3:  # LEFT sensor triggered: go RIGHT (90° → +x)
            print('hit boundary - LEFT sensor')
            self.govector(45, 0, 0)
            sleep(2)
            return True
        else:
            return False
    
    
    
    def escapeFront(self):
        print('back sensor triggered - escaping front')
        self.govector(0, 20, 0)
        sleep(1)
        self.govector(0, 0, 0)

    
    def escapeRight(self):
        print('left sensor triggered - escaping right')
        self.govector(20, 0, 0)
        sleep(1)
        self.govector(0, 0, 0)
        
    def escapeLeft(self):
        print('right sensor triggered - escaping left')
        self.govector(-20, 0, 0)
        sleep(1)
        self.govector(0, 0, 0)
    
            

