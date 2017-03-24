import socket
import time

host = ""
port = 61000

while True:
    command = raw_input("Enter command:")
    s = socket.socket()
    s.connect((host, port))
    s.send(command)
    a = command.split(" ")
    if a[0] != 'download':
        nameFile = s.recv(1024)
        t = nameFile.split('@')
        for files in t :
            print files
        #print nameFile
    else :
        nameFile = a[1]
        print a[1]
        with open(nameFile, 'a+') as f:
            print 'file opened'
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
            print "end"
        print('Successfully get the file')
    s.close()
print('connection closed')
