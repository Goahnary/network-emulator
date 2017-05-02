from routernew import Router
import _thread
import socket
import queue
import sys
import tkinter as tk
from tkinter import filedialog

class Client(Router):
    def __init__(self, clientCode, host, port):
        super().__init__(clientCode, host, port)

        # listen for new Routers
        try:
            _thread.start_new_thread(self.listen, ())
        except:
            print("Error: unable to start listen thread")

    def createConnection(self, IP, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((IP, port))

            # send routerCode and weight
            weight = 1
            data = (self.routerCode, weight)
            self.dataSend(sock, data)
            # get the neighbor router's code
            code = self.dataReceive(sock)

            # set the neighbor router's weight
            self.neighbors[code] = weight
            # create a queue to send data to this connection
            self.arrSending[code] = queue.Queue()

            # continuously send whatever data is in the buffer
            _thread.start_new_thread(self.cycleSend, (sock, code))
            # continuously receive whatever data is in the buffer
            _thread.start_new_thread(self.cycleRecv, (sock, code))

            self.generateGraph()
            self.generateTree()
            self.generateForwarding()

        except socket.error as msg:
            print('Failed to create socket. Error Code : ' + str(msg.errno) + ' Message ' + msg.strerror)
            sys.exit()

    def userListen(self):
        # get user input (removing, asking stuff, testing, idk)
        while True:
            uInput = input("Enter number to choose option:\n\t[1] : list all routers\n\t[2] : send text to router"
                           "\n\t[3] : show network graph\n\t[4] : show minimum spanning tree"
                           "\n\t[5] : show router's forwarding table\n\t[6] : Add Router\n\t[7] : Remove Router"
                           "\nEnter choice: ")

            # shows all router codes in network
            if (uInput == "1"):
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename()

                #http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
                #http://stackoverflow.com/questions/1035340/reading-binary-file-in-python-and-looping-over-each-byte
                """file = open(“testfile.txt”, ”w”)

    file.write(“Hello World”)
    file.write(“This is our
    new
    text
    file”)
    file.write(“ and this is another
    line.”)
    file.write(“Why? Because
    we
    can.”)

            file.close()"""

            # send some text to a router
            elif (uInput == "2"):
                code = input("Enter router code to send to (i.e. A): ")
                try:
                    qSend = self.arrSending[code]
                    uMsg = input("Message: \n")
                    qSend.put(self.wrapMessage("text", uMsg))
                    print("Message '" + uMsg + "' sent.\n")
                except KeyError:
                    print("That router does not exist.\n")

            # show network graph
            elif (uInput == "3"):
                for key, value in self.neighbors.items():
                    data = self.wrapMessage("rGraph", ())

                    # request updated graph and wait for it
                    with self.condGraph:
                        self.arrSending[key].put(data)
                        self.condGraph.wait()
                    break

                self.drawGraph(self.networkGraph)
            # print(json.dumps(self.networkGraph, sort_keys=True, indent=4), "\n")

            # show spanning tree
            elif (uInput == "4"):
                for key, value in self.neighbors.items():
                    data = self.wrapMessage("rTree", ())

                    # request updated graph and wait for it
                    with self.condTree:
                        self.arrSending[key].put(data)
                        self.condTree.wait()
                    break

                self.drawGraph(self.networkTree)
            # print(json.dumps(self.networkTree, sort_keys=True, indent=4), "\n")

            # show a specific router's forwarding table
            elif (uInput == "5"):
                code = input("Enter router code to get table (i.e. A): ")
                try:
                    data = self.wrapMessage("rTable", ())

                    # update this table with router's forwarding table
                    with self.condTable:
                        self.arrSending[code].put(data)
                        self.condTable.wait()

                    # print forwarding table
                    print(json.dumps(self.forwarding, sort_keys=True, indent=4), "\n")
                except KeyError:
                    print("That router does not exist.\n")

            # add a new router
            elif (uInput == "6"):
                code = input("Enter new router code (i.e. A): ")
                if code not in self.neighbors:
                    port = input("Enter new port for router: ")
                    try:
                        nRouters = literal_eval(input("Enter routers to connect to in the form:\n"
                                                      "[('host', port), ('host', port), ...)]\n "))
                        router = Router(code, "", eval(port))
                        router.initConnections(nRouters)

                        print("Router " + code + " added.\n")
                    except:
                        print("That wasn't formatted correctly.\n")

                else:
                    print("That router already exists.\n")

            # remove a router
            elif (uInput == "7"):
                code = input("Enter router code to remove (i.e. A): ")
                if code in self.neighbors:
                    self.arrSending[code].put(self.wrapMessage("unplug", ()))
                else:
                    print("That router does not exist.\n")