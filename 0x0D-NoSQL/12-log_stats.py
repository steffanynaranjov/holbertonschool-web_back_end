#!/usr/bin/env python3
"""  Log stats """
from pymongo import MongoClient


def count_logs(collection, match):
    """ function that return a logs by method """
    return collection.find(*match).count()


def print_logs(logs):
    """ function that print logs """
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    logs_len = count_logs(logs, [{}])
    print(f'{logs_len} logs')

    print('Methods:')
    for met in method:
        logs_by_method = count_logs(logs, [{'method': met}])
        print(f'\tmethod {met}: {logs_by_method}')

    count_path = count_logs(
        logs,
        [{'path': '/status'}, {'method': 'GET'}])
    print(f'{count_path} status check')


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx
    print_logs(logs)
