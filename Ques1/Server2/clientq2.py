import socket
import time
import os
import hashlib
import datetime
import re
PORT_SERVER = 62005
PORT_CLIENT = 62004
HOST_SERVER = ""
HOST_CLIENT = ""

BLOCKED=False
def server():
	skt = socket.socket()
	skt.bind((HOST_SERVER, PORT_SERVER))
	skt.listen(5)
	while True:
		global BLOCKED
		while BLOCKED:
			p=1	
		BLOCKED=True
		connect_other_client, address_other_client = skt.accept()
		print 'Got connection from\n', address_other_client
		command = connect_other_client.recv(1024)
		command = command.split(" ")

		if command[0] == str('index') and command[1] == str('longlist'):
        		file_list = os.popen('ls ./SharedFiles -l').read()
			file_list = file_list.split('\n')
        		#print file_list
        		file_list.pop(0)
        		delimitor = '@'
        		file_list = delimitor.join(file_list)
        		command = os.listdir('./SharedFiles')
        		output = []
        		for files in command :
				files = './SharedFiles/' + files
        	    		data = os.stat(files)
        	    		te = int(data.st_mtime)
				te = datetime.datetime.fromtimestamp(te)
        	    		#print te
        		connect_other_client.send(file_list)
		elif command[0] == str('index') and command[1] == str('shortlist'):
        		file_list = os.popen('ls ./SharedFiles').read()
        		file_list = file_list.split('\n')
        		ls = os.listdir('./SharedFiles')
        		output = []
        		for files in ls :
				files = './SharedFiles/' + files
        	    		data = os.stat(files)
        	    		te = int(data.st_mtime)
				#te = datetime.datetime.fromtimestamp(te)
        	    		#print te
        	    		#print command[2], command[3]
        	    		if te > int(command[2]) and te < int(command[3]):
        	        	#	print file_list[i]
        	        		output.append(file_list[i])
        		delimitor = '@'
        		output = delimitor.join(output)
        		connect_other_client.send(output)
		
		elif command[0] == str('index') and command[1] == str('regex'):
        		file_list = os.popen('ls ./SharedFiles').read()
        		file_list = file_list.split('\n')
        		ls = os.listdir('./SharedFiles')
        		output = []
        		for files in ls :
				files = './SharedFiles/' + files
        	    		data = os.stat(files)
        	    		te = int(data.st_mtime)
				te = datetime.datetime.fromtimestamp(te)
        	    		#print te
        	   		#print command[2]
        	    		if re.match(command[2],files):
        	        		#print file_list[i]
        	        		output.append(file_list[i])
        		delimitor = '@'
        		output = delimitor.join(output)
        		connect_other_client.send(output)
		
		elif command[0] == str('hash') and command[1] == str('verify') :
        		output = []
        		with open('./SharedFiles/'+command[2],'rb') as f :
        	    		h = hashlib.md5()
        	    		while True:
        	        		data = f.read(1024)
        	        		if not data:
						break
        	        		h.update(data)
        	    		output.append(str(h.hexdigest()))
        		data = os.stat('./SharedFiles/'+command[2])
        		output.append(str(int(data.st_mtime)))
        		delimitor = '@'
        		output = delimitor.join(output)
        		#print output
        		connect_other_client.send(output)
		
		elif command[0] == str('hash') and command[1] == str('checkall') :
        		ls = os.listdir('./SharedFiles')
        		delimitor = '@'
        		output = []
        		for files in ls :
        			output.append(str(files))
        			with open('./SharedFiles/'+files,'rb') as f :
       	        			h = hashlib.md5()
       	        			while True:
       	        	    			data = f.read(1024)
       	        	    			if data=="":
       	        	        			break
       	        	    			h.update(data)
       	        			output.append(str(h.hexdigest()))
			data = os.stat('./SharedFiles/'+files)
			output.append(str(int(data.st_mtime)))
       			output = delimitor.join(output)
       			connect_other_client.send(output)
	
		elif command[0] == str('download') :
       			print command[1]
       			filename = command[1]
       			f = open('./SharedFiles/'+filename,'rb')
       			l = f.read(1024)
       			while (l):
       	   			connect_other_client.send(l)
       	   			l = f.read(1024)
       			f.close()
       			print 'All Data Sent'
		BLOCKED=False	

def client_download(file_name,file_size):
	with open('./SharedFiles/'+file_name, 'a+') as f:
		print 'Download Started' , file_name
		command = "download "+file_name
		skt = socket.socket()
		skt.connect((HOST_CLIENT, PORT_CLIENT))
    		skt.send(command)
		recieved_size=0
		while recieved_size<file_size:
			print "*"
			data = skt.recv(1024)
			recieved_size+=1024
			print "."
			if not data:
				break
			f.write(data)
		print "Download Comleted"


def client():
	start_time=time.time()
	files_hashes=dict()
	while True:
		global BLOCKED
		if time.time()-start_time>3 and BLOCKED==False:
			BLOCKED=True
			print time.time()
			start_time = time.time()
	
			#get list of files in Shared Directory		
			skt = socket.socket()
			skt.connect((HOST_CLIENT, PORT_CLIENT))
			command = "index longlist"
	    		skt.send(command)
		    	file_list = skt.recv(1024)
	        	file_list = file_list.split('@')
			print file_list
			for files in file_list :
				files = files.split()
				file_name=files[8]
				file_size=files[3]
				print "file name-->",file_name
	         		if file_name not in files_hashes.keys():
					#new file
					print file_name
					skt = socket.socket()
					skt.connect((HOST_CLIENT, PORT_CLIENT))
					command = "hash verify "+file_name
					skt.send(command)
					hash_time = skt.recv(1024)
					hash_time = hash_time.split('@')
					hash_v = hash_time[0]
					files_hashes[file_name] = hash_v
					print file_name,hash_time
					client_download(file_name,file_size)
				else:
					#old file
					print("old")
					command = "hash verify "+file_name
					skt.send(command)
					hash_time = skt.recv(1024)
					hash_time = hash_time.split('@')
					hash_v = hash_time[0][0]
					#file modified
					if hash_v != file_hashes[file_name]:
						files_hashes[file_name] = hash_v
					print file_name
					client_download(file_name,file_size)
			BLOCKED=False
	

def main():
 
	print 'Server Shyam activated'
	#Server thread
	pid_Server = os.fork()
	global BLOCKED
	BLOCKED=False
	if pid_Server==0:
		#in server
		server()
	
	#error in creating server therad
	elif pid_Server<0:
		print("Error Creating Server Thread")
	
	#in main code
	else:
		pid_Client=os.fork()
		if pid_Client==0:
			#in client
			client()
		
		#error creating client thread
		elif pid_Client<0:
			print("Error creating Client Thread")

		#main code
		else:
			#wait for server thread to terminate
			print("hello")
			while True:
				wpid,status=os.waitpid(pid_Server, os.WUNTRACED)
				if (os.WIFEXITED(status) or os.WIFSIGNALED(status)):
					break
			while True:
				wpid,status=os.waitpid(pid_Client, os.WUNTRACED)
				if (os.WIFEXITED(status) or os.WIFSIGNALED(status)):
					break
	return 0

main()
