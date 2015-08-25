#! /usr/bin/python
#Copyright Amrith Krishnan 2015

#import libraries
from matplotlib import pyplot as plt
import numpy as np
from scipy import optimize
import math

#Pyhy[i,j] signifies the probability that the predicted class i is chosen given that the true class is j
#Pyh[i] signifies the probability that an object is predicted to be in class i
#Py[j] is the probability that a random object is from class j

#n is the number of dimensions of the Pyhy matrix
n = 3
#the following arrays are arrays used to test the function
Pyhy = np.array([[0.2, 0.4, 0.4], [0.5, 0.4, 0.1], [0.3, 0.4, 0.3]])
Pyh = np.random.rand(n,1.0)
Pyhyguess = np.ones((n,n))
#initialize the P(Yj) array 
x = 1.0/float(n)
Py = x*np.ones(float(n))
#r is the fixed classification accuracy
r = 0.40
#flatten the array
Pyhy_i=np.ravel(Pyhy, order='C')
                
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
def calcPyh(inputArray):
    Pyh_i = np.zeros(n)
    Pyhy_i = inputArray.reshape(n,n)
    for i in range(n):
        for j in range(n):
            Pyh_i[i] = Pyh_i[i] + Py[j]*Pyhy_i[i,j]
    return Pyh_i

#plt.imshow(Pyh, interpolation='nearest')
#plt.show()

#calculate c given Pyhy, Py, Pyh using the formula for channel capacity (without the supremum)
def chCapMin(inputArray):
    Pyhy_i = inputArray.reshape(n,n)
    chCapMin1 = 0.0
    Pyh_ii = calcPyh(Pyhy_i)
    for i in range(n):
        for j in range(n):
            inParenPrimer = float(Pyhy[i,j])/float(Pyh_ii[i])
            if inParenPrimer > 0:
                inParen = math.log(inParenPrimer, 2)
                a = float(Pyhy[i,j])
                b = float(Py[j])
                d = float(inParen)
                c = a*b*d
                chCapMin1 = chCapMin1 + c
    return chCapMin1

def chCapMax(inputArray):
    return -chCapMin(inputArray)

#constraint 1: Pyhy > 0
def con1(inputArray):
    return inputArray.min()

#constraint 2: sum of Pyhy elements in a row = 1 because total probability is 1
#removed as of right now because it is exiting function - "more equality constraints than independent variables"
def con2(inputArray):
    Pyhy_i = inputArray.reshape(n,n)
    con2a = ((Pyhy_i.sum(axis=1)-1)**2).min() 
    return con2a

#constraint 3: fixed classification accuracy, summation(index i) of Pyhy * Pyi = r
def con3(inputArray):
    inProduct = 0
    Pyhy_i = inputArray.reshape(n,n)
    for i in range(n):
        inProduct += Pyhy_i[i,i]*Py[i]
    con3a = inProduct - r 
    return con3a

#this alternative 3rd constraint uses numpy.sum instead of a for loop within another for loop.
def alternativecon3(inputArray):
    Pyhy = inputArray.reshape(n,n)
    axisSum = np.sum(Pyhy, axis=1)
    inSummation = axisSum*Py
    con3z = inSummation - r
    return con3z

#this is the constraint that applies to rows where there are only 0s and 1s?
def con4(inputArray):
    Pyhy_i = inputArray.reshape(n,n)
    for i in range(n):
        for j in range(n):
            zeros = Pyhy_i[i,j] - Pyhy_i[i,j-1]
            return zeros - 1

#Set the constraints on the function "cap"
cons = ({'type': 'ineq', 'fun' : con1},
        {'type': 'eq', 'fun' : con2},
        {'type': 'eq', 'fun' : con3})
          
#use an optimization to minimize the function in the form "minimize(funcName, [guess], constraints=, method=, options= )
#may have to add additional arguments to maximize

#the following two optimizations minimize the function by minimizing the ChCap function
          
minimizePyhy = optimize.minimize(chCapMin, Pyhyguess, constraints=cons, method='SLSQP', options={'disp': True})
#print minimizePyhy

#minimizePyhyfmin = optimize.fmin_slsqp(chCapMin, Pyhyguess, eqcons=[con3,con2], ieqcons=[con1])
#print minimizePyhyfmin

#the following two optimizations maximize the function by minimizing the negative of the ChCap function

maximizePyhy = optimize.minimize(chCapMax, Pyhyguess, constraints=cons, method='SLSQP', options={'disp': True})
#print maximizePyhy

#maximizePyhyfmin = optimize.fmin_slsqp(chCapMax, Pyhyguess, eqcons=[con3,con2], ieqcons=[con1]) 
#print maximizePyhyfmin

#the following are functions used to test whether the chcap function works

def testfunc(inputArray):
    Pyhy_itest = np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
    Py_itest = np.array([[1.0/float(n)],[1.0/float(n)],[1.0/float(n)]])
    Pyh_itest = calcPyh(Pyhy_itest)
    chCapMin_itest = chCapMin(Pyhy_itest)
    return chCapMin_itest

minimizePyhyTestminimize = optimize.minimize(testfunc, Pyhyguess, constraints=cons, method='SLSQP', options={'disp': True})
print minimizePyhyTestminimize

minimizePyhyTestfmin = optimize.fmin_slsqp(testfunc, Pyhyguess, eqcons=[con3,con2], ieqcons=[con1])
print minimizePyhyTestfmin



