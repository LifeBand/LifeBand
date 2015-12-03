import os
import sys
sys.path.append(os.getcwd()+'/server')
sys.path.append(os.getcwd()+'/lib')
import serverCtrl
import serverModl

def main():
	databse_path = 'lifeBandDB.db'
	listen_ip ='0.0.0.0'#'172.17.144.192'
	listen_port = 5005
	send_port = 6006
	model = serverModl.ServerModel(databse_path)
	model.create_sensor_database()
	controller = serverCtrl.ServerController(databse_path,listen_ip,listen_port,send_port,model) #receivelisten_port,sendlisten_port)
	controller.run_server()




if __name__ == "__main__":
	main()
