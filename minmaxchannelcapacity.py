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
Pyhy = np.array([[0.1, 0.4, 0.5], [0.3, 0.4, 0.3], [0.5, 0.1, 0.4]])
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
    chanCap = 0.0
    Pyh_i = calcPyh(Pyhy_i)
    for i in range(n):
        for j in range(n):
            inParenPrimer = float(Pyhy_i[i,j])/float(Pyh_i[i])
            if inParenPrimer > 0:
                inParen = math.log(inParenPrimer, 2)
                a = float(Pyhy_i[i,j])
                b = float(Py[j])
                d = float(inParen)
                c = a*b*d
                chanCap = chanCap + c
    return chanCap

def chCapMax(inputArray):
    return -chCapMin(inputArray)

#constraint 1: Pyhy > 0
def con1(inputArray):
    return inputArray.min()

#constraint 2: sum of Pyhy elements in a row = 1 because total probability is 1
def con2(inputArray):
    Pyhy_i = inputArray.reshape(n,n)
    inputArraySum = np.sum(Pyhy_i)
    con2a = inputArraySum - (n**2)
#    for j in range(n-1):
#        axisSum = Pyhy_i.sum(axis=j)-1
#        con2a = (axisSum**2).min()
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
    for i in range(n):
        axisSum = np.sum(Pyhy, axis=i)
        inSummation = axisSum*Py[i]
    con3z = inSummation - r
    return con3z

#this is the constraint that applies to rows where there are only 0s and 1s?
def con4(inputArray):
    Pyhy_i = inputArray.reshape(n,n)
    for i in range(n):
        for j in range(n):
            zeros = Pyhy_i[i,j] - Pyhy_i[i,j-1]
    con4a = zeros - 1.0
    return con4a

#Set the constraints on the function "cap"
cons = ({'type': 'ineq', 'fun' : con1},
        {'type': 'eq', 'fun' : con2},
        {'type': 'eq', 'fun' : con3},
        {'type': 'ineq', 'fun' : con4})
          
#use an optimization to minimize the function in the form "minimize(funcName, [guess], constraints=, method=, options= )
#may have to add additional arguments to maximize

#the following optimization minimizes the function
          
minimizePyhy = optimize.minimize(chCapMin, Pyhyguess, constraints=cons, method='SLSQP', options={'disp': True})
#print minimizePyhy

minimizePyhyfmin = optimize.fmin_slsqp(chCapMin, Pyhyguess, eqcons=[con3,con2], ieqcons=[con1,con4])
#print minimizePyhyfmin

#the following optimization maximizes the function by minimizing the negative of the function

maximizePyhy = optimize.minimize(chCapMax, Pyhyguess, constraints=cons, method='SLSQP', options={'disp': True})
#print maximizePyhy

maximizePyhyfmin = optimize.fmin_slsqp(chCapMax, Pyhyguess, eqcons=[con3,con2], ieqcons=[con1,con4])
#print minimizePyhyfmin

#the following are functions used to test whether the chcap function works

#the following function makes sure that for a 2darray of n x n dimensions...
#an inputArray where the diagonal is all ones and everything else is 0 yields a channel capacity of logbase2(n)

def chCapTestFunc():
    Pyhy_test = np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
    chCapTest = 0.0
    Pyhy_testi=np.ravel(Pyhy_test, order='C')
    chCapTest = chCapMin(Pyhy_testi)
    assert np.allclose(np.log2(n), chCapTest) # - - It Works!!
    return chCapTest

#the following function makes sure that for a 2darray of n x n dimensions...
#an inputArray where every item is filled with ones yields a channel capacity of 0

def chCapTestFunc2():
    Pyhy_test2 = np.array([[1.0,1.0,1.0],[1.0,1.0,1.0],[1.0,1.0,1.0]])
    chCapTest2 = 0.0
    Pyhy_test2i=np.ravel(Pyhy_test2, order='C')
    chCapTest2 = chCapMin(Pyhy_test2i)
    assert np.allclose(0.0, chCapTest2) # - - It Works!!
    return chCapTest2





    





