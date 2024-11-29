import socket

s = socket.socket()
host = socket.gethostname()
print("Server will start on host: ",host)

port = 8080
s.bind((host,port))

print("\nServer done binding to host and port sucessfully!\n")

print("\nServer is waiting for numbers\n")

s.listen(1)

conn,addr = s.accept()
print(addr," has connected to the server and is now online...\n")

while 1:
    incoming_message=conn.recv(1024)
    incoming_message=incoming_message.decode()
    print("Client :",incoming_message)
    print("")
    message=input("")
    message=message.encode()
    conn.send(message)
    print("")           
   
 

