import os
import sys
sys.path.append(os.getcwd()+'/server')
sys.path.append(os.getcwd()+'/lib')
import serverCtrl

def main():
	DatabasePath = 'lifeBandDB.db'
	ListenIP ='0.0.0.0' #'172.17.148.20'
	receivePort =5005
	sendPort = 6006
	controller = serverCtrl.serverController(DatabasePath,ListenIP,receivePort,sendPort)
	controller.runServer()




if __name__ == "__main__":
	main()
