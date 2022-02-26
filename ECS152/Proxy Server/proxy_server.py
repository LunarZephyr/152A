from socket import *
import sys

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# Fill in start.
host = 'localhost' #'192.168.0.103' #'localhost'
port = 8888
buffer_size = 1024
tcpSerSock.bind((host,port))
tcpSerSock.listen()
# Fill in end.

while True:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    # Fill in start.
    encoded_message = tcpCliSock.recv(buffer_size)
    message = encoded_message.decode('utf-8')
    # Fill in end.

    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    try:
        # Check whether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode('utf-8'))
        tcpCliSock.send("Content-Type:text/html\r\n".encode('utf-8'))

        # Fill in start.
        for i in outputdata:
            tcpCliSock.send(i)
        # Fill in end.

        print('Read from cache')

    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver

            # Fill in start.
            c = socket(AF_INET, SOCK_STREAM)
            # Fill in end.

            hostn = filename.replace("www.","",1)
            print(hostn)
            #try:
            # Connect to the socket to port 80
            # Fill in start.
            host_ip = gethostbyname(filename)
            c.connect((host_ip, 80))
            # Fill in end.

            # Create a temporary file on this socket and ask port 80 for the file requested by the client:
            fileobj = c.makefile('wr', None)
            fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")
            fileobj.flush()
            # Read the response into buffer

            # Fill in start.
            c.send('\nHTTP/1.1 200 OK\n'.encode('utf-8'))  
            buffer = fileobj.readline()
            # Fill in end.

            # Create a new file in the cache for the requested file.
            # Also send the response in the buffer to client socket and the corresponding file in the cache
            tmpFile = open("./" + filename,"wb")
            # Fill in start.
            response = tcpSerSock.rec(1024)
            for i in buffer:
                tmpFile.write(i)
                tcpCliSock.send(i)

            # Fill in end.

            #except:
                #print("Illegal request")

        else:
            # HTTP response message for file not found

            # Fill in start.
            print('404 Not Found')
            tcpSerSock.send('\nHTTP/1.1 404 Not Found\n'.encode('utf-8'))
            # Fill in end.

            # Close the client and the server sockets
            tcpCliSock.close()

# Fill in start.
tcpSerSock.close()
# Fill in end.
