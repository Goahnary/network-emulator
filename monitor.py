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