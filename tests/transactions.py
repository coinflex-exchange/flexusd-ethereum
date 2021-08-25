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
from decimal import Decimal
from typing import List
### Third-Party Packages ###
from brownie import flexUSD
from brownie.convert import Wei
from brownie.exceptions import VirtualMachineError
from brownie.network.transaction import TransactionReceipt
from eth_account import Account
### Local Modules ###
from . import *
from .accounts import *
from .deployments import *

def test_transfer_to_users(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Transaction Test #1: Distribute 100 each to user accounts.{ NFMT }')
  amount: int       = 100
  flex_usd: flexUSD = wrap_flex_proxy
  for i, user_account in enumerate(user_accounts):
    amount_wei: Decimal = Wei(f'{amount} ether').to('wei')
    txn = flex_usd.transfer(user_account, amount_wei, {'from': admin})
    print(f'Transaction #{i + 1}: ' \
      f'(from={ admin.address[:20] }..., ' \
        f'to={ user_account.address[:20] }..., ' \
          f'amount={ amount }, id={ txn.txid[:20] }... ' \
        ')')
  spent: int         = len(user_accounts) * amount
  spent_wei: Decimal = Wei(f'{spent} ether').to('wei')
  assert flex_usd.balanceOf(admin) == (flex_usd.totalSupply() - spent_wei)

def test_transfer_while_broke(user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  amount: int          = 100
  amount_wei: Decimal  = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSD    = wrap_flex_proxy
  test_acct: Account   = user_accounts[0]
  target_acct: Account = user_accounts[1]
  revert: bool         = False
  revert_msg: str
  try:
    flex_usd.transfer(target_acct, amount_wei, { 'from': test_acct })
  except VirtualMachineError as err:
    revert = True
    revert_msg = err.message
  assert revert     == True
  print(revert_msg)
  assert revert_msg == 'VM Exception while processing transaction: revert ERC20: transfer internalAmt exceeds balance'

def test_transfer_hot_potato(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  amount: int             = 100
  amount_wei: Decimal     = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSD       = wrap_flex_proxy
  ### First Transfer from Admin ###
  txn: TransactionReceipt = flex_usd.transfer(user_accounts[0], amount_wei, { 'from': admin })
  print(f'<Transaction (amount={amount}, txid={txn.txid[:15]}..., from={admin.address[:15]}..., to={user_accounts[0].address[:15]}...)>')
  assert flex_usd.balanceOf(user_accounts[0]) == amount_wei
  count: int = len(user_accounts)
  ### Pass the Hot Potato ###
  for i in range(count):
    if i >= count - 1: break
    from_addr: str = user_accounts[i]
    to_addr: str   = user_accounts[i+1]
    txn = flex_usd.transfer(to_addr, amount_wei, { 'from': from_addr })
    print(f'<Transaction (amount={amount}, txid={txn.txid[:15]}..., from={from_addr.address[:15]}..., to={to_addr.address[:15]}...)>')
    assert flex_usd.balanceOf(from_addr) == 0
    assert flex_usd.balanceOf(to_addr)   == amount_wei

def test_transfer_while_blacklisted(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  amount: int         = 100
  amount_wei: Decimal = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSD   = wrap_flex_proxy
  ### First Transfer from Admin ###
  from_addr: str          = admin.address
  to_addr: str            = user_accounts[0].address
  txn: TransactionReceipt = flex_usd.transfer(to_addr, amount_wei, { 'from': from_addr })
  print(f'<Transaction (amount={amount}, txid={txn.txid[:15]}..., from={from_addr[:15]}..., to={to_addr[:15]}...)>')
  assert flex_usd.balanceOf(user_accounts[0]) == amount_wei
  ### Blacklist ###
  blacklist_target: str   = user_accounts[0].address
  txn: TransactionReceipt = flex_usd.AddToBlacklist(blacklist_target, { 'from': admin })
  print(txn)
  assert txn.events['fTokenBlacklist'] is not None
  print(txn.events)
  ### Try Transferring Forward ###
  from_addr: str = user_accounts[0].address
  to_addr: str   = user_accounts[1].address
  revert: bool   = False
  revert_msg: str
  try:
    flex_usd.transfer(to_addr, amount_wei, { 'from': from_addr })
  except VirtualMachineError as err:
    revert = True
    revert_msg = err.message
  assert revert                        == True
  assert revert_msg                    == 'VM Exception while processing transaction: revert account is blacklisted'
  assert flex_usd.balanceOf(from_addr) == amount_wei # Balance Unchanged
