from eospy.cleos import Cleos

ce = Cleos(url='http://api.pennstation.eosnewyork.io:7001')

import requests

url = "https://eos.greymass.com/v1/chain/abi_json_to_bin"

payload = {"code":"eosio","args": {'creator': 'eosio', 'name': 'testtesttest', 'owner': 'EOS5YMv2UBcuiExv1C8fZjjnE4evofRdBh5Nrt8TYz44G7KC5tZNq', 'active': 'EOS5YMv2UBcuiExv1C8fZjjnE4evofRdBh5Nrt8TYz44G7KC5tZNq'},"action":"newaccount"}
response = requests.request("POST", url, json=payload)

print(response.text)

# use a string or EOSKey for push_transaction
key = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
# use EOSKey:
# import eospy.keys
# key = eospy.keys.EOSKey('5HuaTWKeGzZhqyzuzFAjjFjPnnnjdgcp562oBSS8Wv1qgDSkR2W')

resp = ce.create_account('eosio', key, 'testtesttest', 'EOS5YMv2UBcuiExv1C8fZjjnE4evofRdBh5Nrt8TYz44G7KC5tZNq', 'EOS5YMv2UBcuiExv1C8fZjjnE4evofRdBh5Nrt8TYz44G7KC5tZNq',
                         stake_net='1.0000 EOS', stake_cpu='1.0000 EOS', ramkb=8, permission='active', transfer=False, broadcast=False)

print('------------------------------------------------')
print(resp)
print('------------------------------------------------')