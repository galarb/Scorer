from scorer import scorer
from time import sleep
from signal import pause

#DOA, D1A, D2A, D3A, DOB, D1B, D2B, D3B, in1_pin, in2_pin, in3_pin, in4_pin, drib1_pin, drib2_pin, RL1_pin, RL2_pin, RL3_pin, button _pin

pilot = scorer(10, 22, 17, 27, 5, 6, 19, 13, 21, 20, 16, 12, 8, 7, 24, 23, 18, 4)
pause()  # Keeps the script running to wait for button presses


try:
    while True:
        if pilot.modeflag == 0:
            # IDLE MODE
            pilot.govector(0, 0, 0)  # No movement
            pilot.dribble(0)         # Maybe small dribble? Or completely off.
        else:
            # HUNT MODE
            pilot.govector(0, 0, 20)  # Example: Go forward hunting
            pilot.dribble(0)

        sleep(0.1)  # Small sleep to avoid high CPU usage

except KeyboardInterrupt:
    print('Stopped by user')
    pilot.stophard()
