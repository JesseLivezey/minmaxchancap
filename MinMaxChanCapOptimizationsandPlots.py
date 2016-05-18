#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from minimummaximumchannelcapacity import n, Pyhy, Pyhy_in, Py, x, r, chCapMin, chCapMax, con2, con3, con4
import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt

#the following optimization minimizes the function

minimizePyhyfmin = optimize.fmin_slsqp(chCapMin, Pyhy_in, eqcons=[con3, con2], ieqcons=[con4], bounds = [(0, 1) for ii in range(n**2)])

plt.figure()
np.array(minimizePyhyfmin)
minOutput = minimizePyhyfmin.reshape(n,n)
plt.imshow(minOutput, interpolation='nearest')#, cmap='viridis')
plt.colorbar()
plt.title('Minimum Capacity')
plt.show()

#the following optimization maximizes the function by minimizing the negative of the function

#maximizePyhy = optimize.minimize(chCapMax, Pyhy_in, method='SLSQP', bounds = [(0, 1) for ii in range(n**2)], constraints=(cons))

maximizePyhyfmin = optimize.fmin_slsqp(chCapMax, Pyhy_in, eqcons=[con3, con2], ieqcons=[con4], bounds = [(0, 1) for ii in range(n**2)])

plt.figure()
np.array(maximizePyhyfmin)
maxOutput = maximizePyhyfmin.reshape(n,n)
plt.imshow(maxOutput, interpolation='nearest')#, cmap='viridis')
plt.colorbar()
plt.title('Maximum Capacity')
plt.show()