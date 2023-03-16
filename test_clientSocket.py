import socket #import socket module

s = socket.socket() #Create a socket object
#host = socket.gethostname() #Get the local machine name
host = '192.168.0.218'
#print(host)
port = 12399 # Reserve a port for your service
s.bind((host,port)) #Bind to the port
s.listen(1) #Wait for the client connection
while True:
    c,addr = s.accept() #Establish a connection with the client
    print('Got connection from')
    print(addr)
    c.send(b"Thank you for connecting")
    c.close()
    
'''
TCP_IP = '192.16.0.215' # this IP of my pc. When I want raspberry pi 2`s as a client, I replace it with its IP '169.254.54.195'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print ("received data raspia:", data)
'''

