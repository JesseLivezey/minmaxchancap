#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

#the following are functions used to test whether the chcap function works

from minimummaximumchannelcapacity import *
import numpy as np
import numpy.matlib

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

def chCapTestFunc():
    Py = x*np.ones(float(n))
    Pyhy_test = np.matlib.identity(n, dtype='float')
    chCapTest = 0.0
    Pyhy_testi=np.ravel(Pyhy_test, order='C')
    chCapTest = chCapMin(Pyhy_testi, r)
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
    chCapTest2 = chCapMin(Pyhy_test2i, r)
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
    chCapTest3 = chCapMin(Pyhy_test3i, r)
    assert np.allclose(0.0, chCapTest3)
    
chCapTestFunc3()

def con4TestFunc(inputArray):
    MatDif = 0.0
    con4_test = np.ravel(inputArray, order='C')
    MatDif = con4(con4_test, r)
    assert np.allclose(1.0, MatDif)

con4TestFunc(Pyhy_con4_test)

def con3TestFunc(inputArray):
    con3_test = np.ravel(inputArray, order='C')
    ActError = con3(con3_test, r)
    assert np.allclose(0.0, ActError)
    
con3TestFunc(Pyhy_con3_test)

def con2TestFunc(inputArray):
    con2_test = np.ravel(inputArray, order='C')
    MatSum = con2(con2_test, r)
    assert np.allclose(0, MatSum)
    
con2TestFunc(Pyhy_con2_test)
