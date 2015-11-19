import os
import sys
sys.path.append(os.getcwd()+'/server')
sys.path.append(os.getcwd()+'/lib')
import serverCtrl
import serverModl

def main():
	DatabasePath = 'lifeBandDB.db'
	ListenIP ='172.17.158.44'# #'172.17.148.20'
	Port = 5005
	#receivePort =5005
	#sendPort = 6006
	model = serverModl.serverModel(DatabasePath)
	model.createSensorDatabase()
	controller = serverCtrl.serverController(DatabasePath,ListenIP,Port,model) #receivePort,sendPort)
	controller.runServer()




if __name__ == "__main__":
	main()
