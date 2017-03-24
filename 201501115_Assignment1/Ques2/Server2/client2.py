import socket
import time
import os
import hashlib
import datetime
import re
PORT_SERVER = 62005
PORT_CLIENT = 62004
HOST = ""

BLOCKED=False

def print_counter(counter):
	counter += 1
	#print "Here:",counter
	#print "value:", pid_Server

def main():
 
	quit=False
	count =0
	print_counter(count)
	print 'Server2 activated'
	#lop = 1
	global BLOCKED
	BLOCKED=False

	#Server thread
	pid_Server = os.fork()
	if pid_Server==0:
	#in server
		skt = socket.socket()
		skt.bind((HOST, PORT_SERVER))
		skt.listen(5)
		while True:
			count += 1
			print_counter(count)
			while BLOCKED:
				p=1	
			BLOCKED=True
			connect_other_client, address_other_client = skt.accept()
			print 'Got connection from', address_other_client
			command = connect_other_client.recv(1024)
			command = command.split(" ")


			if command[0] == str('index') and command[1] == str('longlist'):
        			file_list = os.popen('ls ./SharedFiles -l').read()
				file_list = file_list.split('\n')
        			ls = os.listdir('./SharedFiles')
				for files in ls:
					files = './SharedFiles/' + files
        		    		data = os.stat(files)
        		    		te = int(data.st_mtime)
					#te = datetime.datetime.fromtimestamp(te)
        		    		print te
        		    	#	print command[2], command[3]
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
        			i = 1
        			output = []
        			for files_info in file_list[1:-1]:
					files_info = files_info.split()
					files = './SharedFiles/' + files_info[8]
        		    		data = os.stat(files)
        		    		te = int(data.st_mtime)
					#te = datetime.datetime.fromtimestamp(te)
        		    		print te
        		    	#	print command[2], command[3]
        		    		if te > int(command[2]) and te < int(command[3]):
        		        		print file_info
        		        		output.append(' '.join(files_info))
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
				#te = int(data.st_mtime)
				#te = datetime.datetime.fromtimestamp(te)
        		    	#print te
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
			elif command[0] == str('index') and command[1] == str('regex'):
        			file_list = os.popen('ls ./SharedFiles -l').read()
        			file_list = file_list.split('\n')
				print file_list
        			ls = os.listdir('./SharedFiles')
        			output = []
        			for files_info in file_list[1:-1] :
					print files_info
					files_info = files_info.split()
					files = './SharedFiles/' + files_info[8]
        	    			data = os.stat(files)
        	    			te = int(data.st_mtime)
					te = datetime.datetime.fromtimestamp(te)
        	    			#print te
        	   			#print command[2]
        	    			if re.search(command[2],files):
        	        			#print file_list[i]
        	        			output.append(' '.join(files_info))
        			delimitor = '@'
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
			
			BLOCKED=False	

	
	#server code ends
	
	#error in creating server therad
	elif pid_Server<0:
		print("Error Creating Server Thread")
	
	#in main code
	else:
		pid_Client=os.fork()
		
		#client code
		if pid_Client==0:
			start_time=time.time()
			files_hashes=dict()
			while True:
				count2 = 0
				count2+=1
				print_counter(count2)
				if time.time()-start_time>3 and BLOCKED==False:
					BLOCKED=True
					print time.time()
					start_time = time.time()
			
					#get list of files in Shared Directory		
					skt = socket.socket()
					skt.connect((HOST, PORT_CLIENT))
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
							skt.connect((HOST, PORT_CLIENT))
							command = "hash verify "+file_name
							skt.send(command)
							hash_time = skt.recv(1024)
							hash_time = hash_time.split('@')
							hash_v = hash_time[0]
							files_hashes[file_name] = hash_v
							print file_name,hash_time
							#client_download(file_name,file_size)
							with open('./SharedFiles/'+file_name, 'a+') as f:
								print 'Download Started' , file_name
								command = "download "+file_name
								skt = socket.socket()
								skt.connect((HOST, PORT_CLIENT))
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
								print "Download Completed"
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
							#client_download(file_name,file_size)
							with open('./SharedFiles/'+file_name, 'a+') as f:
								print 'Download Started' , file_name
								command = "download "+file_name
								skt = socket.socket()
								skt.connect((HOST, PORT_CLIENT))
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
								print "Download Completed"
				BLOCKED=False
		#client code ended
		
		#error creating client thread
		elif pid_Client<0:
			print("Error creating Client Thread")

		#main code
		else:
			#wait for server thread to terminate
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
