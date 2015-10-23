from random import randint


def stubAccelerometer():
	thistime = randint(0,50)
	if thistime>45:
		return "garbage"
	elif thistime > 40:
		xf = randint(100,500)
		yf = randint(100,500)
		zf = randint(100,500)
		xa = randint(100,900)
		ya = randint(100,900)
		za = randint(100,900)
	elif thistime <=7:
		xf = randint(0,-500)
		yf = randint(0,-500)
		zf = randint(0,-500)
		xa = randint(0,-900)
		ya = randint(0,-900)
		za = randint(0,-900)
	else
		xf = randint(0,50)
		yf = randint(0,50)
		xa = randint(0,90)
		ya = randint(0,50)
		zf = randint(0,90)
		za = randint(0,90)
	string = "" + xa + ya + za + xf + yf + zf
	return string