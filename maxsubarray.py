#!/usr/bin/env python

import doctest

__author__ = "Gabriele Modena <gm@nowave.it>"
"""
Given an array of positive and negative (NON ZERO) numbers find the subarray of maximum sum.
"""

def maxsubarray(a=[-1, 2, 5, -1, 3, -2, 1]):
    """
    Linear solution to the max subarray problem.
    
    Base cases
    >>> maxsubarray([])
    []
    
    >>> maxsubarray([-1, -2, -3, -1])
    [-1]
    
    >>> maxsubarray([0, 1, -1])
    [0, 1]
    
    >>> a = [-1, 2, 5, -1, 3, -2, 1]
    >>> maxsubarray(a)
    [2, 5, -1, 3]
    """
    cur_end = 0
    cur_sum = 0
    cur_start = 0
    
    max_sum = None
    max_start = 0
    max_end = 0
        
    arr_len = len(a)
    for cur_end in range(0, len(a)):
        # compute all subarrays till the current element
        cur_sum += a[cur_end]        
        if cur_sum > max_sum:
            max_sum = cur_sum
            max_start = cur_start
            max_end = cur_end
        
        if cur_sum < 0:
            cur_sum = 0
            cur_start = cur_end + 1
        
    return a[max_start:max_end+1]
    
if __name__ == '__main__':
    doctest.testmod()
    
    try:
        a = input("Insert a python list of non zero integers (ie: [-1, 2, 5, -1, 3, -2, 1])\n")
        print "Max subarray:", maxsubarray(a) 
    except:
        print "Invalid input"
        exit(0)