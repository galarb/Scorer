  from omnidriver import omnidriver
from time import sleep, ticks_ms



class scorer:
    def __init__(self, DOA, D1A, D2A, D3A, DOB, D1B, D2B, D3B):
        self.mot1 = omnidriver(
            in1=DOA,
            in2=D1A
            )
        self.mot2 = omnidriver(
            in1=D2A,
            in2=D3A
            )
        self.mot3 = omnidriver(
            in1=DOB,
            in2=D1B
            )
        self.mot4 = omnidriver(
            in1=D2B,
            in2=D3B
            )
    def govector(self, vx, vy, omega):
        v1 = vx + vy + omega
        v2 = -vx + vy + omega
        v3 = -vx - vy + omega
        v4 = vx - vy + omega
        self.mot1.motgo(v1)
        self.mot2.motgo(v2)
        self.mot3.motgo(v3)
        self.mot4.motgo(v4)
        print('speed value = ', v1, v2, v3, v4)
                        
                        
                        
                        

        
