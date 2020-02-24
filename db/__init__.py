#!/usr/bin/python3
# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# yyserver1是在 {C:/windows/System32/drivers}/etc/hosts中配置域名
engine = create_engine('mysql+pymysql://root:root@yyserver1:3307/fms')
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
