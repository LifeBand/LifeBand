import socket
DEF_BUFFER_SIZE = 1024

def createUDPSocket(ip,port):
	conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	conn.bind((ip,port))
	return conn

def sendUDP(conn, ip,port, message):
	conn.sendto(message, (ip,port))
	return

def recvUDP(conn):
	data = None
	try:
		receiver, data = conn.recvfrom(DEF_BUFFER_SIZE)
	except:
		pass
	return receiver , data


def closeUDPSocket(conn):
	conn.close()

'''

server = createUDPSocket('127.0.0.1',7050)


try:
	while True:
		#Accept each communication
		conn, addr = recvUDP(server)
		#Create a new thread for each connection that is made
		#thread.start_new_thread( serverController, (conn,addr)) 
except (KeyboardInterrupt, SystemExit):
	closeTCP(conn)
	server.close()
'''