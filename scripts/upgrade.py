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
  if chain.id == 3:
    proxy_address = '0xF201327da0698696b9C1362Ff8091eD869eC95d1'
  elif chain.id == 42:
    proxy_address = '0x0A327833232Ec4c88DbFa0ae6E44b31D6956088e'
  else:
    print(f'{TERM_RED}Proxy is not deployed yet on current chain{TERM_NFMT}')
    return
  proxy = Contract.from_abi('Proxy', proxy_address, FlexUSDV2.abi)
  proxy.updateCode(fusd, {'from': acct, 'gas_price': gas_price})
  print(f'\tUpdate successful!\n')
