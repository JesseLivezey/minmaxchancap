#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

#the following are functions used to test whether the chcap function works

#from minmaxchancapoptimizationsandplots import *
from channel_capacity import (chCapMinIterative, chCapMaxIterative, Initializer, Deriver, FixedDeriver, FixedDeriverMax, chCapMin, chCapMax,
                              con2, con3, con4)
import numpy as np
import scipy.optimize

#Pyhy_real_test = Pyhy

Pyhy_con4_test = np.array([[0.6, 0.1, 0.3],
                           [0.4, 0.6, 0.3],
                           [0.1, 0.1, 0.2]])
                           
Pyhy_con3_test = np.array([[0.4, 0.3, 0.3],
                           [0.3, 0.4, 0.3],
                           [0.3, 0.3, 0.4]])

Pyhy_con2_test = np.array([[0.1, 0.8, 0.1],
                           [0.4, 0.6, 0.0],
                           [0.2, 0.5, 0.3]])

#test the gradient vs. finite difference approximation
def check_Deriver():
    n = 3
    r = 0.4
    Py = np.ones(n)/float(n)
    x0 = np.ravel(Initializer(r, n))
    errorMin = scipy.optimize.check_grad(chCapMin, FixedDeriver, x0, r, n, Py)
    errorMax = scipy.optimize.check_grad(chCapMax, FixedDeriverMax, x0, r, n, Py)
    print(errorMin)
    print(errorMax)
    assert (errorMin > 0 and errorMin < 0.001)
    assert (errorMax > 0 and errorMax < 0.001)

check_Deriver()


#the following function makes sure that for a 2darray of n x n dimensions...
#an inputArray where the diagonal is all ones and everything else is 0 yields a channel capacity of logbase2(n)
def test_chCap_min_soln():
    n = 5
    r = None
    Py = np.ones(n)/float(n)
    Pyhy = np.ravel(np.eye(n), order='C')

    chCapTestMin = chCapMin(Pyhy, r, n, Py)
    chCapTestMax = chCapMax(Pyhy, r, n, Py)

    assert np.allclose(np.log2(n), chCapTestMin) # - - It Works!!
    assert np.allclose(np.log2(n), -chCapTestMax)


#the following function makes sure that for a 2darray of n x n dimensions...
#an inputArray where every item is filled with ones yields a channel capacity of 0
def test_chCap_uniform():
    n = 5
    r = None
    Py = np.ones(n)/float(n)
    Pyhy = np.ones((n, n))/float(n)

    chCapTestMin2 = chCapMin(Pyhy, r, n, Py)
    chCapTestMax2 = chCapMax(Pyhy, r, n, Py)

    assert np.allclose(0., chCapTestMin2) # - - It Works!!
    assert np.allclose(0., chCapTestMax2) # - - It Works!!

#This is the case where you are only inputting one type of class and so you still transmit no information.
def test_chCap_single_input():
    n = 5
    r = None
    Py = np.zeros(n)
    Py[0] = 1.0
    Pyhy_testi=np.ravel(np.eye(n), order='C')

    chCapTestMin3 = chCapMin(Pyhy_testi, r, n, Py)
    chCapTestMax3 = chCapMax(Pyhy_testi, r, n, Py)

    assert np.allclose(0.0, chCapTestMin3)
    assert np.allclose(0.0, chCapTestMax3)
    
def test_con4():
    n = 3
    r = None
    con4_test = np.ravel(Pyhy_con4_test, order='C')
    MatDif = con4(con4_test, r, n, Py)
    assert MatDif >= 0


def test_con3():
    n = 3
    r = .15
    con3_test = np.ravel(Pyhy_con3_test, order='C')
    ActError = con3(con3_test, r, n, Py)
    assert np.allclose(0.0, ActError)


def test_con2():
    n = 3
    r = None
    con2_test = np.ravel(Pyhy_con2_test, order='C')
    MatSum = con2(con2_test, r, n, Py)
    assert np.allclose(0, MatSum)
