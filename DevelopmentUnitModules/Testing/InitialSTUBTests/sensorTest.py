#!/usr/bin/python

import csv
import os
import time

#File imports
import pulse
import Accelerometer as accel
def main():

	currTime = str(time.strftime("%c").replace(' ','-'))
	accelFields = ["xf:", "yf:", "zf:", "xa:", "ya:", "za:"]

	currDir = os.path.dirname(__file__)
	directory = os.path.join(currDir,'Log')
	if not os.path.exists(directory):
		os.mkdir(directory)

	pulseFile = open(directory+'/'+currTime+'PULSE.csv','a')
	accelFile = open(directory+'/'+currTime+'ACCEL.csv','a')

	while(True):

		currPulse = 0

		currAccel = {
					'xf':0,
					'yf':0,
					'zf':0,
					'xa':0,
					'ya':0,
					'za':0
					}

		response = str(pulse.makePulse())
		if "PULSE:" in response:
			response = response[6:len(response)]
			response = response.replace(' ','')
			#print response
			try:
				currPulse = float(response)
				if(currPulse<=150 and currPulse>=50):
					pulseFile.write(currTime+','+str(currPulse)+','+'Good\n') 

					print 'PULSE:\t'+currTime+'\t'+str(currPulse)+'\n'

				else:
					pulseFile.write(currTime+','+str(currPulse)+','+'Bad\n')
						
			except ValueError:
			    currPulse = -1
			    pulseFile.write(currTime+','+str(currPulse)+','+'Garbage data\n') 
		else:
			pulseFile.write(currTime+','+str(-1)+','+'Garbage data\n') 


		response = str(accel.stubAccelerometer())
		
		indexWhiteSpace=0

		indexXf=0
		indexYf=0
		indexZF=0
		
		indexXa=0
		indexYa=0
		indexZa=0

		if ("ACCEL:" in response):
			response = response[6:len(response)]
			response = response.replace(' ','')
			#print response+'\n\n'
			try:
				
				indexXf = response.index(accelFields[0])
				indexWhiteSpace = response.index(accelFields[1],indexXf)
				currAccel['xf'] = float(response[indexXf+3:indexWhiteSpace])
				
				indexYf = response.index(accelFields[1])
				indexWhiteSpace = response.index(accelFields[2],indexYf)
				currAccel['yf'] = float(response[indexYf+3:indexWhiteSpace])
				
				indexZf = response.index(accelFields[2])
				indexWhiteSpace = response.index(accelFields[3],indexYf)
				currAccel['zf'] = float(response[indexZf+3:indexWhiteSpace])
				
				indexXa = response.index(accelFields[3])
				indexWhiteSpace = response.index(accelFields[4],indexXa)
				currAccel['xa'] = float(response[indexXa+3:indexWhiteSpace])
				

				indexYa = response.index(accelFields[4])
				indexWhiteSpace = response.index(accelFields[5],indexYa)
				currAccel['ya'] = float(response[indexYa+3:indexWhiteSpace])
				
				indexZa = response.index(accelFields[5])
				
				currAccel['za'] = float(response[indexZa+3:len(response)])

				if(currAccel['xf']<=50) and currAccel['yf']<=50 and currAccel['zf']<=50:
					accelFile.write(currTime+','+str(currAccel['xf'])+','+
							str(currAccel['yf'])+','+str(currAccel['zf'])+','+
							str(currAccel['xa'])+','+str(currAccel['ya'])+','+
							str(currAccel['za'])+', Good Data\n')

					print 'ACCEL: '+currTime
					for key, value in currAccel.items():
						print '\t'+str(key) +": "+ str(value)
					print '\n'
				else:
					accelFile.write(currTime+','+str(currAccel['xf'])+','+
							str(currAccel['yf'])+','+str(currAccel['zf'])+','+
							str(currAccel['xa'])+','+str(currAccel['ya'])+','+
							str(currAccel['za'])+', Bad Data\n')
						
			except ValueError:
			    accelFile.write(currTime+','+str(-1)+','+str(-1)+','+
			    		str(-1)+','+str(-1)+','+str(-1)+','+str(-1)+','+
			    		'Garbage data\n') 
		else:
			accelFile.write(currTime+','+str(-1)+','+str(-1)+','+
			    		str(-1)+','+str(-1)+','+str(-1)+','+str(-1)+','+
			    		'Garbage data\n')
		time.sleep(1)
if __name__ == "__main__":
    main()