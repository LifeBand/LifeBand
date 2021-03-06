from adxl345 import ADXL345
from math import sqrt
from time import sleep

__author__ = "dominikschmidtlein"
__date__ = "$Nov 26, 2015 1:12:15 PM$"

MAGNITUDE_THRESHOLD = 2.5
PERIOD_BETWEEN_SAMPLES = 0.01

def get_magnitude(x, y, z):
    return sqrt(x**2 + y**2 + z**2)

def get_magnitude_dict(axes):
    return get_magnitude(axes['x'], axes['y'], axes['z'])
    
def read_acceleration_to_dict(adxl345):
    return adxl345.getAxes(True)

def send_magnitude(magnitude):
    print magnitude
    
def check_magnitude(magnitude):
    return magnitude > MAGNITUDE_THRESHOLD

def send_alarm():
    print "                                 ALARM"

if __name__ == "__main__":
    adxl345 = ADXL345()
    while True:
        sleep(PERIOD_BETWEEN_SAMPLES)
        magnitude = get_magnitude_dict(read_acceleration_to_dict(adxl345))
        send_magnitude(magnitude)
        if check_magnitude(magnitude):
            send_alarm()