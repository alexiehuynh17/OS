import time,queue,operator,copy

class Process:
	def __init__(self,burst,come,iostart,iorun,hasio,name):
		self.burst = burst
		self.come = come
		self.iostart = iostart
		self.iorun = iorun
		self.timeRe = burst
		self.io = []
		self.ioqueue = []
		self.bu = []
		self.status = ""
		self.thiss = -1
		self.hasIo = hasio
		self.name = name
#Set status at t-time
def MarkStatus(p, t, n):
	for i in range(n):
		check = 0
		if t > p[i].bu[len(p[i].bu) - 1] and t > p[i].io[len(p[i].io) - 1]:
			p[i].status = "Done"
			continue
		for j in range (0,len(p[i].bu) - 1,2):
			if p[i].bu[j] <= t and t < p[i].bu[j+1]:
			   check = 1	
			   p[i].status = "CPU(running)"
		if check == 1: 
			continue
		for j in range (0,len(p[i].io) - 1,2):
			if p[i].io[j] <= t and t < p[i].io[j+1]:
			   check = 1	
			   p[i].status = "IO(waiting)"
		if check == 1: 
			continue
		for j in range (0,len(p[i].ioqueue) - 1,2):
			if p[i].ioqueue[j] <= t and t < p[i].ioqueue[j+1]:
			   check = 1	
			   p[i].status = "IO queue"
		if check == 1: 
			continue

		p[i].status = "Ready queue"
		if (p[i].come > t):     
			p[i].status = "Has not arrived yet"		
	return p
#Print final result
def PrintResult(defaultP,t,n):
	defaultP = MarkStatus(defaultP,t,n)
	ts = 'In t = ' + str(t)
	print(ts)
	for i in range(n):
		s = 'P[' + str(i+1) +']: ' + defaultP[i].status + '.'
		print(s)
#Combine all p include burst time, io time, io queue time
def CombineResult(defaultP,p,n):
	for i in range(n):
		for j in range(len(p)):
			if defaultP[i].name == p[j].name:
				for k in range (len(p[j].bu)):
					defaultP[i].bu.append(p[j].bu[k])
				for k in range (len(p[j].io)):
					defaultP[i].io.append(p[j].io[k])
				for k in range (len(p[j].ioqueue)):
					defaultP[i].ioqueue.append(p[j].ioqueue[k])
	return defaultP
#Push new process
def pushP(p, add, n):
	if (add.come >= p[len(p)-1].come):
		p.append(add)
		return p
	position = 0
	for i in range(n):
		if p[i].come > add.come:
			position = i
			break
	p.insert(position,add) 
	return p
#Get next process FCFS,RR
def pushQueueFCFS(q,p,t):
	for i in range(len(p)):
		if p[i].thiss == -1:
				q.put(i)	      
				return q;            	
	return q
#Get next process FJS,SRTF
def pushQueueFJS(q,p,t):
	minn = 99999
	position = -1
	for i in range(len(p)):
		if p[i].thiss == -1:
			if p[i].come <= t and p[i].burst < minn:
				position = i
				minn = p[i].burst
	if minn != 99999:
		q.put(position)
		return q		
	for i in range(len(p)):
		if p[i].thiss == -1:
				q.put(i)	      
				return q;            	
	return q

#First Come First Serve 
def FCFS(n, p, t, defaultP):
	p.sort(key = operator.attrgetter('come'))	
	q = queue.Queue()
	q.put(0)
	p[0].thiss = 1
	curTime = 0
	curIoTime = 0
	while not q.empty():
		x = q.get()
		p[x].thiss = 1
		if p[x].hasIo == 0:
			if p[x].burst != 0:
				if p[x].iostart != 0:
					if curTime < p[x].come:
						curTime = p[x].come
					p[x].bu.append(curTime)
					curTime += p[x].iostart
					p[x].bu.append(curTime)
				p[x].timeRe -= p[x].iostart
			if curIoTime < curTime:
				curIoTime = curTime
			curIoTime += p[x].iorun	
			p[x].io.append(curIoTime - p[x].iorun)
			p[x].io.append(curIoTime)
			if abs(curTime - curIoTime + p[x].iorun) != 0:
				p[x].ioqueue.append(curTime)
				p[x].ioqueue.append(curIoTime - p[x].iorun)
			p[x].hasIo = 1
		else:
			if curTime < p[x].come:
				curTime = p[x].come
			p[x].bu.append(curTime)
			curTime += p[x].timeRe
			p[x].bu.append(curTime)			
			p[x].timeRe = 0
		if p[x].timeRe!=0:       
			tmp = Process(p[x].timeRe,curIoTime,0,0,1,p[x].name)			
			p = pushP(p,tmp,n)
		q = pushQueueFCFS(q,p,curTime)

	defaultP = CombineResult(defaultP,p,n)
	PrintResult(defaultP,t,n)
#Shortest Job First
def FJS(n, p, t, defaultP):
	p.sort(key = operator.attrgetter('come','burst'))	
	q = queue.Queue()
	q.put(0)
	p[0].thiss = 1
	curTime = 0
	curIoTime = 0
	while not q.empty():
		x = q.get()
		p[x].thiss = 1
		if p[x].hasIo == 0:
			if p[x].burst != 0:
				if p[x].iostart != 0:
					if curTime < p[x].come:
						curTime = p[x].come
					p[x].bu.append(curTime)
					curTime += p[x].iostart
					p[x].bu.append(curTime)
				p[x].timeRe -= p[x].iostart
			if curIoTime < curTime:
				curIoTime = curTime
			curIoTime += p[x].iorun	
			p[x].io.append(curIoTime - p[x].iorun)
			p[x].io.append(curIoTime)
			if abs(curTime - curIoTime + p[x].iorun) != 0:
				p[x].ioqueue.append(curTime)
				p[x].ioqueue.append(curIoTime - p[x].iorun)
			p[x].hasIo = 1
		else:
			if curTime < p[x].come:
				curTime = p[x].come
			p[x].bu.append(curTime)
			curTime += p[x].timeRe
			p[x].bu.append(curTime)			
			p[x].timeRe = 0
		if p[x].timeRe!=0:       
			tmp = Process(p[x].timeRe,curIoTime,0,0,1,p[x].name)			
			p = pushP(p,tmp,n)
		q = pushQueueFJS(q,p,curTime)
	
	defaultP = CombineResult(defaultP,p,n)                                                     
	PrintResult(defaultP,t,n)
#Round Robin with quantum time
def RR(n, p, t, qtime, defaultP):
	p.sort(key = operator.attrgetter('come'))	
	q = queue.Queue()
	q.put(0)
	p[0].thiss = 1
	curTime = 0
	curIoTime = 0
	while not q.empty():
		x = q.get()
		p[x].thiss = 1
		if p[x].hasIo == 0:
			if p[x].burst != 0:
				if p[x].iostart != 0:
					if curTime < p[x].come:
						curTime = p[x].come
					p[x].bu.append(curTime)
					if curTime + p[x].iostart >= curTime + qtime:
						curTime += qtime
						p[x].timeRe -= qtime
						p[x].bu.append(curTime)						
						tmp = Process(p[x].timeRe,curTime,p[x].iostart - qtime,p[x].iorun,0,p[x].name)			
						p = pushP(p,tmp,n)
						q = pushQueueFCFS(q,p,curTime)
						continue
					else:
						curTime += p[x].iostart
					p[x].bu.append(curTime)
				p[x].timeRe -= p[x].iostart
			if curIoTime < curTime:
				curIoTime = curTime
			curIoTime += p[x].iorun	
			p[x].io.append(curIoTime - p[x].iorun)
			p[x].io.append(curIoTime)
			if abs(curTime - curIoTime + p[x].iorun) != 0:
				p[x].ioqueue.append(curTime)
				p[x].ioqueue.append(curIoTime - p[x].iorun)
		else:
			if curTime < p[x].come:
				curTime = p[x].come
			p[x].bu.append(curTime)
			if curTime + p[x].timeRe > curTime + qtime:
				curTime += qtime
				p[x].timeRe -= qtime
				p[x].bu.append(curTime)			
			else:
				curTime += p[x].timeRe
				p[x].bu.append(curTime)			
				p[x].timeRe = 0
		if p[x].timeRe!=0:       
			if p[x].hasIo == 0:
				come = curIoTime
			else:
				come = curTime
			tmp = Process(p[x].timeRe,come,0,0,1,p[x].name)			
			p = pushP(p,tmp,n)
		p[x].hasIo = 1
		q = pushQueueFCFS(q,p,curTime)

	defaultP = CombineResult(defaultP,p,n)
	PrintResult(defaultP,t,n)
#Shortest Remaining Time First
#Check in i-time has process come 	
def CheckP(x,p):
	if x < len(p) - 1:
		for i in range(len(p)):
			if i != x and p[i].thiss == -1:
				if p[i].burst < p[x].burst:
					return i						
	return -1	

def SRTF(n,p,t,defaultP):
	p.sort(key = operator.attrgetter('come','burst'))
	q = queue.Queue()
	q.put(0)
	p[0].thiss = 1
	curTime = 0
	curIoTime = 0
	cnt = 0
	while not q.empty():
		x = q.get()
		y = CheckP(x,p)
		cnt += 1;
		if y != -1 and p[x].come >= curTime and p[x].iostart != 0:
			p[x].hasIo = 1
			tmp = Process(p[x].burst-p[y].come,p[y].come,p[x].iostart-p[y].come,p[x].iorun,0,p[x].name)			
			p[x].burst = p[y].come;
			p[x].timeRe = p[x].burst						
			p = pushP(p,tmp,n)
		p[x].thiss = 1
		if p[x].hasIo == 0:
			if p[x].burst != 0:
				if p[x].iostart != 0:
					if curTime < p[x].come:
						curTime = p[x].come
					p[x].bu.append(curTime)
					curTime += p[x].iostart
					p[x].bu.append(curTime)
				p[x].timeRe -= p[x].iostart
			if curIoTime < curTime:
				curIoTime = curTime
			curIoTime += p[x].iorun	
			p[x].io.append(curIoTime - p[x].iorun)
			p[x].io.append(curIoTime)
			if abs(curTime - curIoTime + p[x].iorun) != 0:
				p[x].ioqueue.append(curTime)
				p[x].ioqueue.append(curIoTime - p[x].iorun)
			p[x].hasIo = 1
		else:
			if curTime < p[x].come:
				curTime = p[x].come
			p[x].bu.append(curTime)
			curTime += p[x].timeRe
			p[x].bu.append(curTime)			
			p[x].timeRe = 0
		if p[x].timeRe!=0:       
			tmp = Process(p[x].timeRe,curIoTime,0,0,1,p[x].name)			
			p = pushP(p,tmp,n)
		q = pushQueueFJS(q,p,curTime)

	defaultP = CombineResult(defaultP,p,n)
	PrintResult(defaultP,t,n)

#Input
#start_time = time.time()
kind = input()
n = int(input())
p = []
for x in range(n):
	lst = list(map(float,input().split(' ')))
	info = Process(lst[0],lst[1],lst[2],lst[3],0,x)
	p.append(info)
quantum = 0
if kind == 'RR':
	quantum = float(input())	
t = float(input())
defaultP = copy.deepcopy(p)
if kind == 'FCFS':
	FCFS(n,p,t,defaultP)
elif kind == 'FJS':
	FJS(n,p,t,defaultP)
elif kind == 'SRTF':
	SRTF(n,p,t,defaultP)
else:
	RR(n,p,t,quantum,defaultP)
#print("--- %s seconds ---" % (time.time() - start_time))






	
						