def f():
    for i in range(5):
	yield i
	
for i in f():
	print i
