#!/usr/bin/pythpn3
""" LFU cache """

from collections import OrderedDict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFU Cache """
    def __init__(self):
        super().__init__()
        self.__count = OrderedDict()

    def put(self, key, item):
        """ store data """
        if key and item:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS\
                    and key not in self.cache_data:
                self.discard()

            self.dict_count(key)
            self.cache_data[key] = item

    def get(self, key):
        """ return data """
        if key in self.cache_data:
            if key in self.__count:
                self.__count[key] += 1
            return self.cache_data[key]

        return None

    def discard(self):
        """ remove item from cache """
        minItem = min(self.__count.values())
        removed = ""
        for key in self.__count.keys():
            if self.__count[key] == minItem:
                removed = key
                break

        del self.__count[removed]
        del self.cache_data[removed]
        print("DISCARD: {}".format(removed))

    def dict_count(self, key):
        """ Create a dic """
        if key in self.cache_data:
            self.__count[key] += 1
        else:
            self.__count[key] = 1
