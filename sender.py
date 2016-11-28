#!/usr/bin/env python
import socket,os,time, sys

port = 7182
BUFFER_SIZE = 1024


def menu():	
	print "1-> Start chat!  "
	print "2-> Select Service  "
	print "0-> exit "
	print "[commands: show users -> /list or /all ] "
	return None

if __name__ == '__main__':
	
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
	#client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #this is a broadcast socket

	menu()

	choice = raw_input('\n->')

	if (choice==str(0)):

		#username = raw_input('\nusername:')
		sys.exit(1)


	elif (choice==str(1)): 
		#If the choice == 1 connect to chat instant
		username = raw_input('\nType a username->')
		client_socket.sendto(username, ("224.0.0.127", port))

		while True:				
			pid = os.fork()			
			if pid:				
				rcv_message, sender_addr = client_socket.recvfrom(BUFFER_SIZE)
				print rcv_message + "\n"
			else:
				message = raw_input('-->')
				client_socket.sendto(message, ("224.0.0.127", port))

	elif (choice==str(2)): 

			#Handle the requst. When @ is assign,
			# identifies that the request is comming from the user (on service.py file)
			client_socket.sendto("@", ('225.0.0.250', 7280))
			rcv_message, sender_addr = client_socket.recvfrom(BUFFER_SIZE)

			#echo the service
			print '1 ' + rcv_message
			select_server = raw_input('select service-->')
			#print "response from service > "+rcv_message,sender_addr

			##In order to use multiple services
			# for i in range(len(rcv_message)):
			# 	print rcv_message[i][0]				
			# 	print i+1 , rcv_message[i] 
			# serv_ip =  rcv_message[select_server-1][0]
			# serv_port = rcv_message[select_server-1][1]

			#Parse the service
			s = rcv_message.split(":")
			serviceName = s[0]
			serv_ip = s[1]
			serv_port = s[2]	
			print serviceName, serv_ip, serv_port

			#Init Chat service.
			username = raw_input('\nType a username->')
			client_socket.sendto(username, (str(serv_ip), int(serv_port)))

			while True:

				pid = os.fork()
				
				if pid:					
					rcv_message, sender_addr = client_socket.recvfrom(BUFFER_SIZE)
					print rcv_message + "\n"
				else:
					message = raw_input('-->')
					client_socket.sendto(message, ("224.0.0.127", port))
