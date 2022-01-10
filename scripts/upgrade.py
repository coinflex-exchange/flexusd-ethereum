from brownie import FlexUSDV2, Proxy
from brownie.network import Chain, accounts
from brownie.network.contract import Contract
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
  print(f'\t{ TERM_GREEN }FlexUSD Implementation Logic V2 Deployment{ TERM_NFMT }')
  fusd = FlexUSDV2.deploy({'from': acct, 'gas_price': gas_price}, publish_source=True)
  print(f'\tDeployed successful!\n')
  
  # update proxy
  print(f'\t{ TERM_GREEN }FlexUSD Proxy Update logic{ TERM_NFMT }')
  proxy_address = '0xF201327da0698696b9C1362Ff8091eD869eC95d1'
  proxy = Contract.from_abi('Proxy', proxy_address, FlexUSDV2.abi)
  proxy.updateCode(fusd, {'from': acct, 'gas_price': gas_price})
  print(f'\tUpdate successful!\n')

# Running 'scripts/upgrade.py::main'...
#         Network Chain-ID: <Chain object (chainid=3, height=11788435)>
#         Account Address:  0x945e9704D2735b420363071bB935ACf2B9C4b814
#         Account Balance:  1697893782406130262

#         FlexUSD Implementation Logic V2 Deployment
# Transaction sent: 0x5c4d64c5ab90ffe046109bdb71b5aa46a7ef0591f5c0aa0d8dd50c24af3165aa
#   Gas price: 2.0 gwei   Gas limit: 2044227   Nonce: 47
#   FlexUSDV2.constructor confirmed   Block: 11788437   Gas used: 1858389 (90.91%)
#   FlexUSDV2 deployed at: 0xCA733eA3F85683A11Ebf03cfe350787a79e644CA

# Waiting for https://api-ropsten.etherscan.io/api to process contract...
# Verification submitted successfully. Waiting for result...
# Verification pending...
# Verification complete. Result: Pass - Verified
#         Deployed successful!

#         FlexUSD Proxy Update logic
# Transaction sent: 0xee587196384fd477f2ef58baf0047215632c7d473e10054ca4ba27cbc24adc08
#   Gas price: 2.0 gwei   Gas limit: 50025   Nonce: 48
#   Transaction confirmed   Block: 11788441   Gas used: 38128 (76.22%)

#         Update successful!