#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/transactions.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-25 12:55
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from typing import List
### Third-Party Packages ###
from brownie.network.account import Account
### Local Modules ###
from . import *
from .accounts import *
from .deployments import *

def test_show_accounts(admin: Account, user_accounts: List[Account]):
  print(f'{ BLUE }Test #1 Show accounts and assure Accounts have funds.{ NFMT }')
  starting_fund: int = Wei('100 ether').to('wei')
  assert admin.balance() == starting_fund
  print(f'Admin: { admin } { GREEN }(balance={ admin.balance() }){ NFMT }')
  for i, user_account in enumerate(user_accounts):
    assert user_account.balance() == starting_fund
    print(f'User #{i + 1}: { user_account } { GREEN }(balance={ user_account.balance() }){ NFMT }')

def test_deployments(deploy_fusd: flexUSD, wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Test #2 Deploy Implementation Logic and then flexUSD.{ NFMT }')
  fusd: flexUSD       = deploy_fusd
  flex_proxy: flexUSD = wrap_flex_proxy
  ### Display Shared Logic and Separate Storage ###
  print(f'Implementation V0: { fusd } (totalSupply={ fusd.totalSupply() }, admin={ fusd.admin() })')
  print(f'flexUSD: { flex_proxy } (totalSupply={ flex_proxy.totalSupply()}, admin={ flex_proxy.admin() })')
  assert fusd.totalSupply() != flex_proxy.totalSupply() # Storage is not shared, logic is;
  assert fusd.admin()       == flex_proxy.admin()       # Initialized by the same key

def test_transfer_to_users(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Test #3 Distribute 100 each to user accounts.{ NFMT }')
  amount: int       = 100
  flex_usd: flexUSD = wrap_flex_proxy
  for i, user_account in enumerate(user_accounts):
    amount_wei: int = Wei(f'{amount} ether').to('wei')
    txn = flex_usd.transfer(user_account, amount_wei, {'from': admin})
    print(f'Transaction #{i + 1}: ' \
      f'(from={ admin.address[:20] }..., ' \
        f'to={ user_account.address[:20] }..., ' \
          f'amount={ amount }, id={ txn.txid[:20] }... ' \
        ')')
  spent: int     = len(user_accounts) * amount
  spent_wei: int = Wei(f'{spent} ether').to('wei')
  assert flex_usd.balanceOf(admin) == (flex_usd.totalSupply() - spent_wei)
