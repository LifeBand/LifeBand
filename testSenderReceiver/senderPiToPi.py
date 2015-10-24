import socket

UDP_IP = "134.117.59.71"
UDP_PORT = 5005
hi = "HEY"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(hi.encode('utf-8'), (UDP_IP, UDP_PORT))