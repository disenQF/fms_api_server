#!/usr/bin/python3
# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import pymysql

Base = declarative_base()
metadata = Base.metadata

# yyserver1是在 {C:/windows/System32/drivers}/etc/hosts中配置域名
engine = create_engine('mysql+pymysql://root:root@yyserver1:3307/fms')
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

db_conn = pymysql.Connection(host='yyserver1',
                        port=3307,
                        user='root',
                        password='root',
                        db='fms',
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor )
