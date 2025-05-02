from gpiozero import Device, DigitalOutputDevice
from gpiozero.pins.rpigpio import RPiGPIOFactory
Device.pin_factory = RPiGPIOFactory()

from time import sleep

class Stepper:
    full_step_sequence = [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
    ]

    half_step_sequence = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
    ]

    def __init__(self, in1_pin, in2_pin, in3_pin, in4_pin, step_mode="full", speed=1000):
        self.pins = [
            DigitalOutputDevice(in1_pin),
            DigitalOutputDevice(in2_pin),
            DigitalOutputDevice(in3_pin),
            DigitalOutputDevice(in4_pin)
        ]

        self.speed = speed  # microseconds between steps
        self.set_step_mode(step_mode)

    def set_step_mode(self, mode):
        if mode == "half":
            self.step_sequence = self.half_step_sequence
        else:
            self.step_sequence = self.full_step_sequence

    def step_motor(self, direction, steps):
        step_count = len(self.step_sequence)
        seq_range = range(step_count) if direction > 0 else reversed(range(step_count))

        for _ in range(steps):
            for i in seq_range:
                for pin, value in zip(self.pins, self.step_sequence[i]):
                    pin.value = value
                sleep(self.speed / 1_000_000.0)

    def rotate_degrees(self, degrees, direction=1):
        steps_per_rev = 2048 if len(self.step_sequence) == 4 else 4096
        steps_needed = int((degrees / 360) * steps_per_rev)
        self.step_motor(direction, steps_needed)

    def release(self):
        for pin in self.pins:
            pin.off()

