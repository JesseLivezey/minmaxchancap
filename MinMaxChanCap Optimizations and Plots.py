#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from minimummaximumchannelcapacity import chCapMin, chCapMax, con1, con2, con3, con4
import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt

#n is the number of dimensions of the Pyhy matrix
n = 3
#the following arrays are arrays used to test the function
Pyhy = np.array([[0.1, 0.4, 0.5], [0.3, 0.4, 0.3], [0.5, 0.1, 0.4]])
Pyhyguess = np.ones((n,n))
#initialize the P(Yj) array 
x = 1.0/float(n)
Py = x*np.ones(float(n))
#r is the fixed classification accuracy
r = 0.30
#flatten the array
Pyhy_in=np.ravel(Pyhy, order='C')

#Set the constraints on the function "cap"
cons = ({'type': 'ineq', 'fun' : con1},
        {'type': 'eq', 'fun' : con2},
        {'type': 'eq', 'fun' : con3},
        {'type': 'ineq', 'fun' : con4})
          
#use an optimization to minimize the function in the form "minimize(funcName, [guess], constraints=, method=, options= )

#the following optimization minimizes the function

minimizePyhyfmin = optimize.fmin_slsqp(chCapMin, Pyhy_in, eqcons=[con3, con2], ieqcons=[con1, con4])

plt.figure()
np.array(minimizePyhyfmin)
minOutput = minimizePyhyfmin.reshape(n,n)
plt.imshow(minOutput, interpolation='nearest')#, cmap='viridis')
plt.colorbar()
plt.title('Minimum Capacity')
plt.show()

#the following optimization maximizes the function by minimizing the negative of the function

maximizePyhyfmin = optimize.fmin_slsqp(chCapMax, Pyhy_in, eqcons=[con3, con2], ieqcons=[con1, con4])

plt.figure()
np.array(maximizePyhyfmin)
maxOutput = maximizePyhyfmin.reshape(n,n)
plt.imshow(maxOutput, interpolation='nearest')#, cmap='viridis')
plt.colorbar()
plt.title('Maximum Capacity')
plt.show()

