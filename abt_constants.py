#!/usr/bin/python

#
#    "global" constants needed by all
#

NSYMBOLS = 150

SMALL = 1   # flags to switch models 
BIG   = 2

T = True
F = False

Forward   = 0
Viterbi   = 1
BaumWelch = 2

######################
sig = 2.0
Ratio = 1.0    # spread of symbols relative to obs SD
di = int(Ratio*sig)   # change in output obs mean per state

K = 1000
M = 1000*1000

NEpochs = 5*K

####  How many analysis runs to do
Nruns = 10
