def canParse(string):
	try:
		float(string)
		return True
	except Exception, e:
		return False

def main():
	while(True):
		string = pulse()
		if canParse(string):
			parsed = float(string)
			if parsed >= 50 and parsed <= 150:
				print "good data"
			else:
				print "bad float"
		else: 
			print "bad data"
