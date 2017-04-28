import _thread
import socket
import queue
 
class Router:
    host = "127.0.0.1"
    port = 5000
     
    try:
    	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
		print('Failed to create socket. Error Code: ' + str(msg.errno) + ' Message ' + msg.strerror)
		sys.exit()


    def __init__(self, routerCode, host, port):
		self.routerCode = routerCode
		self.sock.bind((host,port))
		self.neighbors = []


	#nArray = [ (IP, port), (IP, port), ... ]
	def initConnections(self, nArray):
		#Connect to adjacent Routers
		for router in nArray:
			_thread.start_new_thread(sendNewConnection, (router))

		#Listen for new Routers
		try:
			_thread.start_new_thread(listen, ())
		except:
  			print("Error: unable to start listen thread")

  		#Generate map and tree
		netMap = generateMap()
		netTree = generateTree(netMap)
		

	#tupRouter = (IP, port)
	def sendNewConnection(tupRouter):
		try:
	    	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    	sock.connect(tupRouter[0], tupRouter[1])

	    	while True:
	    		sock.
	    except socket.error as msg:
			print('Failed to create socket. Error Code : ' + str(msg.errno) + ' Message ' + msg.strerror)
			sys.exit()
		
			

	def listen(self):
	    self.sock.listen(1)
	    
	    while True:
	    	_thread.start_new_thread(procListen, self.sock.accept())

	def procListen(self, conn, addr):
		while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print("from connected  user: " + str(data))
             
            data = str(data).upper()
            print("sending: " + str(data))
            conn.send(data.encode())
	             
	    conn.close()
	    		
