from routernew import Router
from monitornew import Monitor
from servernew import Server

mon = Monitor("monitor", "", 5000)
r1 = Router("A", "", 5501)
r2 = Router("B", "", 5502)
r3 = Router("C", "", 5503)
r4 = Router("D", "", 5504)
r5 = Router("E", "", 5505)
r6 = Router("F", "", 5506)
r7 = Router("G", "", 5507)
r8 = Router("H", "", 5508)
r1.initConnections([])
r2.initConnections([("localhost", 5501)])
r3.initConnections([("localhost", 5501)])
r4.initConnections([("localhost", 5503)])
r5.initConnections([("localhost", 5503), ("localhost", 5504), ("localhost", 5502)])
r6.initConnections([("localhost", 5504)])
r7.initConnections([("localhost", 5506)])
r8.initConnections([("localhost", 5507), ("localhost", 5502), ("localhost", 5506)])

s = Server("server", "", 5678)
s.createConnection("localhost", 5508)

mon.userListen()