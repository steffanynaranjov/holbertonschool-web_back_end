#!/usr/bin/python3
""" 1. FIFO caching """
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """ Basic Cache class """

    def __init__(self):
        """ Override superclass __init__ """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ Setter method """
        if key is None or item is None:
            return None
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            last = list(self.cache_data.keys())[0]
            self.cache_data.pop(last)
            print("DISCARD: {}".format(last))

    def get(self, key):
        """ Getter method """
        if key in self.cache_data and key is not None:
            return self.cache_data[key]
        return None
