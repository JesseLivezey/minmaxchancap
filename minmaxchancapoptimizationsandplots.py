#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from channel_capacity import *
import numpy as np
import random
from scipy import optimize
from matplotlib import pyplot as plt

#Pyhy[i,j] signifies the probability that the predicted class i is chosen given that the true class is j
#Pyh[i] signifies the probability that an object is predicted to be in class i
#Py[j] is the probability that a random object is from class j

r = 0.15
n = 10
Pyhy = Initializer(r, n)
Pyhy_in=np.ravel(Pyhy, order='C')
x = 1.0/float(n)
Py = x*np.ones(float(n))

'''Add in additional arguments n, Py, to the "args" parameter in the optimize.fmin_slsqp functions below'''
minimizePyhyfmin = optimize.fmin_slsqp(chCapMin, Pyhy_in, eqcons=[con3, con2], ieqcons=[con4], bounds = [(0, 1) for ii in range(n**2)], fprime = Deriver, args=(r, n, Py))
maximizePyhyfmin = optimize.fmin_slsqp(chCapMax, Pyhy_in, eqcons=[con3, con2], ieqcons=[con4], bounds = [(0, 1) for ii in range(n**2)], fprime = Deriver, args=(r, n, Py))

def plot_min():
	plt.figure()
	np.array(minimizePyhyfmin)
	minOutput = minimizePyhyfmin.reshape(n,n)
	plt.imshow(minOutput, interpolation='nearest')#, cmap='viridis')
	plt.colorbar()
	plt.title('Minimum Capacity')

plot_min()

def plot_max():
	plt.figure()
	np.array(maximizePyhyfmin)
	maxOutput = maximizePyhyfmin.reshape(n,n)
	plt.imshow(maxOutput, interpolation='nearest')#, cmap='viridis')
	plt.colorbar()
	plt.title('Maximum Capacity')

plot_max()
plt.show()

'''The following program bounds minimum and maximum capacity 
as a function of classification accuracy (r)'''
def bound_plot():
	# use plot, plot the x array as classification accuracies
     # access the last function value or Pyhy after optimization and compute channel capacity of this Pyhy
     # access the "current function value" from the dict returned y optimize.fmin_slsqp
     #for loop over accuracies and create a list of accuracies
     num = 100
     out_array_min, out_array_max = [], []
     in_array = []
     for i in range(num):
         acc = i/100
         in_array.append(acc)
         curr_max_func_value = optimize.fmin_slsqp(chCapMax, Pyhy_in, eqcons=[con3, con2], ieqcons=[con4], args=(acc, n, Py), iprint=0, bounds = [(0, 1) for ii in range(n**2)])
         curr_min_func_value = optimize.fmin_slsqp(chCapMin, Pyhy_in, eqcons=[con3, con2], ieqcons=[con4], args=(acc, n, Py), iprint=0, bounds = [(0, 1) for ii in range(n**2)])
         out_array_min.append(chCapMin(curr_min_func_value, acc, n, Py))
         out_array_max.append(chCapMax(curr_max_func_value, acc, n, Py))
     plt.scatter(in_array, out_array_min)
     plt.scatter(in_array, out_array_max)
     plt.title('Bound Minimum and Maximum')
     plt.xlabel('Classification Accuracy')
     plt.ylabel('Channel Capacity')
     plt.xlim(-1.0, 1.0)
     plt.ylim(-1.0, 1.0)
#     f1 = plt.figure()
     plt.show()

#bound_plot() 

def bit_rate_plot():
    num = 100
    N = n
    in_array, out_array = [], []
    def bit_rate(N, P):
        return np.log2(N) + (P*(np.log2(P))) + ((1 - P)*np.log2((1-P)/(N-1)))
    for i in range(num):
        acc = i/100
        in_array.append(acc)
        out_array.append(bit_rate(N, acc))
    plt.scatter(in_array, out_array)
    plt.title('Wolpaw Bit-Rate Plot Figure 4')
    plt.xlabel('Classification Accuracy')
    plt.ylabel('Channel Capacity')
    plt.xlim(0, 1.0)
#    f2 = plt.figure()
    plt.show()

#bit_rate_plot()

def second_plot():
    num = 100
    in_array, out_array = [], []
    for i in range(51, num):
        r = i/100
        in_array.append(r)
        out_array.append((r*np.log(n*r)) + ((1-r)*np.log(n*(1-r))))
    plt.scatter(in_array, out_array)
    plt.xlim(0, 1.0)
#    f3 = plt.figure()
    plt.show()
    
#second_plot()
        
        
    
         

     
     
     








