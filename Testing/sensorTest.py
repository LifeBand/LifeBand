import csv
import os
import time

#File imports
import pulse
import Accelerometer as accel
def main():

	currTime = str(time.strftime("%c").replace(' ','-'))

	currDir = os.path.dirname(__file__)
	directory = os.path.join(currDir,'Log')
	if not os.path.exists(directory):
		os.mkdir(directory)

	pulseFile = open(directory+'/PULSE'+currTime+'.csv','a')
	accelFile = open(directory+'/ACCEL'+currTime+'.csv','a')

	while(True):

		currPulse = 0
		currAccel = {
					'xf':0
					'yf':0
					'zf':0
					'xa':0
					'ya':0
					'za':0
					}

		response = str(pulse.makePulse())
		if ("PULSE:" in response):
			response = response[6:len(response)]
			response = response.replace(' ','')
			print response
			try:
				currPulse = float(response)
				if(currPulse<=150 or currPulse>=50):
					print "We got good data"
					pulseFile.write(currTime+','+str(currPulse)+','+'Good\n') 
				else:
					print "We got bad data"
					pulseFile.write(currTime+','+str(currPulse)+','+'Bad\n')
						
			except ValueError:
			    print "This is Garbage data"
			    currPulse = -1
			    pulseFile.write(currTime+','+str(currPulse)+','+'Garbage data\n') 


		response = str(accel.stubAccelerometer())
		if ("ACCEL:" in response):
			response = response[6:len(response)]
			response = response.replace(' ','')
			print response
			try:
				currPulse = float(response)
				if(currPulse<=150 or currPulse>=50):
					print "We got good data"
					pulseFile.write(currTime+','+str(currPulse)+','+'Good\n') 
				else:
					print "We got bad data"
					pulseFile.write(currTime+','+str(currPulse)+','+'Bad\n')
						
			except ValueError:
			    print "This is Garbage data"
			    currPulse = -1
			    pulseFile.write(currTime+','+str(currPulse)+','+'Garbage data\n') 

		'''if canParse(string):
			parsed = float(string)
			if parsed >= 50 and parsed <= 150:
				print "good data"
			else:
				print "bad float"
		else: 
			print "bad data"
		'''
		time.sleep(1)
if __name__ == "__main__":
    main()