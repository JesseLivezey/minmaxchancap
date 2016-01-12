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
Pyhyguess = np.ones((n,n))
#initialize the P(Yj) array 
x = 1.0/float(n)
Py = x*np.ones(float(n))
#r is the fixed classification accuracy
r = 0.40
#flatten the array
Pyhy_in=np.ravel(Pyhy, order='C')

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

#constraint 1: Pyhy > 0
def con1(inputArray):
    return inputArray.min()

#constraint 2: sum of Pyhy elements in a row is np.sum(Pyhy_i[i])
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
#        print Pyhy_i[i,i]
#        print Py[i]
            inProduct += Pyhy_i[i,i]*Py[i]
#        print inProduct
    con3a = inProduct - r
    return con3a

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