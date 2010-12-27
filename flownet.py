#!/usr/bin/env python

import urllib2
import re
import doctest

__author__ = "Gabriele Modena <gm@nowave.it>"
"""
Map a phone number to the corresponding words from the input dictionary that generate that number.

See http://www.flownet.com/ron/papers/lisp-java/instructions.html for full problem description

"""


CHARACTERS = {'a': 5, 'b': 7, 'c': 6, 'd': 3, 'e': 0, 'f': 4, 'g': 9, 'h': 9, 'i': 6, 'j': 1, 'k': 7, 'l': 8, 
        'm': 5, 'n': 1, 'o': 8, 'p': 8, 'q': 1, 'r': 2, 's': 3, 't': 4, 'u': 7, 'v': 6, 'w': 2, 'x': 2, 'y': 3, 'z': 9}


SAMPLE_DICT = "an\nblau\nBo\"\nBoot\nbo\"s\nda\nFee\nfern\nFest\nfort\nje\njemand\nmir\nMix\nMixer\nName\nneu\no\"d\nOrt\nso\nTor\nTorf\nWasser"
SAMPLE_INPUT = "112\n5624-82\n4824\n0721/608-4067\n10/783--5\n1078-913-5\n381482\n04824"

SAMPLE_OUTPUT = "5624-82: mir Tor\n5624-82: Mix Tor\n4824: Torf\n4824: fort\n4824: Tor 4\n10/783--5: neu o\"d 5\n10/783--5: je bo\"s 5\n10/783--5: je Bo\" da\n381482: so 1 Tor\n04824: 0 Torf\n04824: 0 fort\n04824: 0 Tor 4"


def load_words(dictionary=None):
    """
    Load dictionary
    """
    words = {}
    if not dictionary:
        dictionary = urllib2.urlopen('http://www.flownet.com/ron/papers/lisp-java/dictionary.txt').read()


    for x in dictionary.split():
        n = word2number(x)
        try:
            words[str(n)].append(x)
        except KeyError:
            words[str(n)] = [x]

    return words

def load_numbers(input=None):
    """
    Load a list of phone numbers
    """
    if not input:
        input = urllib2.urlopen('http://www.flownet.com/ron/papers/lisp-java/input.txt').read()
    
    return input
    
def word2number(word):
    """
    Map a word to a number
    
    >>> word2number("2wusch5")
    '2273695'
    """
    number = []
    
    for w in word.lower():
        if w.isdigit():
            number.append(w)
        else:
            try:
                number.append(CHARACTERS[w])
            except KeyError:
                continue
    
    return "".join(str(n) for n in number)

def generate_lookups(number):
    """
    Generate  lookup entries for a given string k
    as:
    k, k-1, k-2,...k-i for 0 <= i <= k 
    
    >>> for lk in generate_lookups("107835"): print lk
    107835
    10783
    1078
    107
    10
    1
    """
    for i, n in enumerate(number):
        yield number[:len(number)-i]

    
def find_encodings(number, words, replaced=False):
    
    """
    Base case.
    If no number is passed, yield and empty list and terminate computation.
    
    Yield-ing [] is necessary for the recursion step.
    
    
    >>> words = load_words(SAMPLE_DICT)
    >>> numbers = load_numbers(SAMPLE_INPUT)
    >>> for e in find_encodings("107835", words, numbers): print e
    ['neu', 'o"d', '5']
    ['neu', '8', 'da']
    ['je', 'bo"s', '5']
    ['je', 'Bo"', 'da']
    ['je', '7', 'o"d', '5']
    """
    if not number:
        yield []
        return 
            
    for k in generate_lookups(number):
        """
        Store all encodes for digit k
        """
        encodes = []
        
        """
        check if number 'k' can be encoded to a word
        """
        if words.has_key(k):
            encodes = words[k]
        """
        In a partial encoding that currently covers k digits, digit k+1 is encoded by itself 
        if and only if, first, digit k was not encoded by a digit and, second, there is no word
        in the dictionary that can be used in the encoding starting at digit k+1. 
            
        Here we check if this condition holds and replace DIGIT k with itself IIF:
            
        1. k has length 1 (= is a digit)
        2. k does not encode any word
        3. digit k-1 was not replaced     
        """
        replace = not encodes
        if len(k) == 1 and replace and not replaced:
            encodes = [k]
            
        elif not encodes:
            continue
        
        """
        Recursive step
        
        Recursion can end in 2 ways:
            - last k can be encoded: return all words that match the given number
            - last k can not be encoded: discard any possibly found encoding and return and empty list
        """
        for encoding in find_encodings(number[len(k):], words, replace):
            for en in encodes:
                yield [en] + encoding
                

def phone_numbers(numbers, words):
    """
    Print phone numbers translations
  
     >>> words = load_words(SAMPLE_DICT)
     >>> numbers = load_numbers(SAMPLE_INPUT)
     >>> phone_numbers(numbers, words)
     5624-82: mir Tor
     5624-82: Mix Tor
     4824: fort
     4824: Torf
     4824: Tor 4
     4824: 4 Ort
     10/783--5: neu o"d 5
     10/783--5: neu 8 da
     10/783--5: je bo"s 5
     10/783--5: je Bo" da
     10/783--5: je 7 o"d 5
     381482: so 1 Tor
     04824: 0 fort
     04824: 0 Torf
     04824: 0 Tor 4
  
    """        
    for number in numbers.split():
        m = re.sub('\D', "", number)
        
        for encoding in find_encodings(m, words, False):
            if encoding:
                print number + ":", " ".join(w for w in encoding)
    
if __name__ == '__main__':
    doctest.testmod()
 
    """
    Calling load_words and load_numbers without paramaters will use
    the sample number list and dictionary provided by flownet
    """
    words = load_words(SAMPLE_DICT)
    numbers = load_numbers(SAMPLE_INPUT)
    
    phone_numbers(numbers, words)