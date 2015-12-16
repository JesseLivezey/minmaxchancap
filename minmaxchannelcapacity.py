#! /usr/bin/python
#Copyright Amrith Krishnan 2015

#import libraries
from matplotlib import pyplot as plt
import numpy as np
import numpy.matlib
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

#plot show is used to test whether the arrays are in a desirable format
'''plt.imshow(Pyhy, interpolation= 'nearest')
plt.colorbar()
plt.show()

plt.imshow(Pyh, interpolation= 'nearest')
plt.colorbar()
plt.show()'''

#Calculate Pyh[i] given n, Pyhy, and Py using the formula sigma(index j) P(Yhi|Yj)*P(Yj)
def calcPyh(inputArray):
    Pyh_i = np.zeros(n)
    Pyhy_i = inputArray.reshape(n,n)
    for i in range(n):
        for j in range(n):
            Pyh_i[i] = Pyh_i[i] + Py[j]*Pyhy_i[i,j]
    return Pyh_i

'''Pyh_iplot = calcPyh(Pyhy)
Pyh_iplot = [Pyh_iplot]
plt.imshow(Pyh_iplot)
plt.colorbar()
plt.show()'''

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

'''chanCapPlot = chCapMin(Pyhy)
chanCapPlot = [[chanCapPlot]]
plt.imshow(chanCapPlot)
plt.colorbar()
plt.show()'''

def chCapMax(inputArray):
    return -chCapMin(inputArray)

#constraint 1: Pyhy > 0
def con1(inputArray):
    return inputArray.min()

#constraint 2: sum of Pyhy elements in the matrix = 1*n because total probability is 1 added n times
def con2(inputArray):
    Pyhy_i = inputArray.reshape(n,n)
    inputArraySum = (np.sum(Pyhy_i))**2
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

#this is the constraint that applies to rows where there are only 0s and 1s
def con4(inputArray):
    Pyhy_i = inputArray.reshape(n,n)
    zeros=0
    for i in range(n):
        for j in range(n):
            if Pyhy_i[i,j] == 1.0:                
                zeros = Pyhy_i[i,j] - Pyhy_i[i,j-1]
    con4a = zeros - 1.0
    return con4a

#Set the constraints on the function "cap"
cons = ({'type': 'ineq', 'fun' : con1},
        {'type': 'eq', 'fun' : con2},
        {'type': 'eq', 'fun' : con3},
        {'type': 'ineq', 'fun' : con4})
          
#use an optimization to minimize the function in the form "minimize(funcName, [guess], constraints=, method=, options= )

#the following optimization minimizes the function

minimizePyhyfmin = optimize.fmin_slsqp(chCapMin, Pyhyguess, eqcons=[con3,con2], ieqcons=[con1,con4])

plt.figure()
np.array(minimizePyhyfmin)
minOutput = minimizePyhyfmin.reshape(n,n)
plt.imshow(minOutput, interpolation='nearest', cmap='viridis')
plt.colorbar()
plt.title('Minimum Capacity')

#the following optimization maximizes the function by minimizing the negative of the function

maximizePyhyfmin = optimize.fmin_slsqp(chCapMax, Pyhyguess, eqcons=[con3,con2], ieqcons=[con1,con4])

plt.figure()
np.array(maximizePyhyfmin)
maxOutput = maximizePyhyfmin.reshape(n,n)
plt.imshow(maxOutput, interpolation='nearest', cmap='viridis')
plt.colorbar()
plt.title('Maximum Capacity')
plt.show()

#the following are functions used to test whether the chcap function works

#the following function makes sure that for a 2darray of n x n dimensions...
#an inputArray where the diagonal is all ones and everything else is 0 yields a channel capacity of logbase2(n)

def chCapTestFunc():
    Py = x*np.ones(float(n))
    Pyhy_test = np.matlib.identity(n, dtype='float')
    chCapTest = 0.0
    Pyhy_testi=np.ravel(Pyhy_test, order='C')
    chCapTest = chCapMin(Pyhy_testi)
    assert np.allclose(np.log2(n), chCapTest) # - - It Works!!
    return chCapTest

chCapTestFunc()

#the following function makes sure that for a 2darray of n x n dimensions...
#an inputArray where every item is filled with ones yields a channel capacity of 0

def chCapTestFunc2():
    Py = x*np.ones(float(n))
    Pyhy_test2 = np.ones((n,n), dtype='float')/n
    chCapTest2 = 0.0
    Pyhy_test2i=np.ravel(Pyhy_test2, order='C')
    chCapTest2 = chCapMin(Pyhy_test2i)
    assert np.allclose(0.0, chCapTest2) # - - It Works!!
    return chCapTest2

chCapTestFunc2()

#This is the case where you are only inputting one type of class and so you still transmit no information.

def chCapTestFunc3():
    Py = np.zeros(n)
    Py[0] = 1.0
    Pyhy_test3 = np.ones((n,n), dtype='float')/n
    chCapTest3 = 0.0
    Pyhy_test3i=np.ravel(Pyhy_test3, order='C')
    chCapTest3 = chCapMin(Pyhy_test3i)
    assert np.allclose(0.0, chCapTest3)
    
chCapTestFunc3()





    





