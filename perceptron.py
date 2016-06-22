#  -*- coding: utf-8 -*-
import random
import matplotlib.pyplot as plt
# 2x1+x2-1=0
def produceSample(sample_num):
	positive_sample = list()
	negative_sample = list()
	while True:
		i = random.random()
		j = random.random()
		if (2*i+j-1) > 0:
			if len(positive_sample) < sample_num:
				positive_sample.append((i, j, 1))
		if (2*i+j-1) < 0:
			if len(negative_sample) < sample_num:
				negative_sample.append((i, j, -1))
		if len(positive_sample) == sample_num and len(negative_sample) == sample_num:
			break
	return positive_sample + negative_sample
	

if __name__ == '__main__':
	data = produceSample(20)
	#print type(data)
	ps = [x for x in data if x[2] == 1]
	ns = [x for x in data if x[2] == -1]
	print ps
	ps_x1, ps_x2, ps_ylabel = zip(*ps)
	ns_x1, ns_x2, ns_ylabel = zip(*ns)

	eq = list()
	#x1*w1+x2*w2+b=0
	w1 = 1
	w2 = 1
	b = 1
	for x in range(0, 10):
		tmp = random.random()
		if tmp == 0:
			eq.append((tmp, -b*1.0/w2))
		else:
			eq.append((tmp, (-b-tmp*w1)*1.0/w2))
	eq_x1, eq_x2 = zip(*eq)
	plt.scatter(ps_x1, ps_x2, c='r')
	plt.scatter(ns_x1, ns_x2, c='g')
	plt.plot(eq_x1, eq_x2)
	plt.show()
	
	# begin
	eta = 0.05 # learning rate
	flag = 0
	for x in data:
		if x[2]*(w1*x[0]+w2*x[1]+b) < 0:
			flag = 1
		
	while True:
		#print w1, w2, b
		if flag == 0:
			break
		count = 0
		for x in data:
			count += 1
			#print x[2], (w1*x[0]+w2*x[1]+b), 'hello'
			flag = 0
			if x[2]*(w1*x[0]+w2*x[1]+b) < 0:
				flag = 1
				w1 = w1 + eta*x[0]*x[2]
				w2 = w2 + eta*x[1]*x[2]
				b = b + eta*x[2]

				eq = list()
				for m in range(0, 10):
					tmp = random.random()
					#w1*x1+w2*x2+b=0
					if w1 == 0:
						eq.append((tmp, -b*1.0/w2))
					else:
						eq.append((tmp, (-b-w1*tmp*1.0)/w2))
				eq_x1, eq_x2 = zip(*eq)
				plt.scatter(ps_x1, ps_x2, c='r')
				plt.scatter(ns_x1, ns_x2, c='g')
				plt.plot(eq_x1, eq_x2)
				plt.show()
				break
	print ps
	print
	print ns


	eq = list()
#	w1*x1+w2*x2+b=0
	for m in range(0, 10):
		tmp = random.random()
		#w1*x1+w2*x2+b=0
		if w1 == 0:
			j = -b*1.0/w2
#			eq.append((tmp, -b*1.0/w2))
		else:
			j = (-b-w1*tmp*1.0)/w2
#			eq.append((tmp, (-b-w1*x[0]*1.0)/w2))
		eq.append((tmp, j))
	eq_x1, eq_x2 = zip(*eq)
	plt.scatter(ps_x1, ps_x2, c='r')
	plt.scatter(ns_x1, ns_x2, c='g')
	print eq_x1
	print eq_x2
	print count
	plt.plot(eq_x1, eq_x2)
	plt.show()
