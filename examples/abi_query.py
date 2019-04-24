from eospy.types import Abi
from eospy.cleos import Cleos

system_accounts = ['eosio', 'eosio.token', 'eosio.msig', 'eosio.wrap']

ce = Cleos(url='https://proxy.eosnode.tools')

for acct in system_accounts:
    print('Getting abi for ' + acct)
    abi_dict = ce.get_abi(acct)
    abi = abi_dict['abi']
