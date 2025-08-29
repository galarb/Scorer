from gpiozero import Button
from time import sleep

# Replace with your actual GPIO pin
BUTTON_PIN = 4 

button = Button(BUTTON_PIN, pull_up=True)

print("Press the button (Ctrl+C to stop)...")

try:
    while True:
        if button.is_pressed:
            print("Button pressed")
        else:
            print("Button released")
        sleep(0.2)

except KeyboardInterrupt:
    print("Stopped.")

