#!/usr/bin/env python
# -*- coding: utf-8 -*-


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

This program can be used both as a command line utility and a module. 
Please see usage instructions in the README file of this repo at 
https://github.com/rajendrauppal/url-shortener
'''


__author__ = "Rajendra Kumar Uppal"
__copyright__ = "Copyright 2015, Rajendra Kumar Uppal"
__credits__ = ["Michael Fogleman", "Rajendra Kumar Uppal"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Rajendra Kumar Uppal"
__email__ = "rajen.iitd@gmail.com"
__status__ = "Production"


import sys
import psycopg2 # Python binding module to interface with PostgreSQL


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


class UrlDatabase(object):
    
    def __init__(self, dbname='postgres', dbuser='postgres', dbpassword='postgres'):    
        conn_str = "dbname='" + dbname + "' user='" + dbuser + "' password='" + dbpassword + "'"
        try:
            self.conn = psycopg2.connect(conn_str)
            cur = self.conn.cursor()
            table_query = "CREATE TABLE IF NOT EXISTS Urls(id serial, long_url VARCHAR(80) PRIMARY KEY)"
            cur.execute(table_query)
            self.conn.commit()
        except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
            if self.conn:
                self.conn.rollback()
            print "Error %s" % e
            sys.exit(1)

    def __del__(self):
        if self.conn:
            self.conn.close()

    def insert(self, long_url):
        num_rows = self.get_row_count() + 1
        insert_query = "INSERT INTO Urls VALUES(" + str(num_rows) + ", " + long_url + ")"
        cur = self.conn.cursor()
        cur.execute(insert_query)
        self.conn.commit()

    def get_url(self, id):
        search_query = "SELECT * FROM Urls WHERE urlid=id"
        cur = self.conn.cursor()
        cur.execute(search_query)
        rows = cur.fetchall()
        return rows

    def get_id(self, url):
        search_query = "SELECT * FROM Urls WHERE long_url=" + url
        cur = self.conn.cursor()
        cur.execute(search_query)
        rows = cur.fetchall()
        return rows[0][0]

    def get_row_count(self):
        search_query = "SELECT * FROM Urls"
        cur = self.conn.cursor()
        cur.execute(search_query)
        rows = cur.fetchall()
        return len(rows)


class UrlShortener(object):

    def __init__(self):
        self.url_encoder = UrlEncoder()
        self.url_database = UrlDatabase()

    def shorten(self, long_url, prefix_url):
        ''' Shortens long_url '''
        self.url_database.insert(long_url)
        urlid = self.url_database.get_id(long_url)
        print urlid
        encoded_url = self.url_encoder.encode_url(urlid)
        while prefix_url.endswith('/'):
            prefix_url = prefix_url[:-1]
        short_url = prefix_url + '/' + encoded_url
        return short_url

    def unshorten(self, short_url):
        ''' Unshortens short_url '''
        pass


def drop_table(table_name):
    conn_str = "dbname='postgres' user='postgres' password='postgres'"
    conn = None
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        table_query = "DROP TABLE IF EXISTS " + table_name
        cur.execute(table_query)
        conn.commit()
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        if conn:
            conn.rollback()
        print "Error %s" % e
        sys.exit(1)


def usage():
    print "Usage: Requires command line arguments."
    print "python url_shortener.py <input_url> <prefix_url> <action>"
    print "Example:"
    print "Encode: python url_shortener.py http://github.com/rajendrauppal/url-shortener http://t.co ENCODE"
    print "Encode: python url_shortener.py http://t.co/RjJw DECODE"


def main():
    num_args = len(sys.argv)
    if num_args == 4:
        input_url = "'" + sys.argv[1] + "'"
        prefix_url = sys.argv[2]
        action = sys.argv[3]
        #drop_table("Urls")
        urlshortener = UrlShortener()
        if action == "ENCODE":
            print urlshortener.shorten(input_url, prefix_url)
        elif action == "DECODE":
            print urlshortener.unshorten(input_url)
        else:
            print "Invalid action! Allowed actions are: ENCODE, DECODE"
            print "Exiting..."
            sys.exit(1)
    else:
        usage()
        sys.exit(1)

    
if __name__ == '__main__':
    main()
