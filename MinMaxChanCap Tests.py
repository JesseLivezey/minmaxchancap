#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

#the following are functions used to test whether the chcap function works

from minimummaximumchannelcapacity import n, Pyhy, Py, Pyhyguess, x, r, chCapMin, chCapMax, con1, con2, con3, con4
import numpy as np

Pyhy_in=np.ravel(Pyhy, order='C')

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


