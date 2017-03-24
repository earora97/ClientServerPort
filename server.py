import socket
import time
import os
import hashlib
port = 61000
host = ""

s = socket.socket()
s.bind((host, port))
s.listen(5)

print 'Server listening....'
lop = 1
while True:
    conn, addr = s.accept()
    print 'Got connection from', addr
    command = conn.recv(1024)
    a = command.split(" ")

    if a[0] == str('index') and a[1] == str('longlist'):
        t = os.popen('ls -l').read()
        t = t.split('\n')
        print t
        t.pop(0)
        d = '@'
        t = d.join(t)
        a = os.listdir('./')
        result = []
        for files in a :
            data = os.stat(files)
            te = int(data.st_mtime)
            print te
        conn.send(t)

    elif a[0] == str('index') and a[1] == str('shortlist'):
        t = os.popen('ls').read()
        t = t.split('\n')
        ls = os.listdir('./')
        i = 1
        result = []
        for files in ls :
            data = os.stat(files)
            te = int(data.st_mtime)
            print te
            print a[2], a[3]
            if te > int(a[2]) and te < int(a[3]):
                print t[i]
                result.append(t[i])
            i += 1
        d = '@'
        result = d.join(result)
        conn.send(result)

    elif a[0] == str('hash') and a[1] == str('verify') :
        result = []
        with open(a[2],'rb') as f :
            h = hashlib.md5()
            while True:
                data = f.read(1024)
                if not data:
                    break
                h.update(data)
            result.append(str(h.hexdigest()))
        data = os.stat(a[2])
        result.append(str(int(data.st_mtime)))
        d = '@'
        result = d.join(result)
        print result
        conn.send(result)

    elif a[0] == str('hash') and a[1] == str('checkall') :
        ls = os.listdir('./')
        d = '@'
        result = []
        for files in ls :
            result.append(str(files))
            with open(files,'rb') as f :
                h = hashlib.md5()
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    h.update(data)
                result.append(str(h.hexdigest()))
            data = os.stat(files)
            result.append(str(int(data.st_mtime)))
        result = d.join(result)
        conn.send(result)

    elif a[0] == str('download') :
        print a[1]
        filename = a[1]
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
           conn.send(l)
           l = f.read(1024)
        f.close()
        print 'mello'

    conn.close()
s.close()
