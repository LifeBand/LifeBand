from random import randint


def stubAccelerometer():
	
	thistime = randint(0,50)
	string = "ACCEL: "
	data = {"xf: ", "yf: ", "zf: ", "xa: ", "ya: ", "za: "}
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
	
	for i in data:
		if "f" in i:
			string += i + randint(min, max) + " "
		elif "a" in i:
			string += i + randint(min, max*2 -10) + " "
	return string
