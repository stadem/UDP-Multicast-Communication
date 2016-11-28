#!/usr/bin/env python

import socket, sys, os, time,pickle
import struct
#define host ip & port


BUFFER_SIZE = 1024

host = '225.0.0.250'
port = 7280


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:


	#bind and set server to listen
	server_socket.bind((host,port))
	mreq = struct.pack("=4sl", socket.inet_aton(host), socket.INADDR_ANY)
	server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	

except socket.error, (value,message):
	
	if server_socket:
				server_socket.close()
				print "Could not open socket: " + message
				sys.exit(1)


def server(socket,client,dgram):
		#if @ then is user requset
		if '@' in dgram:
			print "User request service list"
			print list_of_servers
	
			#Send to the user the available service
			server_socket.sendto(str(list_of_servers[0]), client )

		#else the request is for initialize the service.
		else: #server
			print "server initialize new Service"
			#list_of_servers = list_of_servers + (dgram,)
			#list_of_servers =
			print dgram
			
			return  str(dgram)


#server while working
if __name__ == '__main__':
	
	list_of_servers = []
	client_addr = ""

	while True:

		pid = os.fork()
				
		if pid: #father

			os.waitpid(pid,0);
		else:

			print 'Listening at',server_socket.getsockname()
			print "\n"
			print "Receiving from", client_addr
			#receive datagram
			dgram,client_addr =  server_socket.recvfrom(BUFFER_SIZE)
			#Add into the list the new service
			print 'dgram#'+dgram+' client_addr#', client_addr,'\n'
			list_of_servers.append(server(server_socket,client_addr,dgram))
