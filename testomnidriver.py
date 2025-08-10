from omnidriver import omnidriver
from time import sleep

# Pin assignments
DOA = 10
D1A = 22
D2A = 17
D3A = 27

DOB = 5
D1B = 6
D2B = 19
D3B = 13

# Create 4 motor drivers
motors = [
    omnidriver(in1=DOA, in2=D1A),
    omnidriver(in1=D2A, in2=D3A),
    omnidriver(in1=DOB, in2=D1B),
    omnidriver(in1=D2B, in2=D3B),
]

# Test: run first motor forward at 60% for 2 seconds
for i, motor in enumerate(motors, start=0):
    print(f"Testing motor {i} forward")
    motor.motgo(60)  # forward
    sleep(2)
    
    print(f"Testing motor {i} backward")
    motor.motgo(-60)  # backward
    sleep(2)
    
    motor.motgo(0)  # stop
    print(f"Motor {i} stopped")
    sleep(1)

