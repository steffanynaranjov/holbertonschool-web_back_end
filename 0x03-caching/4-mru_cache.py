#!/usr/bin/python3
""" MRU cache """

from collections import deque
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRU cache """
    def __init__(self):
        """ constructor """
        super().__init__()
        self.__stack = deque()

    def put(self, key, item):
        """ store data """
        if key and item:
            if key in self.cache_data:
                self.__stack.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                removed = self.__stack.popleft()
                del self.cache_data[removed]
                print("DISCARD: {}".format(removed))

            self.__stack.appendleft(key)
            self.cache_data[key] = item

    def get(self, key):
        """ Return data """
        if key in self.cache_data:
            self.__stack.remove(key)
            self.__stack.appendleft(key)
            return self.cache_data[key]
        return None
