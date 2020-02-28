#!/usr/bin/python3
# coding: utf-8

from redis import Redis

rd = Redis('47.105.137.19', db=5, port=6379, decode_responses=True)

if __name__ == '__main__':
    print(rd.keys('*'))