#!/usr/bin/env python

import doctest

__author__ = 'Gabriele Modena <gm@nowave.it>'

"""
  Given two positive integers $L and $R we need to find Plusified
  expressions of both for which Eval($E_L) == Eval($E_R).
  
  A plusified expression is an expression where we can choose whether to add a single
  "+" between any consecutive digit.

  For a detailed problem definition see: http://blog.tty.nl/2009/08/19/haskell-solution-to-perl-quiz-of-the-week-plusified-equations/
"""


def read_numbers(greet="Please enter two space-separated positive integers\n"):
    """
    Read a string of 2 space-separated positive integers from stdin and
    return them individually
    
    >>> num_str = '123 96'

    >>> num_str.split()[0]
    '123'
    
    >>> num_str.split()[1]
    '96'
    """
    num_str = raw_input(greet)
    
    try:
        fst, snd = num_str.split()[0], num_str.split()[1]
        
        if fst.isdigit() and snd.isdigit() and int(fst) > 0 and int(snd) > 0:
            return fst, snd 
        else:
            raise 
    except:
        print "Invalid parameters"
        
        exit(1)
        
def plusify(fst):
    """
    Returns a plus expression dict of the input
    Key: sum
    Value: list of expressions that generated the sum
    
    >>> fst = '123'
    >>> plusify(fst)
    {24: ['1+23'], 15: ['12+3']}
    """
    fst_pls = {}
    
    for i in range(1,len(fst)):
        cur = fst[0:i], "+", fst[i:len(fst)]
        expr = "".join([x for x in cur])   
        try:
            fst_pls[eval(expr)].append(expr)
        except:
            fst_pls[eval(expr)] = [expr]
            
        
    return fst_pls
    
def find_matches(dict_rexp, dict_lexp):
    """
    yields a generator of matching sum expressions
    """
    matches = []
    for k in dict_rexp:
        try:
            for x in dict_rexp[k]:
                for y in dict_lexp[k]:
                   yield x, " = ", y
        except:
            continue
        
     
if __name__ == '__main__':
    doctest.testmod()

    fst, snd = read_numbers()
   
    
    for m in find_matches(plusify(str(fst)), plusify(str(snd))):
        print "".join(x for x in m)