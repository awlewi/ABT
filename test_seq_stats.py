#!/usr/bin/python
#
#   Test observation stats 
#    generated

import sys

import numpy as np
import matplotlib.pyplot as plt
from hmm_bt import *

from abt_constants import * 

# Select the ABT file here
from simp_ABT import *    # basic 4-state HMM 
#from peg2_ABT import *         # elaborate 16-state HMM
#

nargs = len(sys.argv) - 1

#print 'Nargs: ', nargs
#print 'Argv:  ', sys.argv
#quit()

if nargs == 1:
    lfname = sys.argv[1]
elif nargs == 0:
# read in data file 
    lfname = logdir+'statelog.txt'
else:
    print 'bad command line - quitting'
    print 'you typed: ',
    for a in sys.argv:
        print '[',a,']',
    print ''        
    print 'usage test_seq_stats [filename] (containing state seq output data)'
    quit()
    
logf = open(lfname,'r')


print '\n\n\n                       Sequence Test Report '
print '                                     checking state transition stats from ground truth \n\n'

state_selection = 'l2'

X = []   # state names 
Y = []   # observations
Ls =[]   # length of the epochs/runouts

seq = [] # current state seq
os  = [] # current obs seq

Ahat = np.zeros((N,N))  # N def in model0x

for line in logf:
   #print '>>>',line
   line = line.strip()
   if line == '---': 
       # store freq of state transitions
       for i in range(len(seq)):
           if(i>0):  # no transition INTO first state
               j = names.index(seq[i])
               k = names.index(seq[i-1])
               Ahat[k,j] += 1
       Ls.append(len(os)) 
       os  = []
       seq = []
   else:
       [state, obs ] = line.split(',')
       seq.append(state)
       os.append(obs)
       X.append(state)
       Y.append([int(obs)])
       os.append([int(obs)])


#  divide to create frequentist prob estimates
for i in range(N-2):  # rows (but NOT OutS and OutF cause they don't transition out)
    rsum = np.sum(Ahat[i,:])
    #print 'A,sum', Ahat[i,:], rsum
    for j in range(N): # cols
        Ahat[i,j] /= rsum
        
#state = names[13]

N = len(names) - 2   # don't expect OutF and OutS

# set up sums for each state
s1 = np.zeros(N)
s2 = np.zeros(N)
n  = np.zeros(N)  # counts for each state

for i in range(len(X)): 
    for j in range(N):     # accumulate stats for each state
        #print X[j],names[j]
        if X[i] == names[j]:
            s1[j] +=  Y[i][0]
            s2[j] += (Y[i][0])**2
            n[j]  += 1
            #print X[j], s1[j], s2[j]

outputAmat(A,   "Model A Matrix",    names, sys.stdout)    
outputAmat(Ahat,"Empirical A Matrix",names, sys.stdout)

print 'A-matrix estimation errors: '

Adiff_Report(A,Ahat,names) 


if(False):
    # print histogram of specified state observations
    state = names[statenos[state_selection]-1]
    hist = np.zeros(NSYMBOLS)

    n2 = 0
    for i in range(len(X)):
        s = X[i]
        n2 += 1
        #print n,s,Y[i]
        if s == state:
            hist[Y[i][0]] += 1  # count the output 
        
    print 'Studied {:d} symbols for state {:s}'.format(n2,state)
    for i in range(len(hist)):
        if hist[i] > 0.001:
            print i, hist[i]
        
    
    
