# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 16:47:23 2021

@author: ericr
"""
import numpy as np

# Spiralize arranges array in desired goal state
def Spiralize(N):
    m = int(np.sqrt(N))
    n = m
    Sorted = np.arange(N).reshape((m,m))+1
    vals = np.arange(N).reshape((m,m))+1
    Sorted = Sorted.ravel()
    k = 0
    l = 0
    # For Array pointer 
    index = 0
    while (k < m and l < n): 
        # Print the first row 
        # from the remaining rows 
        for i in range(l, n, 1): 
            vals[k][i] = Sorted[index] 
            index += 1
        k += 1
        # Print the last column 
        # from the remaining columns 
        for i in range(k, m, 1): 
            vals[i][n - 1] = Sorted[index] 
            index += 1
        n -= 1
        # Print the last row 
        # from the remaining rows 
        if (k < m): 
            i = n - 1
            while(i >= l): 
                vals[m - 1][i] = Sorted[index] 
                index += 1
                i -= 1
            m -= 1
        # Print the first column 
        # from the remaining columns 
        if (l < n): 
            i = m - 1
            while(i >= k): 
                vals[i][l] = Sorted[index] 
                index += 1
                i -= 1
            l += 1
    # Replace center value with index
    vals[l][n]=0
    return vals.ravel()
