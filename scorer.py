from omnidriver import omnidriver
from time import sleep
from gpiozero import Button,PWMOutputDevice, Device
from signal import pause
from RPLCD.i2c import CharLCD
from threading import Thread, Timer
from vcnl4040 import VCNL4040
from gpiozero.pins.lgpio import LGPIOFactory
from dcmotdriver import dcmotdriver

class scorer:
    def __init__(self,
                 motorA_pins,   # (DOA, D1A, D2A, D3A)
                 motorB_pins,   # (DOB, D1B, D2B, D3B)
                 kickerdribbler_pins,  # (D0C, D1C, D2C, D3C)
                 sensor_pins, # (RL1_pin, RL2_pin, RL3_pin)
                 modebutton_pin):

        self.motorA_pins = motorA_pins
        self.motorB_pins = motorB_pins
        self.kickerdribbler_pins = kickerdribbler_pins
        self.sensor_pins = sensor_pins
        self.modebutton_pin = modebutton_pin
        
        D0C, D1C, D2C, D3C = kickerdribbler_pins
        DOA, D1A, D2A, D3A = motorA_pins
        DOB, D1B, D2B, D3B = motorB_pins
        
        RL1_pin, RL2_pin, RL3_pin = sensor_pins
    
        self.motors = [
            omnidriver(in1=DOA, in2=D1A),
            omnidriver(in1=D2A, in2=D3A),
            omnidriver(in1=DOB, in2=D1B),
            omnidriver(in1=D2B, in2=D3B),
        ]

        self.modeflag = 0
       

        # Save pin numbers
        self.RL1 = Button(RL1_pin, pull_up=True, bounce_time=0.05)  # 50 ms debounce
        self.RL2 = Button(RL2_pin, pull_up=True, bounce_time=0.05)
        self.RL3 = Button(RL3_pin, pull_up=True, bounce_time=0.05)
        self.modbutton = Button(modebutton_pin, pull_up=True, bounce_time=0.05)
        self.modbutton_pin = modebutton_pin
        self.RL1_pin = RL1_pin
        self.RL2_pin = RL2_pin
        self.RL3_pin = RL3_pin
        
        self.dribbler = dcmotdriver(D0C, D1C)
        self.kickermotor = dcmotdriver(D2C, D3C)
        
        
        self.ballsensor = VCNL4040()
        

        # Setup interrupts
        self.RL1.when_pressed = self.escapeLeft
        self.RL2.when_pressed = self.escapeFront
        self.RL3.when_pressed = self.escapeRight
        self.modbutton.when_pressed = self.changemode
    
        self.lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, charmap='A00')

        self.lcd.write_string('Scorer Restarted Successfully!')
        
    def govector(self, vx, vy, ω):  #Holonomic drive
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
    
    def start_dribbler(self, speed, duration=None):
        def _run():
            print(f"[Thread] Starting dribbler at speed {speed}")
            self.dribbler.motgo(speed)
            if duration:
                print(f"[Thread] Will stop in {duration} seconds")
                sleep(duration)
                self.dribbler.stophard()
                print("[Thread] Dribbler stopped after duration")
        Thread(target=_run, daemon=False).start()

    def _run_dribbler(self, speed, duration):
        self.dribbler.motgo(speed)
        print(f"Dribbler running at speed {speed}")

        if duration:
            Timer(duration, self.dribbler.stophard).start()

    
    def start_kicker(self, speed, duration=None):
        def _run():
            print(f"[Thread] Starting kicker at speed {speed}")
            self.kickermotor.motgo(speed)
            if duration:
                print(f"[Thread] Will stop in {duration} seconds")
                sleep(duration)
                self.kickermotor.stophard()
                print("[Thread] kickermotor stopped after duration")
        Thread(target=_run, daemon=False).start()

    def _run_kicker(self, speed, duration):
        self.kickermotor.motgo(speed)
        print(f"Kicker running at speed {speed}")
        if duration:
            Timer(duration, self.kickermotor.stophard).start()
    
    def kick(self):
        self.kickermotor.motgo(80)
        self.dribbler.motgo(60)
    
    
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
                        
    
    
    def escapeLeft(self):
        if self.modeflag != 1:
            return  # Ignore in IDLE and manual mode
        print('right sensor triggered - escaping left')
        Thread(target=self._do_escape, args=(-60, 0)).start()

    def escapeRight(self):
        if self.modeflag != 1:
            return  # Ignore in IDLE and manual mode
        print('left sensor triggered - escaping right')
        Thread(target=self._do_escape, args=(60, 0)).start()

    def escapeFront(self):
        if self.modeflag != 1:
            return  # Ignore in IDLE and manual mode
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
        self.modeflag = (self.modeflag + 1) % 3  # Cycles through 0,1,2

        self.lcd.clear()
        self.lcd.cursor_pos = (0, 1)

        if self.modeflag == 0:
            print("IDLE MODE activated")
            self.lcd.write_string('IDLE mode')
            self.lcd.backlight_enabled = False

            

        elif self.modeflag == 1:
            print("HUNT MODE activated")
            self.lcd.write_string('HUNT mode')
            self.lcd.backlight_enabled = True

           

        elif self.modeflag == 2:
            print("MANUAL MODE activated")
            self.lcd.write_string('MANUAL mode')
            self.lcd.backlight_enabled = True
            self.update_from_manual_commands()

    def update_from_manual_commands(self):
        # Placeholder: read from serial, socket, etc.
        # For now, just print that we're in manual mode
        print("Awaiting manual commands...")
           


    
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
