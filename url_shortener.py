#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Rajendra Kumar Uppal'
__date__ = ''
__license__ = ''


'''
URL Shortener
===================
Shorten:
1. Create a database of URLs
2. Assign an integer id to the input URL
3. Use the id as the key and encode the id
4. Append the encoded string to the top-level domain URL

Unshorten:
1. Take the encoded string from short URL
2. Decode it and find its id
3. Find its corresponding long URL in the database
'''


import sys


DEFAULT_ALPHABET = 'mn6j2c4rv8bpygw95z7hsdaetxuk3fq'
DEFAULT_BLOCK_SIZE = 24
MIN_LENGTH = 5


class UrlEncoder(object):

    def __init__(self, alphabet=DEFAULT_ALPHABET, block_size=DEFAULT_BLOCK_SIZE):
        self.alphabet = alphabet
        self.block_size = block_size
        self.mask = (1 << block_size) - 1
        self.mapping = range(block_size)
        self.mapping.reverse()
    
    def encode_url(self, n, min_length=MIN_LENGTH):
        return self.enbase(self.encode(n), min_length)
    
    def decode_url(self, n):
        return self.decode(self.debase(n))
    
    def encode(self, n):
        return (n & ~self.mask) | self._encode(n & self.mask)
    
    def _encode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << i):
                result |= (1 << b)
        return result
    
    def decode(self, n):
        return (n & ~self.mask) | self._decode(n & self.mask)
    
    def _decode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << b):
                result |= (1 << i)
        return result
    
    def enbase(self, x, min_length=MIN_LENGTH):
        result = self._enbase(x)
        padding = self.alphabet[0] * (min_length - len(result))
        return '%s%s' % (padding, result)
    
    def _enbase(self, x):
        n = len(self.alphabet)
        if x < n:
            return self.alphabet[x]
        return self._enbase(x / n) + self.alphabet[x % n]
    
    def debase(self, x):
        n = len(self.alphabet)
        result = 0
        for i, c in enumerate(reversed(x)):
            result += self.alphabet.index(c) * (n ** i)
        return result


class UrlDatabase:
    pass


class UrlShortener:
    pass


def usage():
    print "Usage: Requires command line arguments."
    print "python url_shortener.py <input_url> <action>"
    print "Example:"
    print "Encode: python url_shortener.py https://github.com/rajendrauppal/url-shortener ENCODE"
    print "Encode: python url_shortener.py https://gt.co/rner DECODE"


def main():
    num_args = len(sys.argv)
    if num_args == 3:
        input_url = sys.argv[1]
        action = sys.argv[2]
        urlshortener = UrlEncoder()
        if action == "ENCODE":
            urlshortener.encode_url(input_url)
        elif action == "DECODE":
            urlshortener.decode_url(input_url)
        else:
            print "Invalid action! Allowed actions are: ENCODE, DECODE"
            print "Exiting..."
            sys.exit(1)
    else:
        usage()

    
if __name__ == '__main__':
    main()
