import json
import socket

MY_IP = "134.117.59.70"
OTHER_IP = "134.117.59.69"
UDP_PORT = 5005 

#create object
data = {}
#add key value pair to object
data['domkey'] = 'domvalue'
#serialize object to json formatted string
json_data = json.dumps(data)

#UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((MY_IP, UDP_PORT))

while True:
 input1 = input("Send or receive: ")
 if input1 == "s":
  print("{}".format(json_data))
  sock.sendto(json_data.encode('utf-8'), (OTHER_IP, UDP_PORT))   
 elif input1 == "r":
  data, addr = sock.recvfrom(1024)
  data = data.decode('utf-8')
  jsonObject = json.loads(data)
  print("{}".format(jsonObject))
  