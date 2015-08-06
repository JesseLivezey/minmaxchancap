#! /usr/bin/python
#Copyright Amrith Krishnan 2015

#import libraries
from matplotlib import pyplot as plt
import numpy as np
from scipy import optimize
import math

#initialize number of classes required
n = 3
n1 = float(n)
x = float(1/n1)
#the following arrays are random arrays used to test the function
Pyhy = np.random.rand(n,n)
Pyh = np.random.rand(n,1)
Py = np.array((x,1))

#alternatively, the arrays can be configured into arrays of zeros using
'''Pyhy = np.zeros((n,n))
Pyh = np.zeros((n,1))
Py = np.zeros((n,1))'''

#plot show is used to test whether the arrays are in a desirable format
'''plt.imshow(Pyhy, interpolation= 'nearest')
plt.show()

plt.imshow(Pyh, interpolation= 'nearest')
plt.show()

plt.imshow(Py, interpolation= 'nearest')
plt.show()'''

#Calculate Pyh[i] given n, Pyhy, and Py using the formula sigma(index j) P(Yhi|Yj)*P(Yj)
def calcPyh(n, Pyhy, Py):
    for i in range(n):
        for j in range(n):
            global Pyh
            Pyh[i] = Pyh[i] + Py[j]*Pyhy[i,j]
        j = j+1
    i = i + 1
    return Pyh

#plt.imshow(Pyh, interpolation='nearest')
#plt.show()

#calculate c given Pyhy, Py, Pyh using the formula for channel capacity (without the supremum)
def chCap(Pyhy):
    chCap1 = 0
    for i in range(n):
        for j in range(n):
            inParenPrimer = float(Pyhy[i,j])/float(Pyh[i])
            inParen = math.log(inParenPrimer, 2)
            c = Pyhy([i,j])*(Py[j])*(inParen)
            chCap1 = chCap1 + c
        j = j + 1
    i = i + 1
    return chCap1

#Set the constraints on the function "cap" - still in progress
cons = ({'type': 'eq',
          'fun' : lambda x: np.array(n*Py - 1)},
        {'type': 'ineq',
          'fun' : lambda x: np.array()},
         {'type': 'eq',
          'fun' : lambda x: np.array()},
         {'type': 'ineq',
          'fun' : lambda x: np.array()})
          
#use an optimization to minimize the function in the form "minimize(funcName, [guess], constraints=, method=, options= )
#may have to add additional arguments to minimize
          
result = optimize.minimize(chCap, [0.0,1,0],
         constraints=cons, method='SLSQP', options={'disp': True})
         
print result
    