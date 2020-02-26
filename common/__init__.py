#!/usr/bin/python3
# coding: utf-8

from redis import Redis

rd = Redis('﻿139.129.93.165', port=6378, db=4, decode_responses=True)

if __name__ == '__main__':
    print(rd.keys('*'))