import random
n = random.randint(0,30)
lst = ['FCFS','FJS','SRTF','RR']
kind =random.randint(0,3) 
print(lst[kind])
print(n)
for i in range(n):
	x1 = random.randint(10,20)
	x2 = round(random.uniform(0, 20), 1)
	x3 = round(random.uniform(0, x1), 1)
	x4 = round(random.uniform(0, 20), 1)
	print(x1,x2,x3,x4)
if kind == 3:
	print(round(random.uniform(10, 35), 1))	
print(round(random.uniform(10, 35), 1))