#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/accounts.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-25 12:55
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from decimal import Decimal
from typing import List
### Third-Party Packages ###
from brownie.convert import Wei
from brownie.network import accounts
from eth_account import Account
from pytest import fixture
from yaml import safe_load
### Local Modules ###
from . import RED, NFMT

@fixture
def admin() -> Account:
  file_name: str = 'wallet.test.yml'
  ### Load Mnemonic from YAML File ###
  try:
    with open(file_name) as f:
      content = safe_load(f)
      ### Read Mnemonic ###
      mnemonic = content.get('mnemonic', None)
      acct = accounts.from_mnemonic(mnemonic, count=1)
  except FileNotFoundError:
    print(f'{ RED }Cannot find wallet mnemonic file defined at `{ file_name }`.{ NFMT }')
    return
  ### Transfer Initial Balance to Test WAllet ###
  try:
    fund: Decimal = Wei('100 ether').to('wei')
    accounts[0].transfer(acct, fund)
  except ValueError: pass
  return acct

@fixture
def user_accounts() -> List[Account]:
  '''
  Use remaining accounts set up by Ganache-cli to be list of user accounts.
  '''
  return accounts[1:10]
