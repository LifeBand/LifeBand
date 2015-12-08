
Visit our website at http://lifeband.github.io/ for a general overview of our project.

LifeBand is a health-monitoring system for bed-ridden patients.

It uses a system made up of two Raspberry Pi's: One for the server, one for the Wearable
___
The Wearable RPi contains:

* A Pulse sensor: https://www.sparkfun.com/products/11574
* An IMU: https://www.sparkfun.com/products/10121

An Android device is also needed to view the stats.
___
	
**To run the Server**:

1. Clone this repository
2. Go into FinalModules/ServerStandAlone/
3. run command: python runServer.py

**To run the Phone**:

1. Clone this repository
2. Go into FinalModules/LifeBand/
3. Open this directory using Android Studio
4. Run the project


**To run the Wearable**:

1. Clone this repository
2. Go into FinalModules/wearable_pi
3. run command: python wearable_pi.py
	




