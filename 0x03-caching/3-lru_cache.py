#!/usr/bin/python3
""" LRU Caching """

from collections import deque
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRU Caching """
    def __init__(self):
        """ constructor """
        super().__init__()
        self.__deque = deque()

    def put(self, key, item):
        """ Save data """
        if key and item:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                removed = self.__deque.popleft()
                del self.cache_data[removed]
                print("DISCARD: {}".format(removed))
            elif key in self.cache_data:
                self.__deque.remove(key)

            self.__deque.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """ Return data """
        if key in self.cache_data:
            self.__deque.remove(key)
            self.__deque.append(key)
            return self.cache_data[key]
        return None
