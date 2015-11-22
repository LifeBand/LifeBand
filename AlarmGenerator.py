from random import randint

hr_max_threshold = 100
hr_min_threshold = 50
hr_change_threshold = 10
#the largest change in heart rate before it is dangerous

alarm = false
safe_to_turn_off = true
alarming = false


def next_heart_rate():
    #receives the next heart rate
    heart_rate = randint(40, 110)
    return heart_rate
    
def alarm_button_pressed():
    safe_to_turn_off = true

#the first time through sets alarming true
#if alarming is still true, the alarm will be raised
def alarm_signal():
    if alarming:
        safe_to_turn_off = false
        alarm = true
        print("I am alarmed")
        #will also send a signal to the controller
    else:
        alarming = true
    
def turn_off_alarm():
    if safe_to_turn_off:
        alarm = false
    
if __name__ == '__main__':
    alarming = false
    hr = next_heart_rate()
    if hr < hr_min_threshold || hr > hr_max_threshold:
        alarm_signal()
    last_hr = hr
    while true:
        hr = next_heart_rate()
        if hr < hr_min_threshold || hr > hr_max_threshold || abs(hr - last_hr) > hr_change_threshold:
            alarm_signal()
        else:
            turn_alarm_off()
        last_hr = hr
