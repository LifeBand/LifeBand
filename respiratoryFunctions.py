import math
amplitude = 1
vShift = 2
period = 0.0004*math.pi()
def bradypnea_resp(count):
    thing = 2*amplitude*math.sin(period*count/2)
    if thing < 0:
        return 0
    else:
        return thing + vShift
        
def cheyne_Stokes_resp(count):
    return amplitude*math.sin(period*count)*math.sin(period*count/3) +vShift

def kussmauls_resp(count):
    return 1.25*amplitude*math.sin(period*count*2) + vShift

def apneustic_resp(count):
    return abs(math.sin(period*count)) + vShift
