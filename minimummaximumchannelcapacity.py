#! /usr/bin/python
#Copyright Amrith Krishnan 2015-16

#import libraries
from matplotlib import pyplot as plt
import numpy as np
import random
from scipy import optimize
import math

#Pyhy[i,j] signifies the probability that the predicted class i is chosen given that the true class is j
#Pyh[i] signifies the probability that an object is predicted to be in class i
#Py[j] is the probability that a random object is from class j

#initialize a test matrix
def initializer(r, n):
    matrix = np.random.rand(n,n)
    np.fill_diagonal(matrix, 0)
    matrix /= matrix.sum(axis=1, keepdims = True)
    matrix *= 1-r
    np.fill_diagonal(matrix, r)
    return matrix
    
#Calculate Pyh[i] given n, Pyhy, and Py using the formula sigma(index j) P(Yhi|Yj)*P(Yj)
def calcPyh(inputArray, n, Py):
    Pyh = np.zeros(n)
    Pyhy_i = inputArray.reshape(n,n)
#use Py = Pyhy.dot(Py) --- use numpy functionality to shorten and condense code
    for i in range(n):
        for j in range(n):
            Pyh[i] = Pyh[i] + Py[j]*Pyhy_i[j,i]
    return Pyh

#calculate c given Pyhy, Py, Pyh using the formula for channel capacity (without the supremum)
def chCapMin(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    chanCap = 0.0
    Pyh_i = calcPyh(Pyhy_i, n, Py)
    for i in range(n):
        for j in range(n):
            try:
#                print(Pyhy_i[i])
                inParenPrimer = float(Pyhy_i[i,j])/float(Pyh_i[i])
            except ZeroDivisionError:
                pass 
            if inParenPrimer > 0:
                inParen = math.log(inParenPrimer, 2)
                #combine all these values into a single statement to shorten code
                #higher level coding allows us to simplify how we think about the program
                #and also to use other python libraries/functions/algorithms in this code
                a = float(Pyhy_i[i,j])
                b = float(Py[j])
                d = float(inParen)
                c = a*b*d
                chanCap = chanCap + c
    return chanCap

def chCapMax(inputArray, r, n, Py):
    return -chCapMin(inputArray, r, n, Py)

#constraint 1 (con1) was removed and replaced by the 'bounds' method in minimize.fmin_slsqp 

#constraint 2: sum of Pyhy elements in a row is np.sum(Pyhy_i[i]) = 1.0
def con2(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    inputArraySum = 0
    for i in range(n):
        inputArraySum += (np.sum(Pyhy_i[i])-1)**2
    con2a = inputArraySum
    return con2a

#constraint 3: fixed classification accuracy, summation(index i) of Pyhy * Py = r
def con3(inputArray, r, n, Py):
    inProduct = 0
    Pyhy_i = inputArray.reshape(n,n)
    for i in range(n):
            inProduct += Pyhy_i[i,i]*Py[i]
    con3a = inProduct - r
    return con3a
    
#this is the constraint that makes Pyhy[i,i] > Pyhy[i,j]
def con4(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    Pyhy_diag = np.diag(Pyhy_i)
    Pyhy_max = Pyhy_i.max(axis=1)
    diff = Pyhy_diag - Pyhy_max
    worst_case = diff.min()
    return worst_case