from router import Router 

print "Ello Mate"

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



r1.add_neighbor(r2)
r2.add_neighbor(r1)

print(r1.get_neighbors())