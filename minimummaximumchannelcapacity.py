#! /usr/bin/python

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
def Initializer(r, n):
    matrix = np.random.rand(n,n)
    np.fill_diagonal(matrix, 0)
    matrix /= matrix.sum(axis=1, keepdims = True)
    matrix *= 1-r
    np.fill_diagonal(matrix, r)
    return matrix

def Deriver(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    dx = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            try:
                a = (Py[j] * math.log((Pyhy_i[i,j] / calcPyh(inputArray, n, Py)[i]), 10))
                b = (1/math.log(10))
                c = (1/math.log(10)) * (1/calcPyh(inputArray, n, Py)[i])
                dx[i,j] = a + b - c
            except ValueError:
                print("Test failed. Run Again.")
    return np.ravel(dx)

def alternateDeriver(inputArray, r, n, Py):
    '''after this i want to index into this and add element by element
    using a[i,j] = (  ), b[i,j] = (  ), c[i,j] = (  ) and add a b c into dx after the summation'''
    Pyhy_i = inputArray.reshape(n,n)
    dx = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            a = Py.dot(np.log(Pyhy_i.dot(1/calcPyh(inputArray, n, Py))) / math.log(10))
            b = 1/math.log(10)
            c = 1/(calcPyh(inputArray, n, Py)*math.log(10))
            dx = a + b - c
    return np.ravel(dx)
            
#Calculate Pyh[i] given n, Pyhy, and Py using the formula sigma(index j) P(Yhi|Yj)*P(Yj)
def calcPyh(inputArray, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    Pyh = Pyhy_i.dot(Py)
    return Pyh

#calculate c given Pyhy, Py, Pyh using the formula for channel capacity (without the supremum)
def chCapMin(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    chanCap = 0.0
    Pyh_i = calcPyh(Pyhy_i, n, Py)
    for i in range(n):
        for j in range(n):
            try:
                inParenPrimer = Pyhy_i[i,j]/Pyh_i[i]
            except ZeroDivisionError:
                pass 
            if inParenPrimer > 0:
                inParen = math.log(inParenPrimer, 2)
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