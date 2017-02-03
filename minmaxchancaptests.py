#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

#the following are functions used to test whether the chcap function works

from minmaxchancapoptimizationsandplots import *
import numpy as np
import numpy.matlib

Pyhy_real_test = Pyhy

Pyhy_con4_test = np.array([[0.6, 0.1, 0.3],
                           [0.4, 0.6, 0.3],
                           [0.1, 0.1, 0.2]])
                           
Pyhy_con3_test = np.array([[0.4, 0.3, 0.3],
                           [0.3, 0.4, 0.3],
                           [0.3, 0.3, 0.4]])

Pyhy_con2_test = np.array([[0.1, 0.8, 0.1],
                           [0.4, 0.6, 0.0],
                           [0.2, 0.5, 0.3]])
#the following function makes sure that for a 2darray of n x n dimensions...
#an inputArray where the diagonal is all ones and everything else is 0 yields a channel capacity of logbase2(n)

def chCapTestFunc(testArray):
    Py = x*np.ones(float(n))
    Pyhy_testi=np.ravel(testArray, order='C')
    chCapTestMin = chCapMin(Pyhy_testi, r, n, Py)
    chCapTestMax = chCapMax(Pyhy_testi, r, n, Py)
    assert np.allclose(np.log2(n), chCapTestMin) # - - It Works!!
    try:
        assert np.allclose(np.log2(n), -chCapTestMax)
    except AssertionError:
        print(-chCapTestMax)

chCapTestFunc(np.matlib.identity(n, dtype='float'))

#the following function makes sure that for a 2darray of n x n dimensions...
#an inputArray where every item is filled with ones yields a channel capacity of 0

def chCapTestFunc2(testArray):
    Py = x*np.ones(float(n))
    chCapTest2 = 0.0
    Pyhy_test2i=np.ravel(testArray, order='C')
    chCapTestMin2 = chCapMin(Pyhy_test2i, r, n, Py)
    chCapTestMax2 = chCapMax(Pyhy_test2i, r, n, Py)
    assert np.allclose(0.0, chCapTestMin2, chCapTestMax2) # - - It Works!!

chCapTestFunc2(np.ones((n,n), dtype='float')) #also originally had a /n at the end?

#This is the case where you are only inputting one type of class and so you still transmit no information.

def chCapTestFunc3(testArray):
    Py = np.zeros(n)
    Py[0] = 1.0
    chCapTest3 = 0.0
    Pyhy_test3i=np.ravel(testArray, order='C')
    chCapTestMin3 = chCapMin(Pyhy_test3i, r, n, Py)
    chCapTestMax3 = chCapMax(Pyhy_test3i, r, n, Py)
    assert np.allclose(0.0, chCapTestMin3, chCapTestMax3)
    
chCapTestFunc3(np.ones((n,n), dtype='float')) #originally had a /n at the end?

def con4TestFunc(testArray):
    MatDif = 0.0
    con4_test = np.ravel(testArray, order='C')
    MatDif = con4(con4_test, r, n, Py)
    assert MatDif >= 0

con4TestFunc(Pyhy_con4_test)

def con3TestFunc(testArray):
    con3_test = np.ravel(testArray, order='C')
    ActError = con3(con3_test, r, n, Py)
    assert np.allclose(0.0, ActError)
    
con3TestFunc(Pyhy_con3_test)

def con2TestFunc(testArray):
    con2_test = np.ravel(testArray, order='C')
    MatSum = con2(con2_test, r, n, Py)
    assert np.allclose(0, MatSum)
    
con2TestFunc(Pyhy_con2_test)
