# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import json
import socket

__author__ = "dominikschmidtlein"
__date__ = "$Nov 4, 2015 4:08:12 PM$"

if __name__ == "__main__":
    MY_IP = "134.117.59.73"
    OTHER_IP = "134.117.59.74"
    UDP_PORT = 5005
    

    #UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.bind((MY_IP, UDP_PORT))

    while True:
        input1 = input("Send or receive: ")
        if input1 == "s":
            input2 = input("What to send: ")
            #create object
            data = {}
            #add key value pair to object
            data['value'] = input2
            #serialize object to json formatted string
            json_data = json.dumps(data)
            print("{}".format(json_data))
            #encode json encoded string using 'utf-8'
            sock.sendto(json_data.encode('utf-8'), (OTHER_IP, UDP_PORT))   
        elif input1 == "r":
            data, addr = sock.recvfrom(1024)
            #decode from 'utf-8' to json encoded string
            data = data.decode('utf-8')
            #decode string to json object
            jsonObject = json.loads(data)
            print("{}".format(jsonObject))
