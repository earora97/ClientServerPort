import socket
import time
import os
import hashlib
import datetime
PORT_SERVER = 62004
PORT_CLIENT = 62005
HOST_SERVER = ""
HOST_CLIENT = ""

def main():
 
	quit=False
	print 'Server Ram activated'
	#lop = 1
	
	#Server thread
	pid_Server = os.fork()
	if pid_Server==0:
	#in server
		skt = socket.socket()
		skt.bind((HOST_SERVER, PORT_SERVER))
		skt.listen(5)
		while True:
			connect_other_client, address_other_client = skt.accept()
			print 'Got connection from', address_other_client
			command = connect_other_client.recv(1024)
			command = command.split(" ")

			if command[0]=='quit':
				quit=True

			if command[0] == str('index') and command[1] == str('longlist'):
        			file_list = os.popen('ls ./SharedFiles -l').read()
				file_list = file_list.split('\n')
        			print file_list
        			file_list.pop(0)
        			delimitor = '@'
        			file_list = delimitor.join(file_list)
        			command = os.listdir('./SharedFiles')
        			output = []
        			for files in command :
					files = './SharedFiles/' + files
        		    		data = os.stat(files)
        			connect_other_client.send(file_list)
	
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
        			data = os.stat(command[2])
				te = int(data.st_mtime)
				te = datetime.datetime.fromtimestamp(te)
        		    	print te
        			output.append(str(int(data.st_mtime)))
        			delimitor = '@'

        			output = delimitor.join(output)
        			print output
        			connect_other_client.send(output)
		
			elif command[0] == str('hash') and command[1] == str('checkall') :
        			ls = os.listdir('./SharedFiles')
        			delimitor = '@'
        			output = []
				te = int(data.st_mtime)
				te = datetime.datetime.fromtimestamp(te)
        		    	print te
        			for files in ls :
        	    			output.append(str(files))
        	    			with open('./SharedFiles/'+files,'rb') as f :
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
        			connect_other_client.send(output)
		
			elif command[0] == str('download') :
        			print command[1]
				te = int(data.st_mtime)
				te = datetime.datetime.fromtimestamp(te)
        		    	print te
        			filename = command[1]
        			f = open('./SharedFiles/'+filename,'rb')
        			l = f.read(1024)
        			while (l):
        	   			connect_other_client.send(l)
        	   			l = f.read(1024)
        			f.close()
        			print 'All Data Sent'
			
			if quit==True:
				connect_other_client.close()
				skt.close()
				exit()

	
	#server code ends
	
	#error in creating server therad
	elif pid_Server<0:
		print("Error Creating Server Thread")
	
	#in main code
	else:
		pid_Client=os.fork()
		
		#client code
		if pid_Client==0:
			while True:
				command = raw_input("Enter command:")
    				skt = socket.socket()
				skt.settimeout(10)
    				skt.connect((HOST_CLIENT, PORT_CLIENT))
    				skt.send(command)
    				command = command.split(" ")
				if command[0] == 'quit':
					quit=True
				
    				if command[0] != 'download':
        				file_list = skt.recv(1024)
        				file_list = file_list.split('@')
        				for files in file_list :
        	    				print files
				else :
        				file_name = command[1]
        				print file_name[1]
        				with open('./SharedFiles/'+file_name, 'a+') as f:
        	    				print 'Download Started'
        	    				while True:
							try:
	        	        				data = skt.recv(1024)
								print data	
        		        				if not data:
        		            					break
        		        				f.write(data)
							except socket.timeout, e:
								if e.args[0]=='timed out':
									break
						print "Download Completed"
        				print('File Downloaded Successfully')
				if quit==True:
					skt.close()
					exit()


	
		#client code ended
		
		#error creating client thread
		elif pid_Client<0:
			print("Error creating Client Thread")

		#main code
		else:
			#wait for server thread to terminate
			print("hello")
			#try:
			while True:
				wpid,status=os.waitpid(pid_Server, os.WUNTRACED)
				if (os.WIFEXITED(status) or os.WIFSIGNALED(status)):
					break
			#except:
				#connect_other_client.close()
				#skt.close()
			#try:
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
