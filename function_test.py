import numpy as np
import math

# Changing function of phenotype scoring to make the fault scoring right. 
# Every time the q=0, the score of low nq numbers end up in too high 
# phenotype scores, i.e. positive scores. 

# Possible solutions: 
# subsetting nQ with sigmoid function
# subsetting nQ with linear function
# normalizing score, when nq=1, PS should be zero


def sigmoid(x):
    return (1 / (1 + float(0.0005)*(np.exp(-(x-8)))))

q = 3
Q = 393

nq = 32
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



