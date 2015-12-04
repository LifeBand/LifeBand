from adxl345 import ADXL345
from math import sqrt
from time import sleep

__author__ = "Amr Gawish"
__date__ = "$Dec 3, 2015 1:12:15 PM$"

MAGNITUDE_THRESHOLD = 2.5

def get_magnitude(x, y, z):
    return sqrt(x**2 + y**2 + z**2)

def get_magnitude_dic(axes):
    return get_magnitude(axes['x'], axes['y'], axes['z'])
    
def read_acceleration_to_dict(adxl345):
    return adxl345.getAxes(True)

def send_mag_data(magnitude):
    print magnitude
    
def check_magnitude(magnitude):
    return magnitude > MAGNITUDE_THRESHOLD

def send_mag_alarm():
    print "                                 ALARM"

if __name__ == "__main__":
    adxl345 = ADXL345()
    count = 0 
    start_time = time.time()
    while True:
	sleep(0.1)
        magnitude = get_magnitude_dic(read_acceleration_to_dict(adxl345))
        if (time.time() - start_time) < 1:
            if count is 0:
                max_mag = magnitude
                count = 1;
            else:
                if magnitude > max_mag :
                    max_mag = magnitude
        else:
            start_time = time.time()
            if check_magnitude(max_mag):
                send_mag_alarm()
            else:
                count = 0
                send_mag_data(max_mag)
        
