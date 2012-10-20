#!/bin/bash 

TARGET_ENV=py-local

wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
echo $TARGET_ENV
python virtualenv.py --no-site-packages $TARGET_ENV
