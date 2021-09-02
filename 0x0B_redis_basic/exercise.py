#!/usr/bin/env python3
""" basic class redis """

import uuid
import redis
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """ count the number of times a method is called """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Increments the count for a key every time the method is called
        Return:
            Value returned by the original method
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''
    Store the history of inputs and outputs
    '''
    @wraps(method)
    def wrapper(self, *args, **kwds):
        '''
        Wrapper function
        '''
        self._redis.rpush(method.__qualname__ + ':inputs', str(args))
        output = method(self, *args, **kwds)
        self._redis.rpush(method.__qualname__ + ':outputs', output)
        return output
    return wrapper


def replay(method: Callable):
    '''
    Display the history of calls of a particular function
    '''
    r = redis.Redis()
    name = method.__qualname__
    count = r.get(name).decode('utf-8')
    inputs = r.lrange(name + ':inputs', 0, -1)
    outputs = r.lrange(name + ':outputs', 0, -1)
    print('{} was called {} times:'.format(name, count))
    for i, o in zip(inputs, outputs):
        print('{}(*{}) -> {}'.format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    """ cache class """
    def __init__(self):
        """ Constructor initialized """
        self._redis = redis.Redis()
        self._redis.flushdb(asynchronous=True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ methdod that store data in redis """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[
            str, bytes, int, float]:
        """ return the the value """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, data: str) -> str:
        """
        Convert data to string
        """
        return self._redis.get(data).decode('utf-8')

    def get_int(self, data: str) -> int:
        """
        Convert data to int
        """
        return int(self._redis.get(data))
