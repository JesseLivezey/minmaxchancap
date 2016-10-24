#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from minimummaximumchannelcapacity import *
import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt

#the following optimization minimizes the function
'''The following functions have been commented out for isolated testing.'''
#minimizePyhyfmin = optimize.fmin_slsqp(chCapMin, Pyhy_in, eqcons=[con3, con2], ieqcons=[con4], args=(r,), bounds = [(0, 1) for ii in range(n**2)])

#the following optimization maximizes the function by minimizing the negative of the function
#maximizePyhyfmin = optimize.fmin_slsqp(chCapMax, Pyhy_in, eqcons=[con3, con2], ieqcons=[con4], args=(r,), bounds = [(0, 1) for ii in range(n**2)])

def plot_min():
	plt.figure()
	np.array(minimizePyhyfmin)
	minOutput = minimizePyhyfmin.reshape(n,n)
	plt.imshow(minOutput, interpolation='nearest')#, cmap='viridis')
	plt.colorbar()
	plt.title('Minimum Capacity')
	plt.show()

#plot_min()

def plot_max():
	plt.figure()
	np.array(maximizePyhyfmin)
	maxOutput = maximizePyhyfmin.reshape(n,n)
	plt.imshow(maxOutput, interpolation='nearest')#, cmap='viridis')
	plt.colorbar()
	plt.title('Maximum Capacity')
	plt.show()

#plot_max()

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
    #     curr_max_func_value = optimize.fmin_slsqp(chCapMax, Pyhy_in, eqcons=[con3, con2], ieqcons=[con4], args=(acc,), iprint=0, bounds = [(0, 1) for ii in range(n**2)])
         curr_min_func_value = optimize.fmin_slsqp(chCapMin, Pyhy_in, eqcons=[con3, con2], ieqcons=[con4], args=(acc,), iprint=0, bounds = [(0, 1) for ii in range(n**2)])
         out_array_min.append(chCapMin(curr_min_func_value, acc))
    #    out_array_max.append(chCapMax(curr_max_func_value, acc))
     plt.scatter(in_array, out_array_min)
    # plt.scatter(in_array, out_array_max)
     plt.title('Bound Minimum and Maximum')
     plt.xlabel('Classification Accuracy')
     plt.ylabel('Channel Capacity')
     plt.xlim(0, 1.0)
     plt.ylim(0, 1.0)
     plt.show()

bound_plot()
         
         
     
     
     
     








