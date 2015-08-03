#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from matplotlib import pyplot as plt
import numpy as np
import scipy as sp
import math

j = 0
i = 0
c = 0
n = 3
Pyhy = 0
Pyj = float(1/n)
Pyhi = 0

def calcPyhi(n, Pyhy, Pyj):
    if j <= n:
        for j in range(n):
            Pyhi = float(Pyhy)*float(Pyj)
            return Pyhi
        
        j = j+1
        
    else:
        pass
    
def f(Pyhy, Pyj, Pyhi):
    c = Pyhy*Pyj*math.log(float(Pyhy/Pyhi), 2)
    return c
    
def cap(Pyhy):
    for i in range(n):
        for j in range(n):
            
        
        
    
    
    
        
        
        


        
        

    





