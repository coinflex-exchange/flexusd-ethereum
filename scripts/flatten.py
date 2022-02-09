#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  flatten.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-19 16:07
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
'''
Flatten two of the main contracts under contracts/ directory to flattened/ directory
'''
from brownie import FlexUSD

def main():
  with open('./flattened/FlexUSD.sol', 'wb') as f:
    f.write(FlexUSD.get_verification_info()['flattened_source'].encode('utf-8'))
