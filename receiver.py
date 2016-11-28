#!/usr/bin/env python

import socket, sys, os, time
import struct
#define host ip & port

port = 7182
BUFFER_SIZE = 1024

#Add user into list
def insert_user(t,address,username):

			print "inserting"
			#print address , username
			usr_record = address + (username,)		
			
			t = t + ( usr_record,)
			
			
			return (t)

#Search user by username from list an retrun ip/port
def search_user(usr_record,user):

			for i in range(len(usr_record)):
					
				if (usr_record[i][2] == user):					

					ip = usr_record[i][0]
					client_port = usr_record[i][1]
			
			return (ip,client_port)

#Search user by ip/port and retrun username
def search_userFromIpPort(t,ip,port):
		
			for i in range(len(t)):
					
				if (t[i][0] == ip and t[i][1] == port):
					uname = t[i][2]
				
			
			return (uname)

#Check if user is already registerd
def search_if_Registerd(t,un,ip,port):

			for i in range(len(t)):
				if ( (t[i][0] == ip and t[i][1] == port) or t[i][2] == un ):	
					exist = 1
				else:
					exist = 0

				return exist

#Chech if the same user name exist on list
def usernameExist(t,user):

			for i in range(len(t)):
				if (t[i][2] == user):	
					exist = 1
				else:
					exist = 0

				return exist


#Split the message if the length of ':' is 3 
#then this is a message from userform:userto:message else the message
#is in short format line userto:message and the ip/post is 
def packet_split(dgram):

				s = dgram.split(":")
				
				if len(s) == 3:			
					sender = s[0]
					receiver = s[1]
					message = s[2]	
				else:
					sender = ""
					receiver = s[0]
					message = s[1]				
				return  (sender,receiver,message)

def printusers(t) :
		prdata = ""
		for i in range(len(t)):
			prdata = prdata + 'IP: ' + t[i][0] + ' User: ' + t[i][2] +'\n'
		return prdata

	
def poll(table):
		server_socket.sendto(printusers(table), ('224.0.0.127',port))
		time.sleep(10)

def AnnounceToNetwork():
		#Init the service in order to be announce to the user 
		server_socket.sendto("chat:224.0.0.127:7182", ('225.0.0.250',7280))


#server while working
if __name__ == '__main__':

	t = ()
	message =""
	ip = ""
	client_addr = ""
	client_port = 0
	username = ""

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:

 		#bind and set server to listen
		server_socket.bind(('224.0.0.127',port))
		mreq = struct.pack("=4sl", socket.inet_aton("224.0.0.127"), socket.INADDR_ANY)
		server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
		server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

	except socket.error, (value,message):
		
		if server_socket:
					server_socket.close()
					print "Could not open socket: " + message
					sys.exit(1)

	AnnounceToNetwork()

	while True:

		pid = os.fork()
		
		if pid: 

			#Server status
			os.waitpid(pid,0);
			#server_socket.sendto( dgram, ('224.0.0.127',port))
			#poll(t)
			sys.exit(1)
			#dgram,client_addr =  server_socket.recvfrom(BUFFER_SIZE)
			#server_socket.sendto(message, (ip, port))	
			##print "User:", user, " says:", message , "\n"
			
		else:

			print 'Listening at',server_socket.getsockname()
			print "Receiving from", client_addr
			#receive datagram
			dgram,client_addr =  server_socket.recvfrom(BUFFER_SIZE)
			print 'dgram#'+dgram+' client_addr#', client_addr,'\n'
			
			#Parameters for Reply Back
			list_client_addr = list(client_addr)
			cl_ip = list_client_addr[0]
			cl_port =list_client_addr[1]


			##Check if user or message is set
			if ':' in dgram:
				if '*' in dgram:
					print 'Sending message to all connected users'
					#parse packet
					sender,receiver,message = packet_split(dgram)
					uname = search_userFromIpPort(t,cl_ip,cl_port)
					
					for i in range(len(t)):		
						#Send message to all exept myself			
						if (t[i][0] != cl_ip or t[i][1] != cl_port):
							loop_ip = t[i][0]
							loop_port = t[i][1]								
							server_socket.sendto( "[TO ALL]"+uname + " says: "+message, (loop_ip,loop_port))
					# server_socket.sendto( dgram, ('224.0.0.127',port))

				else:
					print 'Sending message to single user'
					#parse packet
					sender,receiver,message = packet_split(dgram)
					#print sender,receiver,message
					
					receiver_ip,receiver_port = search_user(t,receiver)
					#print receiver_ip,receiver_port

					#Getting user name from ip
					uname = search_userFromIpPort(t,cl_ip,cl_port)


					# Allow to send the message without the username of the sender i.e To_user:Message
					if sender == '':
						sender = uname
					server_socket.sendto("@"+sender+" says: "+message, (receiver_ip,receiver_port))

			else:
				##Check if command is set
				if '/list' in dgram:					#list users/		
					print 'Try to set command'
					printusr = printusers(t)				
					server_socket.sendto("[Command is set "+dgram+"]\n\n Available users \n" + printusr, (cl_ip,cl_port))

				elif '/all' in dgram:					#All users/					
					server_socket.sendto("[Command is set "+dgram+"]\n\n Available users Total \n" + str(t), (cl_ip,cl_port))

				else:					
					#Check if already registerd. if not add to list	
					isRegisterd = search_if_Registerd(t, dgram, cl_ip, cl_port)
					if isRegisterd:
						print 'Is already registered'
						server_socket.sendto("Already registered [Pls type { from:to_user:Message OR from:*:Message }\n in order to procced]", (cl_ip,cl_port))
					else:
						print 'try to register user'
						#Register user and retrun welcome message
						server_socket.sendto("[Welcome "+dgram+"]", (cl_ip,cl_port))
						t = insert_user(t,client_addr,dgram)
						print t




