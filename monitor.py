from router import Router 

print "() = weight"

r1 = Router(1)
r2 = Router(2)
r3 = Router(3)
r4 = Router(4)
r5 = Router(5)
r6 = Router(6)
r7 = Router(7)
r8 = Router(8)
r9 = Router(9)
r10 = Router(10)

routers = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]

for x in routers:
	x.add_weight()


for x in routers:
	print "(" + str(x.weight) + ")Hello router " + str(x.routerNum) + ": " + str(x.IP) + " " + str(x.PORT)

# FIXME: FIND RANDOM CONNECTION
print "connecting r1 to r2: "
r1.connectNeighbour(r2)
print "connecting r2 to r3: "
r2.connectNeighbour(r3)
print "connecting r3 to r4: "
r3.connectNeighbour(r4)
print "connecting r3 to r5: "
r3.connectNeighbour(r5)
print "connecting r4 to r6: "
r4.connectNeighbour(r6)
print "connecting r5 to r6: "
r5.connectNeighbour(r6)
print "connecting r6 to r7: "
r6.connectNeighbour(r7)
print "connecting r7 to r8: "
r7.connectNeighbour(r8)
print "connecting r7 to r9: "
r7.connectNeighbour(r9)
print "connecting r8 to r10: "
r8.connectNeighbour(r10)
print "connecting r9 to r10: "
r9.connectNeighbour(r10)
