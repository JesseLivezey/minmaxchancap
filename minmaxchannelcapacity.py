#! /usr/bin/python
#Copyright Amrith Krishnan 2015

#import libraries
from matplotlib import pyplot as plt
import numpy as np
from scipy import optimize
import math

#initialize the P(Yj) array 
n = 3
x = 1.0/float(n)

#the following arrays are arrays used to test the function
Pyhy = np.array([[0.2, 0.4, 0.4], [0.3, 0.4, 0.3], [0.5, 0.2, 0.3]])
Pyh = np.random.rand(n,1)
Pyh /= Pyh.sum()
Py = np.ndarray(shape=(n,1), dtype=float, 
                buffer=np.array([x,x,x]))
                
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
            Pyh[i] = Pyh[i] + Py[j]*Pyhy[i,j]
        j = j+1
    i = i + 1
    return Pyh

#plt.imshow(Pyh, interpolation='nearest')
#plt.show()

#calculate c given Pyhy, Py, Pyh using the formula for channel capacity (without the supremum)
def chCap():
    chCap1 = 0
    for i in range(n):
        for j in range(n):
            inParenPrimer = float(Pyhy[i,j])/float(Pyh[i])
            inParen = math.log(inParenPrimer, 2)
            a = float(Pyhy[i,j])
            b = float(Py[j])
            d = float(inParen)
            c = a*b*d
            chCap1 = chCap1 + c
        j = j + 1
    i = i + 1
    return chCap1

print chCap()

def con1(Py):
    return Py

def con2(Py):
    return np.sum(Py) - 1
    
#Set the constraints on the function "cap" - still in progress
cons = ({'type': 'ineq', 'fun' : con1},
        {'type': 'eq', 'fun' : con2})
          
#use an optimization to minimize the function in the form "minimize(funcName, [guess], constraints=, method=, options= )
#may have to add additional arguments to minimize
          
result = optimize.minimize(chCap, constraints=cons, method='SLSQP', options={'disp': True})
         
print result
    