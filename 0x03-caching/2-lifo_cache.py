#!/usr/bin/python3
""" LIFO Caching """
from collections import OrderedDict
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFO caching """

    def __init__(self):
        """ Override superclass __init__ """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ Put element in dictionary """
        if key is None or item is None:
            return None
        if key in self.cache_data.keys():
            self.cache_data.pop(key)
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            last = list(self.cache_data)[-2]
            self.cache_data.pop(last)
            print("DISCARD: {}".format(last))

    def get(self, key):
        """ Get value linked to key """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
