#!/usr/bin/env python

import random
from sys import argv

"""
  O(Time) efficient poulation sampling.
  
  Sample M distinct members (integers) from a population of P elements integers in [0,P].
  
  Example:
  python sample.py <members> <population>
  
  
  
  For a full problem description see: http://www.rubyquiz.com/quiz39.html
  
  $ time python2.6 sample.py 3 10 

  real	0m0.171s
  user	0m0.056s
  sys	0m0.017s
  
  
  $ time python2.6 sample.py 400 12000 

  real	0m0.074s
  user	0m0.058s
  sys	0m0.014s
  
  $ time python2.6 sample.py 100000 5000000000 
  
  real	0m0.461s
  user	0m0.420s
  sys	0m0.037s
"""

def sample(members, limit):
    """
    Return #members samples from a #limit population
    """
    sampled = {}
    
    for i in range(0, members):
        while 1:
            cur = random.randrange(0, limit, 1)
            
            if sampled.has_key(cur):
                continue
            else:
                sampled[cur] = True
                break
    
    
    return sampled.keys()
    
if __name__ == '__main__':
    try:
        members = int(argv[1])
        population = int(argv[2])
    
    except:
        print "Invalid paramaters.\n Example: python sample.py <members> <limit>"
    
    samples = sample(members, population)
    
    for x in samples:
        print x
        