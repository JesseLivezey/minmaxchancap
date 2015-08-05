#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from matplotlib import pyplot as plt
import numpy as np
from scipy import optimize
import math

#initialize number of classes required
n = 3.0
x = float(1/n)
#the following arrays are random arrays used to test the function
Pyhy = np.random.rand(n,n)
Pyh = np.random.rand(n,1)
Py = np.array((x,1))

print Pyhy
print Pyh
print Py
print x

#alternatively, the arrays can be configured into arrays of zeros using
#Pyhy = np.zeros((n,n))
#Pyh = np.zeros((n,1))
#Py = np.zeros((n,1))

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

#calculate c given Pyhy, Py, Pyh

def chCap(Pyhy):
    chCap1 = 0
    for i in range(n):
        for j in range(n):
            c = Pyhy[i,j]*Py[j]*math.log(Pyhy[i,j]/Pyh[i], 2)
            chCap1 = chCap1 + c
        j = j + 1
    i = i + 1
    print chCap1

chCap(Pyhy)


'''

#Set the constraints on the function "cap" - still in progress
cons = ({'type': 'eq',
          'fun' : lambda x: np.array(n*Py - 1)
          },
        {'type': 'ineq',
          'fun' : lambda x: np.array()
          },
         {'type': 'eq',
          'fun' : lambda x: np.array()
          },
         {'type': 'ineq',
          'fun' : lambda x: np.array()
          })

#minimize the function
result = optimize.minimize(cap, [0.0,1,0],
         constraints=cons, method='SLSQP', options={'disp': True})
        
print result'''

    





