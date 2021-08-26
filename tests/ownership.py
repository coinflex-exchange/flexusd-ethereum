#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/ownership.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-26 11:16
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
from . import BLUE, NFMT
from .accounts import *
from .deployments import *

def test_mint(admin: Account, wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Ownership Test #1: Minting test.{ NFMT }')
  amount: int           = 100
  amount_wei: Decimal   = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSD     = wrap_flex_proxy
  total_supply: Decimal = flex_usd.totalSupply().to('wei')
  print(f'Total Supply: { total_supply })')
  flex_usd.mint(admin, amount_wei, { 'from': admin })
  ts_postmint: Decimal  = flex_usd.totalSupply()
  assert total_supply + amount_wei == ts_postmint
  print(f'Total Supply (Post-Mint): { ts_postmint })')

def test_burn(admin: Account, wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Ownership Test #2: Burning test.{ NFMT }')
  amount: int           = 100
  amount_wei: Decimal   = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSD     = wrap_flex_proxy
  total_supply: Decimal = flex_usd.totalSupply().to('wei')
  print(f'Total Supply: { total_supply })')
  flex_usd.burn(admin, amount_wei, { 'from': admin })
  ts_postburn: Decimal  = flex_usd.totalSupply()
  assert total_supply - amount_wei == ts_postburn
  print(f'Total Supply (Post-Burn): { ts_postburn })')

def test_pause(admin: Account, wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Ownership Test #3: Pausing test.{ NFMT }')
  flex_usd: flexUSD     = wrap_flex_proxy
  flex_usd.pause({ 'from': admin })
  revert: bool          = True
  revert_msg: str 
  try:
    flex_usd.approve(admin, flex_usd.balanceOf(admin), { 'from': admin })
  except VirtualMachineError as err:
    revert = True
    revert_msg = err.message
  assert revert     == True
  assert revert_msg == 'VM Exception while processing transaction: revert the contract is paused'

def test_failed_mint(user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Ownership Test #4: Failed Minting test.{ NFMT }')
  amount: int           = 100
  amount_wei: Decimal   = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSD     = wrap_flex_proxy
  total_supply: Decimal = flex_usd.totalSupply().to('wei')
  print(f'Total Supply: { total_supply })')
  revert: bool          = False
  revert_msg: str
  try:
    flex_usd.mint(user_accounts[0], amount_wei, { 'from': user_accounts[0] })
  except VirtualMachineError as err:
    revert = True
    revert_msg = err.message
  assert revert     == True
  assert revert_msg == 'VM Exception while processing transaction: revert you are not the admin'
  ts_unchanged: Decimal  = flex_usd.totalSupply()
  assert total_supply == ts_unchanged
  print(f'Total Supply (Unchanged): { ts_unchanged })')

def test_failed_burn(user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Ownership Test #5: Failed Burning test.{ NFMT }')
  amount: int           = 100
  amount_wei: Decimal   = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSD     = wrap_flex_proxy
  total_supply: Decimal = flex_usd.totalSupply().to('wei')
  print(f'Total Supply: { total_supply })')
  revert: bool          = False
  revert_msg: str
  try:
    flex_usd.burn(user_accounts[0], amount_wei, { 'from': user_accounts[0] })
  except VirtualMachineError as err:
    revert = True
    revert_msg = err.message
  assert revert     == True
  assert revert_msg == 'VM Exception while processing transaction: revert you are not the admin'
  ts_unchanged: Decimal  = flex_usd.totalSupply()
  assert total_supply == ts_unchanged
  print(f'Total Supply (Unchanged): { ts_unchanged })')

def test_failed_pause(user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Ownership Test #6: Failed Pausing test.{ NFMT }')
  flex_usd: flexUSD     = wrap_flex_proxy
  revert: bool          = True
  revert_msg: str
  try:
    flex_usd.pause({ 'from': user_accounts[0] })
  except VirtualMachineError as err:
    revert     = True
    revert_msg = err.message
  assert revert     == True
  assert revert_msg == 'VM Exception while processing transaction: revert you are not the admin'

def test_transfer_ownership(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Ownership Test #7: Transfer Ownership test.{ NFMT }')
  flex_usd: flexUSD       = wrap_flex_proxy
  ### Transfer Ownership Away ###
  txn: TransactionReceipt = flex_usd.TransferOwnerShip(user_accounts[0], { 'from': admin })
  print(txn)
  assert txn.events['AdminChanged'] is not None
  print(txn.events)
  ### Try Pausing ###
  revert: bool            = True
  revert_msg: str
  try:
    flex_usd.pause({ 'from': admin })
  except VirtualMachineError as err:
    revert     = True
    revert_msg = err.message
  assert revert     == True
  assert revert_msg == 'VM Exception while processing transaction: revert you are not the admin'

def test_transfer_ownership_failed(user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Ownership Test #8: Transfer Ownership test from non-admin.{ NFMT }')
  flex_usd: flexUSD = wrap_flex_proxy
  revert: bool      = True
  revert_msg: str
  try:
    flex_usd.TransferOwnerShip(user_accounts[1], { 'from': user_accounts[0] })
  except VirtualMachineError as err:
    revert     = True
    revert_msg = err.message
  assert revert     == True
  assert revert_msg == 'VM Exception while processing transaction: revert you are not the admin'

def test_transfer_ownership_then_failed_mint(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Ownership Test #9: Transfer Ownership test and then failed Minting.{ NFMT }')
  flex_usd: flexUSD       = wrap_flex_proxy
  ### Transfer Ownership Away ###
  txn: TransactionReceipt = flex_usd.TransferOwnerShip(user_accounts[0], { 'from': admin })
  print(txn)
  assert txn.events['AdminChanged'] is not None
  print(txn.events)
  ### Try Minting ###
  amount: int           = 100
  amount_wei: Decimal   = Wei(f'{amount} ether').to('wei')
  total_supply: Decimal = flex_usd.totalSupply().to('wei')
  print(f'Total Supply: { total_supply })')
  revert: bool          = False
  revert_msg: str
  try:
    flex_usd.mint(user_accounts[0], amount_wei, { 'from': admin })
  except VirtualMachineError as err:
    revert = True
    revert_msg = err.message
  assert revert     == True
  assert revert_msg == 'VM Exception while processing transaction: revert you are not the admin'
  ### Assert Total Supply Unchanged ###
  ts_unchanged: Decimal = flex_usd.totalSupply()
  assert total_supply == ts_unchanged
  print(f'Total Supply (Unchanged): { ts_unchanged })')

def test_transfer_ownership_then_failed_burn(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Ownership Test #10: Transfer Ownership test and then failed Burning.{ NFMT }')
  flex_usd: flexUSD       = wrap_flex_proxy
  ### Transfer Ownership Away ###
  txn: TransactionReceipt = flex_usd.TransferOwnerShip(user_accounts[0], { 'from': admin })
  print(txn)
  assert txn.events['AdminChanged'] is not None
  print(txn.events)
  ### Try Burning ###
  amount: int           = 100
  amount_wei: Decimal   = Wei(f'{amount} ether').to('wei')
  total_supply: Decimal = flex_usd.totalSupply().to('wei')
  print(f'Total Supply: { total_supply })')
  revert: bool          = False
  revert_msg: str
  try:
    flex_usd.burn(user_accounts[0], amount_wei, { 'from': admin })
  except VirtualMachineError as err:
    revert = True
    revert_msg = err.message
  assert revert     == True
  assert revert_msg == 'VM Exception while processing transaction: revert you are not the admin'
  ### Assert Total Supply Unchanged ###
  ts_unchanged: Decimal = flex_usd.totalSupply()
  assert total_supply == ts_unchanged
  print(f'Total Supply (Unchanged): { ts_unchanged })')

def test_transfer_ownership_then_failed_pause(admin: Account, user_accounts: List[Account], wrap_flex_proxy: flexUSD):
  print(f'{ BLUE }Ownership Test #11: Transfer Ownership test and then failed Pausing.{ NFMT }')
  flex_usd: flexUSD       = wrap_flex_proxy
  ### Transfer Ownership Away ###
  txn: TransactionReceipt = flex_usd.TransferOwnerShip(user_accounts[0], { 'from': admin })
  print(txn)
  assert txn.events['AdminChanged'] is not None
  print(txn.events)
  ### Try Pausing ###
  revert: bool            = True
  revert_msg: str
  try:
    flex_usd.pause({ 'from': admin })
  except VirtualMachineError as err:
    revert     = True
    revert_msg = err.message
  assert revert     == True
  assert revert_msg == 'VM Exception while processing transaction: revert you are not the admin'
