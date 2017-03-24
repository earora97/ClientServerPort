import socket
import time
import os
import hashlib
import datetime
PORT_SERVER = 62005
PORT_CLIENT = 62004
HOST = ""
count = 0

def main():
 
	quit=False
	print 'Server Server1 activated'
	#lop = 1
	pid_Client=os.fork()
		
	#client code
	if pid_Client==0:
		for i in range(1,3,0):
			count += 1
			print count
			command = raw_input("Enter command:")
    			skt = socket.socket()
			skt.settimeout(5)
    			skt.connect((HOST, PORT_CLIENT))
    			skt.send(command)
    			command = command.split(" ")
				
			if command[0] == 'download':
        			file_name = command[1]
				path = './SharedFiles/'+file_name
        			with open(path, 'w+') as f:
            				print 'Download Started'
            				for i in range(1,3,0):
						try:
	       	        				data = skt.recv(1024)
							if not data:
        	            					break
        	        				f.write(data)
						except socket.timeout, e:
							if e.args[0]=='timed out':
								break
            				print "Download Completed"
        			print('File Downloaded Successfully')
    			else :
        			file_list = skt.recv(1024)
        			file_list = file_list.split('@')
        			for files in file_list :
            				print files


	#client code ended
		
	#error creating client thread
	elif pid_Client<0:
		print("Error creating Client Thread")

			
	
	#in main code
	else:
		#Server thread
		pid_Server = os.fork()
		if pid_Server==0:
		#in server
			skt = socket.socket()
			skt.bind((HOST, PORT_SERVER))
			skt.listen(5)
			for i in range(1,3,0):
			count += 1
			print count
				print 'Got connection from', address_other_client
				connect_client, address_client = skt.accept()
				command = connect_client.recv(1024)
				command = command.split(" ")

				if command[0]=='quit':
					quit=True

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
        			    		print te
        				connect_client.send(file_list)
		
				elif command[0] == str('index') and command[1] == str('shortlist'):
        				file_list = os.popen('ls ./SharedFiles').read()
        				file_list = file_list.split('\n')
        				ls = os.listdir('./SharedFiles')
        				i = 1
        				output = []
        				for files in ls :
						files = './SharedFiles/' + files
        			    		data = os.stat(files)
        			    		te = int(data.st_mtime)
						te = datetime.datetime.fromtimestamp(te)
        			    		print te
        			    		print command[2], command[3]
        			    		if te > int(command[2]) and te < int(command[3]):
        			        		print file_list[i]
        			        		output.append(file_list[i])
        			    		i += 1
        				delimitor = '@'
        				output = delimitor.join(output)
        				connect_client.send(output)
			
				elif command[0] == str('hash') and command[1] == str('verify') :
        				output = []
					path = './SharedFiles/'+command[2]	
        				with open(path,'rb') as f :
        			    		h = hashlib.md5()
        			    		while True:
        			        		data = f.read(1024)
        			        		if not data:
								break
        			        		h.update(data)
        			    		output.append(str(h.hexdigest()))
        				data = os.stat(command[2])
        				output.append(str(int(data.st_mtime)))
        				delimitor = '@'
        				output = delimitor.join(output)
        				print output
        				connect_client.send(output)
			
				elif command[0] == str('hash') and command[1] == str('checkall') :
        				ls = os.listdir('./SharedFiles')
        				delimitor = '@'
        				output = []
        				for files in ls :
        		    			output.append(str(files))
						path = './SharedFiles/'+files

        		    			with open(path,'rb') as f :
        		        			h = hashlib.md5()
        		        			while True:
        		        	    			data = f.read(1024)
        		        	    			if not data:
        		        	        			break
        		        	    			h.update(data)
        		        			output.append(str(h.hexdigest()))
					data = os.stat('./SharedFiles/'+files)
					output.append(str(int(data.st_mtime)))
        				output = delimitor.join(output)
        				connect_client.send(output)
		
				elif command[0] == str('download') :
        				print command[1]
        				filename = command[1]
					path = './SharedFiles/'+filename

        				f = open(path,'rb')
        				l = f.read(1024)
        				while (l):
        		   			connect_client.send(l)
        		   			l = f.read(1024)
        				f.close()
        				print 'All Data Sent'
				
					if quit==True:
						connect_client.close()
						skt.close()
						exit()

	
		#server code ends
		
		#error in creating server therad
		elif pid_Server<0:
			print("Error Creating Server Thread")
		#main code
		else:
			#wait for server thread to terminate
			print("hello")
			#try:
			for i in range(1,3,0):
			count += 1
			print count
				wpid,status=os.waitpid(pid_Server, os.WUNTRACED)
				if (os.WIFEXITED(status) or os.WIFSIGNALED(status)):
					break
			while True:
				wpid,status=os.waitpid(pid_Client, os.WUNTRACED)
				if (os.WIFEXITED(status) or os.WIFSIGNALED(status)):
					break
			#except:
				#connect_other_client.close()
				#skt.close()
			#connect_other_client.close()
			#skt.close()
	return 0

main()
