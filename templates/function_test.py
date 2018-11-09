import numpy as np
import math
from matplotlib import pylab
import pylab as plt


def sigmoid(x):
    return (1 / (1 + float(0.0005)*(np.exp(-(x-8)))))

q = 0
Q = 13

nq = 4
nQ = 3777 - Q
print "q = %i\n Q = %i\n nq = %i\n nQ = %i\n"%(q,Q,nq,nQ)

if q == 0:
    q = 0.1
if nq == 0:
    nq = 0.1

def formula(q,Q,nq,nQ):
	return math.log((q / float(Q)) / float((nq / float(nQ))), 2)

def formula_wsigm(q,Q,nq,nQ):
	return math.log((q / float(Q)) / float((nq / float(float(nQ*sigmoid(Q))))), 2)


def formula_lin_zerocorr(q,Q,nq,nQ):
	
	#if Q <= 40:
	#	nq_corr = 0.025*Q
	#else:
	#	nq_corr = 1
	#nQ = nQ * nq_corr
	
	nq_corr = 1
	if q == 0.1:
		zero_corr = math.log((0.1 / float(Q)) / float((1 / float(nQ))), 2)
	else:
		zero_corr = 0
	print "nQ corr",nq_corr,"\tnew nQ:",nQ,"\nzero corr",zero_corr
	return nq_corr*math.log((q / float(Q)) / float((nq / float(nQ))), 2) - zero_corr

Phenotype_score = formula(q,Q,nq,nQ)
Phenotype_score_wsigm = formula_wsigm(q,Q,nq,nQ)
Phenotype_score_lin_zerocorr = formula_lin_zerocorr(q,Q,nq,nQ)

print "PS original", Phenotype_score
#print "PS with sigmoid x-8:", Phenotype_score_wsigm,"new nQ:", float(nQ*sigmoid(Q)),"factor:",sigmoid(Q)
print "formula_lin_zerocorr: ", Phenotype_score_lin_zerocorr







"""
mySamples = []
mySigmoid = []

# generate an Array with value ???
# linespace generate an array from start and stop value
# with requested number of elements. Example 10 elements or 100 elements.
# 

x = plt.linspace(-1,20,100)

# prepare the plot, associate the color r(ed) or b(lue) and the label 
plt.plot(x, sigmoid(x), 'r', label='sigmoid minus 8')

# Draw the grid line in background.
plt.grid()

# Title & Subtitle
plt.title('Sigmoid Function')
plt.suptitle('Sigmoid')

# place the legen boc in bottom right of the graph
plt.legend(loc='lower right')

# write the Sigmoid formula
#plt.text(4, 0.8, r'$\sigma(x)=\frac{1}{1+e^{-x}}$', fontsize=15)

#resize the X and Y axes
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.1))
 

# plt.plot(x)
plt.xlabel('X Axis')
plt.ylabel('Y Axis')

# create the graph
plt.show()
"""
