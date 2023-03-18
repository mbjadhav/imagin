import socket #import socket module
import time
s = socket.socket() #Create a socket object

#host = socket.gethostname() #Get the local machine name
host = '192.168.0.218' #IP of host i.e. raspberry pi
#print(host)
port = 12399 # Reserve a port for your service
s.bind((host,port)) #Bind to the port
s.listen(1) #Wait for the client connection
c,addr = s.accept() #Establish a connection with the client

while True:
    print('Got connection from')
    print(addr)
    #i=0
    #for i in 100:
    #    string = 'coundown ' + i
    #   c.send(b(string))
    c.send(b"countdown out")
    time.sleep(1)
c.close()
