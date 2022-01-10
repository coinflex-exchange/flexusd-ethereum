from brownie import flexUSD, Proxy
from brownie.network import Chain, accounts
from brownie.convert import Wei
from eth_account.account import ValidationError
from yaml import safe_load

TERM_RED   = '\033[1;31m'
TERM_NFMT  = '\033[0;0m'
TERM_BLUE  = '\033[1;34m'
TERM_GREEN = '\033[1;32m'

def main():
  chain = Chain()
  print(f'\t{TERM_GREEN}Network Chain-ID: { chain }{TERM_NFMT}')
  if chain.id not in [1,3,4,5,42]:
    return print(f'\t{TERM_RED}The Network is not supported by the script{TERM_NFMT}')

  ## load account
  file_name = 'wallet.admin.yml'
  try:
    with open(file_name) as f:
      content = safe_load(f)
      privkey = content.get('privkey', None)
      acct = accounts.add(privkey)
  except FileNotFoundError:
    print(f'{TERM_RED}Cannot find wallet file defined at `{file_name}`.{TERM_NFMT}')
    return
  except ValidationError:
    print(f'{TERM_RED}Invalid address found in wallet mnemonic file.{TERM_NFMT}')
    return
  print(f'\tAccount Address:  {acct}')
  balance = acct.balance()
  print(f'\tAccount Balance:  {balance}\n')

  gas_price = '2 gwei'

  # deploy flexUSD
  print(f'\t{ TERM_GREEN }FlexUSD Implementation Logic V0 Deployment{ TERM_NFMT }')
  fusd = flexUSD.deploy({'from': acct, 'gas_price': gas_price}, publish_source=True)
  print(f'\tDeployed successful!\n')

  # deploy proxy
  print(f'\t{ TERM_GREEN }FlexUSD Proxy Deployment{ TERM_NFMT }')
  total_supply = Wei('1000000 ether').to('wei')
  init_bytes = fusd.initialize.encode_input(total_supply)
  Proxy.deploy(init_bytes, fusd, {'from': acct, 'gas_price': gas_price}, publish_source=True)
  print(f'\tDeployed successful!\n')



# (flexusd-ethereum-Plzu0GZK-py3.7) tangwei@Tangs-MacBook-Pro flexusd-ethereum % brownie run scripts/deployment.py --network ropsten
# Brownie v1.16.1 - Python development framework for Ethereum

# FlexusdEthereumProject is the active project.

# Running 'scripts/deployment.py::main'...
#         Network Chain-ID: <Chain object (chainid=3, height=11788359)>
#         Account Address:  0x945e9704D2735b420363071bB935ACf2B9C4b814
#         Account Balance:  1705957479136963528

#         FlexUSD Implementation Logic V0 Deployment
# Transaction sent: 0xf46d0e3f115bcd4719f372a55fa93a59e2e6195f28e9da09a55233f47423d3a0
#   Gas price: 2.0 gwei   Gas limit: 2029256   Nonce: 42
#   flexUSD.constructor confirmed   Block: 11788361   Gas used: 1844779 (90.91%)
#   flexUSD deployed at: 0x7875681cC687A1F72683F746a07e7F8EBA4F4C6C

# Waiting for https://api-ropsten.etherscan.io/api to process contract...
# Verification submitted successfully. Waiting for result...
# Verification complete. Result: Already Verified
#         Deployed successful!

#         FlexUSD Proxy Deployment
# Transaction sent: 0x5344e36f669357b97a337fbd7cc504a2818b46dc50023defd67d7e16c396fe3e
#   Gas price: 2.0 gwei   Gas limit: 250229   Nonce: 43
#   Proxy.constructor confirmed   Block: 11788368   Gas used: 227481 (90.91%)
#   Proxy deployed at: 0xF201327da0698696b9C1362Ff8091eD869eC95d1

# Waiting for https://api-ropsten.etherscan.io/api to process contract...
# Verification submitted successfully. Waiting for result...
# Verification pending...
# Verification pending...
# Verification complete. Result: Already Verified
#         Deployed successful!