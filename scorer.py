from omnidriver import omnidriver
from time import sleep
from stepper import Stepper 
from gpiozero import Button,PWMOutputDevice, Device
from signal import pause
from RPLCD.i2c import CharLCD
from threading import Thread
from vcnl4040 import VCNL4040

from gpiozero.pins.lgpio import LGPIOFactory




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
        self.ballsensor = VCNL4040()
        

        # Setup interrupts
        self.RL1.when_pressed = self.escapeLeft
        self.RL2.when_pressed = self.escapeFront
        self.RL3.when_pressed = self.escapeRight
        self.modbutton.when_pressed = self.changemode
    
        self.lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, charmap='A00')

        self.lcd.write_string('Scorer Restarted Successfully!')
        
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
    def release(self):
        self.kickermotor.release()
    
    def ball_loaded(self):
        prox = self.ballsensor.read_proximity()
        lux = self.ballsensor.read_lux_raw()
        #print(f"Proximity: {prox}, Lux Raw: {lux}")
        #sleep(0.5)
        if (prox > 20):
            print("ball loaded")
            return True
        else:
            return False
                        
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
    
    def escapeLeft(self):
        print('right sensor triggered - escaping left')
        Thread(target=self._do_escape, args=(-60, 0)).start()

    def escapeRight(self):
        print('left sensor triggered - escaping right')
        Thread(target=self._do_escape, args=(60, 0)).start()

    def escapeFront(self):
        print('back sensor triggered - escaping front')
        Thread(target=self._do_escape, args=(0, 60)).start()

    def _do_escape(self, vx, vy):
        for _ in range(1000):
            self.govector(vx, vy, 0)
            sleep(0.001)  # 1 millisecond delay for smoother motion
        self.govector(0, 0, 0)
        
    def get_modeflag(self):
        #print(f"Current modeflag: {self.modeflag}")  # Debugging print
        return self.modeflag
    
    def changemode(self):
        self.modeflag = 1 - self.modeflag
        #print(f"Mode changed to: {self.modeflag}")  # Debugging print
        if self.modeflag == 1:
            print("HUNT MODE activated")
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 1)
            self.lcd.write_string('HUNT mode')
            self.lcd.backlight_enabled = True

        else:
            print("IDLE MODE activated")
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 1)
            self.lcd.write_string('IDLE mode')
            self.lcd.backlight_enabled = False

    
    def joyride(self):
        print("Starting JOYRIDE demo...")
        self.lcd.clear()  # Clear the screen before writing
        self.lcd.write_string("Joyride!")

        # Move forward
        print("Forward")
        self.lcd.clear()  # Clear the screen before writing
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Moving Forward")
        self.govector(0, -30, 0)
        sleep(1)
        
        # Move backward
        print("Backward")
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Moving Backward")
        self.govector(0, 30, 0)
        sleep(1)
        
        # Strafe right
        print("Right")
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Strafing Right")
        self.govector(30, 0, 0)
        sleep(1)
        
        # Strafe left
        print("Left")
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Strafing Left")
        self.govector(-30, 0, 0)
        sleep(1)
        
        # Rotate clockwise
        print("Rotate CW")
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Rotating CW")
        self.govector(0, 0, 30)
        sleep(1)
        
        # Rotate counter-clockwise
        print("Rotate CCW")
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Rotating CCW")
        self.govector(0, 0, -30)
        sleep(1)
        
        # Diagonal top-right
        print("Diagonal top-right")
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Diagonal Top-Right")
        self.govector(30, -30, 0)
        sleep(1)
        
        # Diagonal bottom-left
        print("Diagonal bottom-left")
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Diagonal Bottom-Left")
        self.govector(-30, 30, 0)
        sleep(1)
        
        # Full stop
        print("Stopping")
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Stopping")
        self.govector(0, 0, 0)
