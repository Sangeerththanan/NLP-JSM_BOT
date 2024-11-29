import socket

s = socket.socket()
host = input(str("please enter the host name of the Server:"))

port = 8080
s.connect((host, port))
print("connected to the JSM server")

while 1:
    message=input(str(">>"))
    message=message.encode()
    s.send(message)
    
    incomming_message=s.recv(1024)
    incomming_message=incomming_message.decode()
    print("JSM : ",incomming_message)
    print("")