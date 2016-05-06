import socket

TCP_IP = '127.0.0.1' 	# address of the server you would like to connect to
TCP_PORT = 7779		# port you will connect on. THIS SHOULD MATCH THE SERVER FILE
BUFFER_SIZE = 128	# small buffer size for text
MESSAGE = ""

print "Welcome to my python network client!"

# loop to keep asking for input unless you get the exit command
MESSAGE = raw_input("Enter some text: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates socket
s.connect((TCP_IP, TCP_PORT))	# connects to the server
s.send(MESSAGE)			# sends message
data = s.recv(BUFFER_SIZE)	# Recieves return messages
print "Exiting client program!"
s.close()
