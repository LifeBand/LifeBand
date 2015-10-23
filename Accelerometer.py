from random import randint


def stubAccelerometer():
	
	thistime = randint(0,50)
	string = "ACCEL: "
	
	if thistime>45:
		return "garbage"
	elif thistime > 40:
		min = 100
		max = 500
	elif thistime <=7:
		min = -500
		max = 0
	else
		min = 0
		max = 50
	
	for i in range(0, 5):
		string += randint(min, max) + " "
	
	
	return string
