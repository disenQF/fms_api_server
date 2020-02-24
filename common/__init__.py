#!/usr/bin/python3
# coding: utf-8

from redis import Redis

rd = Redis('119.3.170.97', port=6379, db=3, decode_responses=True)

if __name__ == '__main__':
    print(rd.keys('*'))