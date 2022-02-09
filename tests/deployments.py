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
from brownie import FlexUSD, Proxy
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
def deploy_fusd(admin: Account) -> FlexUSD:
  '''
  Deploy and Inititialize Implementation Logic Contract with totalSupply of 0.
  '''
  print(f'{ BLUE }Event: flexUSD Implementation Logic V0 Deployment{ NFMT }')
  ### Deploy ###
  fusd: FlexUSD         = FlexUSD.deploy({'from': admin})
  total_supply: Decimal = Wei('0 ether').to('wei')
  ### Initialize ###
  fusd.initialize(total_supply, {'from': admin})
  return fusd

@fixture
def deploy_proxy(admin: Account, deploy_fusd: FlexUSD) -> Proxy:
  print(f'{ BLUE }Event: flexUSD Deployment{ NFMT }')
  fusd: FlexUSD = deploy_fusd
  ### Deploy ###
  total_supply: Decimal = Wei('1000000 ether').to('wei')
  init_bytes: bytes     = fusd.initialize.encode_input(total_supply)
  fusd: FlexUSD = Proxy.deploy(init_bytes, fusd, {'from': admin})
  return fusd

@fixture
def wrap_flex_proxy(deploy_proxy: Proxy) -> FlexUSD:
  '''
  Wrapping flexUSD address with flexUSDImplV0 Container and Initialize with totalSupply of 1,000,000 
  '''
  print(f'{ BLUE }Event: Wrapping flexUSD with Impl V0{ NFMT }')
  proxy: Proxy = deploy_proxy
  ### Wrap ###
  flex_proxy: FlexUSD
  try:
    flex_proxy = FlexUSD.at(proxy.address)
  except ContractExists:
    project: Project = get_loaded_projects()[0]
    build: dict      = { 'abi': FlexUSD.abi, 'contractName': 'FlexUSD' }
    flex_proxy       = ProjectContract(project, build=build, address=proxy.address)
  return flex_proxy

def test_deployments(deploy_fusd: FlexUSD, wrap_flex_proxy: FlexUSD):
  print(f'{ BLUE }Deployment Test #1: Deploy Implementation Logic and then flexUSD.{ NFMT }')
  fusd: FlexUSD       = deploy_fusd
  flex_proxy: FlexUSD = wrap_flex_proxy
  ### Display Shared Logic and Separate Storage ###
  print(f'Implementation V0: { fusd } (totalSupply={ fusd.totalSupply() }, admin={ fusd.admin() })')
  print(f'flexUSD: { flex_proxy } (totalSupply={ flex_proxy.totalSupply()}, admin={ flex_proxy.admin() })')
  assert fusd.totalSupply() != flex_proxy.totalSupply() # Storage is not shared, logic is;
  assert fusd.admin()       == flex_proxy.admin()       # Initialized by the same key
