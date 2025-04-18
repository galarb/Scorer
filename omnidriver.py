import RPi.GPIO as GPIO
from time import sleep

class omnidriver:
    def __init__(self, in1, in2):
        self.in1 = in1
        self.in2 = in2

        GPIO.setmode(GPIO.BCM)
        #GPIO.cleanup()

        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        
        self.pwm1 = GPIO.PWM(self.in1, 500)  # 500 Hz
        self.pwm2 = GPIO.PWM(self.in2, 500)
        
        self.pwm1.start(100)  # brake
        self.pwm2.start(100)


    def motgo(self, speed):
        pwm_value = min(max(abs(speed), 0), 100)
        if speed > 0:
            self.pwm1.ChangeDutyCycle(pwm_value)
            self.pwm2.ChangeDutyCycle(0)
        elif speed < 0:
            self.pwm1.ChangeDutyCycle(0)
            self.pwm2.ChangeDutyCycle(pwm_value)
        else:
            self.pwm1.ChangeDutyCycle(0)
            self.pwm2.ChangeDutyCycle(0)
        print(f"PWM1: {pwm_value if speed > 0 else 0}\nPWM2: {pwm_value if speed < 0 else 0}")

    def stophard(self):
        self.pwm1.ChangeDutyCycle(100)
        self.pwm2.ChangeDutyCycle(100)
        sleep(0.01)



