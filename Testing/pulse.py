from random import randint

def makePulse():

	x =randint(1,3)
	plgood = randint(50,150)
	plbad = randint(120,500)

	if x is 1:
		#send good data
		return "PULSE: " + str(plgood)
	elif x is 2:
		#send bad data (off range)
		return "PULSE: " + str(plbad)
	else :
		#rubish
		return "PULSE: garbage"
