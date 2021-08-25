#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/deployments.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-25 12:55
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from decimal import Decimal
### Third-Party Packages ###
from brownie import flexUSD, Proxy
from brownie.convert import Wei
from brownie.exceptions import ContractExists
from brownie.network.contract import ProjectContract
from brownie.project.main import get_loaded_projects, Project
from eth_account import Account
from pytest import fixture
### Local Modules ###
from . import BLUE, NFMT
from .accounts import *

@fixture
def deploy_fusd(admin: Account) -> flexUSD:
  '''
  Deploy and Inititialize Implementation Logic Contract with totalSupply of 0.
  '''
  print(f'{ BLUE }Event: flexUSD Implementation Logic V0 Deployment{ NFMT }')
  ### Deploy ###
  fusd: flexUSD         = flexUSD.deploy({'from': admin})
  total_supply: Decimal = Wei('0 ether').to('wei')
  ### Initialize ###
  fusd.initialize(total_supply, {'from': admin})
  return fusd

@fixture
def deploy_proxy(admin: Account, deploy_fusd: flexUSD) -> Proxy:
  print(f'{ BLUE }Event: flexUSD Deployment{ NFMT }')
  fusd: flexUSD = deploy_fusd
  ### Deploy ###
  total_supply: Decimal = Wei('1000000 ether').to('wei')
  init_bytes: bytes     = fusd.initialize.encode_input(total_supply)
  fusd: flexUSD = Proxy.deploy(init_bytes, fusd, {'from': admin})
  return fusd

@fixture
def wrap_flex_proxy(deploy_proxy: Proxy) -> flexUSD:
  '''
  Wrapping flexUSD address with flexUSDImplV0 Container and Initialize with totalSupply of 1,000,000 
  '''
  print(f'{ BLUE }Event: Wrapping flexUSD with Impl V0{ NFMT }')
  proxy: Proxy = deploy_proxy
  ### Wrap ###
  flex_proxy: flexUSD
  try:
    flex_proxy = flexUSD.at(proxy.address)
  except ContractExists:
    project: Project = get_loaded_projects()[0]
    build: dict      = { 'abi': flexUSD.abi, 'contractName': 'flexUSD' }
    flex_proxy       = ProjectContract(project, build=build, address=proxy.address)
  return flex_proxy
