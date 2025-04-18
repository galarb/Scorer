from omnidriver import omnidriver
from time import sleep



class scorer:
    def __init__(self, DOA, D1A, D2A, D3A, DOB, D1B, D2B, D3B):
        self.motors = [
            omnidriver(in1=DOA, in2=D1A),
            omnidriver(in1=D2A, in2=D3A),
            omnidriver(in1=DOB, in2=D1B),
            omnidriver(in1=D2B, in2=D3B),
        ]
        
    def govector(self, vx, vy, ω):  #ω
        v1 = vx - vy - ω     # Front-right  (M1)
        v2 = vx + vy - ω     # Back-right   (M2)
        v3 = vx - vy + ω     # Back-left    (M3)
        v4 = vx + vy + ω     # Front-left   (M4)
        
        self.motors[0].motgo(v1)
        self.motors[1].motgo(v2)
        self.motors[2].motgo(v3)
        self.motors[3].motgo(v4)
        print('speed value = ', v1, v2, v3, v4)
    
    def gomotor(self, mot, speed):
        if 0 <= mot < 4:
            self.motors[mot].motgo(speed)
        else:
            print("Invalid motor index:", mot)
                        
    def stophard(self):
        for i in range(4):
            self.motors[i].stophard()
        
                        

        
