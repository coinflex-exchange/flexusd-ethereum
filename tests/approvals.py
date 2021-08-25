#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/approvals.py
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
from brownie import flexUSD
from brownie.convert import Wei
from eth_account import Account
### Local Modules ###
from . import BLUE, NFMT
from .accounts import *
from .deployments import *

def test_approve_small_amount(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Approval Test #1 Admin Approves User #1 small amount.{ NFMT }')
  amount: int           = 100
  amount_wei: Decimal   = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSD     = wrap_flex_proxy
  test_account: Account = user_accounts[0]
  flex_usd.approve(test_account, amount_wei, {'from': admin})
  assert flex_usd.allowance(admin, test_account) == amount_wei

def test_approve_full_balance(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Approval Test #2 Admin Approves User #1 full balance of admin account.{ NFMT }')
  flex_usd: flexUSD     = wrap_flex_proxy
  amount_wei: int       = flex_usd.balanceOf(admin)
  test_account: Account = user_accounts[0]
  flex_usd.approve(test_account, amount_wei, {'from': admin})
  assert flex_usd.allowance(admin, test_account) == amount_wei

def test_approve_max(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Approval Test #3 Admin Approves User #1 exactly at maximum approval amount of uint256.{ NFMT }')
  amount: Decimal       = Wei('115792089237316195423570985008687907853269984665640564039457584007913129639935').to('ether') # maxapproval / 10^18
  amount_wei: Decimal   = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSD     = wrap_flex_proxy
  test_account: Account = user_accounts[0]
  flex_usd.approve(test_account, amount_wei, {'from': admin})
  assert flex_usd.allowance(admin, test_account) == amount_wei

def test_approve_above_max(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Approval Test #4 Admin Approves User #1 above maximum approval of uint256.{ NFMT }')
  amount: Decimal       = Wei('115792089237316195423570985008687907853269984665640564039457584007913129639936').to('ether') # (maxapproval + 1) / 10^18
  amount_wei: Decimal   = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSD     = wrap_flex_proxy
  test_account: Account = user_accounts[0]
  revert: bool = False
  try:
    flex_usd.approve(test_account, amount_wei, {'from': admin})
  except OverflowError: revert = True
  assert revert == True
  assert flex_usd.allowance(admin, test_account) == 0
