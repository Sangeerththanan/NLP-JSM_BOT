import socket

s = socket.socket()
host = input(str("please enter the host name of the Server:"))

port = 8080
s.connect((host, port))
print("connected to the JSM server")

