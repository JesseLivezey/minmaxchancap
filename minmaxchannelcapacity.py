#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from matplotlib import pyplot as plt
import numpy as np
from scipy import optimize
import math

#initialize variables and numpy arrays
j = 0
i = 0
c = 0
n = 3
r = 0
Pyhy = np.zeros((n,n))
Pyh = np.zeros((n,1))
Py = np.zeros((n,1))

Py[j] = 1/n

#Calculate Pyh[i] given n, Pyhy, and Py using the formula sigma(index j) P(Yhi|Yj)*P(Yj)
def calcPyh(n, Pyhy, Py):
    for i in range(n):
        for j in range(n):
            Pyh[i] = Pyh[i] + Py[j]*Pyhy[i,j]
            return Pyh[i]
        j = j+1
    i = i + 1
    return Pyh

#calculate c given Pyhy, Py, Pyh
def f(Pyhy, Py, Pyh):
    c = Pyhy[i,j]*Py[j]*math.log(Pyhy[i,j]/Pyh[i], 2)
    return c

#calculate the capacity with a summation with a nested "for" loop inside another "for" loop
c1 = 0
def cap(Pyhy):
    for i in range(n):
        for j in range(n):
            c1 = c + f(Pyhy, Py, Pyh)
            if Pyh[i] > 0: 
                return c
            else:
                pass
            j = j + 1
        i = i + 1
    return c


#Set the constraints on the function "cap"
cons = ({'type': 'eq',
          'fun' : lambda x: np.array(n*Py - 1),
          },
          
        {'type': 'ineq',
          'fun' : lambda x: np.array([]),
          },
          
        {'type': 'ineq',
          'fun' : lambda x: np.array([]),
          })
          
result = optimize.minimize(cap, [],
         constraints=cons, method='SLSQP', options={'disp': True})
        
print result
        
            
            
            
            
        
        
    
    
    
        
        
        


        
        

    





