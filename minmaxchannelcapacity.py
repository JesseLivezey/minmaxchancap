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
Pyh = np.random.rand(n,1)
Pyh /= Pyh.sum()
#initialize the P(Yj) array 
x = 1.0/float(n)
Py = x*np.ones(n)
#r is the fixed classification accuracy
r = 0.40
                
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
    return Pyh

#plt.imshow(Pyh, interpolation='nearest')
#plt.show()

#calculate c given Pyhy, Py, Pyh using the formula for channel capacity (without the supremum)
def chCapMin(inputArray):
    chCapMin1 = 0
    for i in range(n):
        for j in range(n):
            inParenPrimer = float(Pyhy[i,j])/float(Pyh[i])
            inParen = math.log(inParenPrimer, 2)
            a = float(Pyhy[i,j])
            b = float(Py[j])
            d = float(inParen)
            c = a*b*d
            chCapMin1 = chCapMin1 + c
    return chCapMin1

def chCapMax(inputArray):
    chCapMax1 = 0
    for i in range(n):
        for j in range(n):
            inParenPrimer = float(Pyhy[i,j])/float(Pyh[i])
            inParen = math.log(inParenPrimer, 2)
            a = float(Pyhy[i,j])
            b = float(Py[j])
            d = float(inParen)
            c = -(a*b*d)
            chCapMax1 = chCapMax1 + c
    return chCapMax1

#constraint 1: Pyhy > 0
def con1(inputArray):
    return Pyhy.min()

#constraint 2: sum of Pyhy elements in a row = 1 because total probability is 1
#removed as of right now because it is exiting function - "more equality constraints than independent variables"
def con2(inputArray):
    for i in range(n):
        con2a = Pyhy[i].sum() - 1
        con2b = math.pow(con2a, 2)
    return con2b

#constraint 3: fixed classification accuracy, summation(index i) of Pyhy * Pyi = r
def con3(inputArray):
    for i in range(n):
        for j in range(n):
            inProduct = Pyhy[i,j]*Py[j]
    con3a = inProduct - r 
    return con3a.min()

#this alternative 3rd constraint uses numpy.sum instead of a for loop within another for loop.
def alternativecon3(inputArray):
    axisSum = np.sum(Pyhy, axis=1)
    inSummation = axisSum*Py
    con3z = inSummation - r
    return con3z

#this is the constraint that applies to rows where there are only 0s and 1s?
def con4(inputArray):
    for i in range(n):
        for j in range(n):
            zeros = Pyhy[i,j] - Pyhy[i,j-1]
            return zeros - 1

#Set the constraints on the function "cap"
cons = ({'type': 'ineq', 'fun' : con1},
#        {'type': 'eq', 'fun' : con2},
        {'type': 'eq', 'fun' : con3})
          
#use an optimization to minimize the function in the form "minimize(funcName, [guess], constraints=, method=, options= )

#flatten the array
np.ravel(Pyhy, order='C')

#the following two optimizations minimize the function by minimizing the ChCap function (ChCapMin)
          
minimizePyhy = optimize.minimize(chCapMin, [1], constraints=cons, method='SLSQP', options={'disp': True})
print minimizePyhy

minimizePyhyfmin = optimize.fmin_slsqp(chCapMin, [1], eqcons=[con3], ieqcons=[con1])
print minimizePyhyfmin

#the following two optimizations maximize the function by minimizing the negative of the ChCap function (ChCapMax)

maximizePyhy = optimize.minimize(chCapMax, [1], constraints=cons, method='SLSQP', options={'disp': True})
print maximizePyhy

maximizePyhyfmin = optimize.fmin_slsqp(chCapMax, [1], eqcons=[con3], ieqcons=[con1]) 
print maximizePyhyfmin