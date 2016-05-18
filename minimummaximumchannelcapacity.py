#! /usr/bin/python
#Copyright Amrith Krishnan 2015-16

#import libraries
from matplotlib import pyplot as plt
import numpy as np
from scipy import optimize
import math

#Pyhy[i,j] signifies the probability that the predicted class i is chosen given that the true class is j
#Pyh[i] signifies the probability that an object is predicted to be in class i
#Py[j] is the probability that a random object is from class j

Pyhy_init_guess = np.array([[0.49, 0.31, 0.21], 
                            [0.28, 0.29, 0.21], 
                            [0.25, 0.34, 0.40]])
                 
#n is the number of dimensions of the Pyhy matrix
n = raw_input('Enter the Pyhy dimensions: ')
n = int(n)

#randomize the input array
Pyhy = np.random.rand(n,n)
print Pyhy
                 
#flatten the array
Pyhy_in=np.ravel(Pyhy, order='C')

#initialize the P(Yj) array 
x = 1.0/float(n)
Py = x*np.ones(float(n))

#r is the fixed classification accuracy
r = raw_input('Enter the fixed classification accuracy: ')
r = float(r)

#Calculate Pyh[i] given n, Pyhy, and Py using the formula sigma(index j) P(Yhi|Yj)*P(Yj)
def calcPyh(inputArray):
    Pyh = np.zeros(n)
    Pyhy_i = inputArray.reshape(n,n)
    for i in range(n):
        for j in range(n):
            Pyh[i] = Pyh[i] + Py[j]*Pyhy_i[j,i]
    return Pyh

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

#constraint 1 (con1) was removed and replaced by the 'bounds' method in minimize.fmin_slsqp 

#constraint 2: sum of Pyhy elements in a row is np.sum(Pyhy_i[i]) = 1.0
def con2(inputArray):
    Pyhy_i = inputArray.reshape(n,n)
    inputArraySum = 0
    for i in range(n):
        inputArraySum += (np.sum(Pyhy_i[i])-1)**2
    con2a = inputArraySum
    return con2a

#constraint 3: fixed classification accuracy, summation(index i) of Pyhy * Py = r
def con3(inputArray):
    inProduct = 0
    Pyhy_i = inputArray.reshape(n,n)
    for i in range(n):
            inProduct += Pyhy_i[i,i]*Py[i]
    con3a = inProduct - r
    return con3a
    
#this is the constraint that makes Pyhy[i,i] > Pyhy[i,j]
def con4(inputArray):
    Pyhy_i = inputArray.reshape(n,n)
    # get diagonal vector (Pyhy[i,i])
    Pyhy_diag = np.diag(Pyhy_i)
    # get max of each row
    Pyhy_max = Pyhy_i.max(axis=1)
    # we want the difference to be positive or zero
    diff = Pyhy_diag - Pyhy_max
    # we want all of the differences to be positive, so we can just return the most negative one
    worst_case = diff.min()
    return worst_case
