#Author: Derek White
#Date: 11/23/2015
#AlarmGenerator.py


from random import randint

HR_MAX_THRESHOLD = 100
HR_MIN_THRESHOLD = 50
HR_CHANGE_THRESHOLD = 10
#the largest change in heart rate before it is dangerous

alarm = False
safeToTurnOff = True
alarming = False


def next_heart_rate():
    #receives the next heart rate
    heartRate = randint(40, 110)
    return heartRate
    
def alarm_button_pressed():
    safeToTurnOff = true

#the first time through sets alarming true
#if alarming is still true, the alarm will be raised
def alarm_signal():
    if alarming:
        safeToTurnOff = false
        alarm = true
        print("I am alarmed")
        #will also send a signal to the controller
    else:
        alarming = true
    
def turn_off_alarm():
    if safeToTurnOff:
        alarm = false
    
if __name__ == '__main__':
    alarming = false
    hr = next_heart_rate()
    if hr < HR_MIN_THRESHOLD || hr > HR_MAX_THRESHOLD:
        alarm_signal()
    lastHr = hr
    while true:
        hr = next_heart_rate()
        if hr < HR_MIN_THRESHOLD || hr > HR_MAX_THRESHOLD || abs(hr - lastHr) > HR_CHANGE_THRESHOLD:
            alarm_signal()
        else:
            turn_alarm_off()
        lastHr = hr
