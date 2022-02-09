#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  deploy_flexusd.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-19 16:07
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
from brownie import accounts, FlexUSD, Proxy, network, Wei
from eth_account.account import ValidationError
from yaml import safe_load

TERM_RED   = '\033[1;31m'
TERM_NFMT  = '\033[0;0m'
TERM_BLUE  = '\033[1;34m'
TERM_GREEN = '\033[1;32m'

def main():
  ### Load Account to use ###
  acct = None
  chain = network.Chain()
  print(f'Network Chain-ID: { chain }')
  chain_map = {
    1: None,              # mainnet
    3: 'ropsten',         # repsten testnet
    4: 'rinkeby',         # rinkeby testnet
    5: 'goerli',          # goerli testnet
    42: 'kovan',          # kovan testnet
    1337: 'dev',          # local ganache-cli evm
    10001: 'smartbch-t1a' # smartbch testnet
  }
  if chain._chainid in (1, 3, 4, 5, 42, 1337, 10001):
    chain_name = chain_map[chain._chainid]
    file_name = 'wallet.yml' if chain_name is None else f'wallet.{chain_name}.yml'
    ### Load Mnemonic from YAML File ###
    try:
      with open(file_name) as f:
        content = safe_load(f)
        ### Read Mnemonic ###
        # mnemonic = content.get('mnemonic', None)
        # acct = accounts.from_mnemonic(mnemonic, count=1)
        ### Read Privkey ###
        privkey = content.get('privkey', None)
        acct = accounts.add(privkey)
    except FileNotFoundError:
      print(f'{TERM_RED}Cannot find wallet mnemonic file defined at `{file_name}`.{TERM_NFMT}')
      return
    except ValidationError:
      print(f'{TERM_RED}Invalid address found in wallet mnemonic file.{TERM_NFMT}')
      return
    ### Transfers some Ether for usage to dev wallet ###
    if chain._chainid == 1337: 
      try:
        accounts[0].transfer(acct, Wei('100 ether').to('wei'))
      except ValueError: pass
  else:
    print('!! Invalid chainid found.')
    return
  print(f'Account: {acct}')
  balance = acct.balance()
  print(f'Account Balance: {balance}')
  if balance == 0:
    return # If balance is zero, exits

  ### Set Gas Price ##
  gas_price = '2 gwei'

  ### Deployments ###
  ### FlexUSD Implementation Logic Deployment ###
  print(f'\t{ TERM_GREEN }FlexUSD Implementation Logic V2 Deployment{ TERM_NFMT }')
  flex_usd: FlexUSD = FlexUSD.deploy({ 'from': acct,'gas_price': gas_price}, publish_source=True)
  print(f'FlexUSD Logic Contract: { flex_usd }')

  ### FlexUSD Proxy Deployment ###
  print(f'\t{ TERM_GREEN }FlexUSD Proxy Deployment{ TERM_NFMT }')
  total_supply = Wei('1000000 ether').to('wei')
  init_bytes = flex_usd.initialize.encode_input(total_supply)
  proxy: Proxy = Proxy.deploy(init_bytes, flex_usd, {'from': acct, 'gas_price': gas_price}, publish_source=True)
  print(f'\t Proxy Deployed successfullly at {proxy} !\n')
