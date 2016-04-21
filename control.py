import router

r1 = router(1)
r2 = router(2)

r1.add_neighbor(r2)
r2.add_neighbor(r1)

print(r1.get_neighbors())