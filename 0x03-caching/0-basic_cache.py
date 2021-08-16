#!/usr/bin/python3
""" BasicCache """

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ Class BasicCache """
    def put(self, key, item):
        """ Funtion that insert values in dictionary"""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """ Function that return a key of dictionary """
        try:
            if key:
                return self.cache_data[key]
        except KeyError:
            return None
