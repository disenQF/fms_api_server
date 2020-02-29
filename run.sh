#!/bin/bash

cd /usr/src
gunicorn -w 2 -b 0.0.0.0:5000 server:app