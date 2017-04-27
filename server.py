
import socket

TCP_IP = '127.0.0.1'    # address of the server you would like to connect to
TCP_PORT = 5829         # port you will connect on. THIS SHOULD MATCH THE SERVER FILE
BUFFER_SIZE = 128       # small buffer size for text
data = ""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))

while data != "EXIT":				# loops unless it gets the exit command
	s.listen(1)				# listens for response
	conn, addr = s.accept()			# sets these two variables to socket accept object
	print('connection address: ', addr)	# prints who is connecting
	data = conn.recv(BUFFER_SIZE)		# grabs sent information from the s.accept object
	if not data: break			# If there is nothing sent (sendiing null) break the loop
	data = data.upper()			# capitalizes the data sent
	print("received data:", data)
	conn.send(data) 			# send the data back	

conn.close()